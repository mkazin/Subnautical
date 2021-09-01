import os
import pathlib

import certifi
import requests
from mongoengine import DoesNotExist
from pip._vendor import cachecontrol
from flask import Flask, request, jsonify, render_template, abort, url_for, redirect, session, flash
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from oauthlib.oauth2 import WebApplicationClient
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests

import subnautical
from model.map_data import Marker, MarkerType
from model.player_data import PlayerData
from controller.charting import Charting


# To run this from PyCharm's Python Console prompt (which lets you hit ^C):
# > runfile('D:/Work/SubnauticaMap/app.py', wdir='D:/Work/SubnauticaMap')
def init_map_data():
    return [Marker(name='Lifepod', bearing=0, distance=0, depth=0,  marker_type_name="Lifepod", color="00FF00")]


app = Flask(__name__)
app.config['SERVER_NAME'] = f"{subnautical.app_domain}:{subnautical.app_port}"
app.config['SESSION_COOKIE_DOMAIN'] = subnautical.app_domain

app.static_folder = subnautical.app_config['ROOT_PATH'] + '/static'
app.template_folder = subnautical.app_config['ROOT_PATH'].split('controller')[0] + '/view/templates'
app.config.from_object('subnautical.config')
app.config['MONGODB_SETTINGS'] = subnautical.config
app.config['MONGODB_SETTINGS']['connectTimeoutMS'] = 200
app.config['MONGODB_SETTINGS']['tlsCAFile'] = certifi.where()

db = MongoEngine(app, app.config)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "config", "client_secrets.json")


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)
app.secret_key = subnautical.GOOGLE_CLIENT_SECRET
client = WebApplicationClient(subnautical.GOOGLE_CLIENT_ID)


# Database upgrade performing two changes:
#
# 1. Converting marker types from constant enum to name/color properties
# 2. Populate x,y coordinates in database so calculation is performed only once on marker write
from utilities import geometry


def populate_x_y_coordinates(user):
    for mark in user.map_data:
        if not hasattr(mark, 'x') or mark.x is None:
            mark.x, mark.y = Charting.get_cartesean_coords(mark.distance, mark.depth, mark.bearing)
            print(f"{mark.distance} bearing {mark.bearing} translated to ({mark.x}, {mark.y})")


def upgrade_user_record(user):
    for marker in user.map_data:
        if hasattr(marker, 'marker_type') and marker.marker_type is not None:
            print(f"* upgrading marker: {marker.name}")
            marker.marker_type_name = marker.marker_type.name.capitalize()
            marker.color = '555555'
            delattr(marker, 'marker_type')

    print('Saving user')

def upgrade_all_users():
    for user in PlayerData.objects:
        print(f"Upgrading user: {user.name}")
        upgrade_user_record(user)
        populate_x_y_coordinates(user)
        user.save(cascade=True)


upgrade_all_users()


@app.route('/')
def hello_world():
    if current_user.is_authenticated and not current_user.is_anonymous:
        return render_template('map.html')
    else:
        print('User not logged in. Redirecting to /login')
        logout_user()
        session.clear()
        return redirect('/login')  # render_template('login.html')


@app.route('/marker', methods=['PUT', 'POST'])
@login_required
def add_marker():
    try:
        heading = float(request.form['heading'])
        distance = int(request.form['distance'])
        depth = int(request.form['depth'])
        marker_name = request.form['name']

        marker_type_name = request.form['marker_type']
        try:
            color = request.form['color']
        except KeyError:
            color = '555555'

        x, y = Charting.get_cartesean_coords(distance, depth, heading)

        new_marker = Marker(bearing=heading, distance=distance, depth=depth, name=marker_name, marker_type_name=marker_type_name, color=color, x=x, y=y)
        current_user.map_data.append(new_marker)
        current_user.save(cascade=True)

    except KeyError:
        abort(400, description="Missing value - please make sure to fill in all fields")
    except ValueError:
        print('Bad form data in request: ', request.form)
        abort(400, description="Bad value - please use integers in all numeric fields")

    flash("Marker added")
    return redirect('/map')


@app.route(rule='/mapdata', methods=['GET'])
@login_required
def output_map_data():
    return jsonify(Charting.get_plot_data(current_user.map_data))


# When querying non-map user data, use partial querying:
# https://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields
# Film(title='The Shawshank Redemption', year=1994, rating=5).save()
# f = Film.objects.only('title').first()

@app.route(rule='/map', methods=['GET'])
@login_required
def generate_map():
    return render_template('map.html', markers=Charting.get_plot_data(current_user.map_data))


@app.route('/login', methods=['GET', 'POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = PlayerData.load_player(form.username.data)
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('index'))
    # return render_template('login.html', title='Sign In', form=form)


@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500, "State does not match!  Session: " + session["state"] + " , Request: " + request.args["state"])

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=subnautical.GOOGLE_CLIENT_ID
    )

    player_id = id_info['sub']

    try:
        player = load_player_from_db(player_id)
        print(f"Callback: trying to load {player_id} resulted in: ", repr(player))
        login_user(player, force=True)
    except DoesNotExist:
        print(f"Callback: trying to load {player_id} threw DoesNotExist. Creating new document for: {id_info['name']}")

        player = PlayerData(
            id=player_id,
            name=id_info['name'],
            email=id_info['email'],
            profile_pic=id_info['picture'],
            email_verified=id_info['email_verified'],
            map_data=init_map_data(),
        )
        player.validate()
        PlayerData.save_player(player)

        login_user(player, force=True)

    return redirect('/')


@login_required
@app.route('/protected_area')
def protected_area():
    return f"Hello {session}! <br/> <a href='/logout'><button>Logout</button></a>"


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect("/")


@login_manager.user_loader
def load_player_from_db(player_id):
    player = PlayerData.load_player(player_id)
    print(f"load_player_from_db retrieved {player.name}")
    return player


with app.app_context():
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid"],
        redirect_uri=url_for('callback'),
        )


if __name__ == '__main__':
    print(f"Starting app on host={subnautical.app_host}, port={subnautical.app_port}")
    app.run(host=subnautical.app_host, port=subnautical.app_port, debug=False)

