# import flask_mongoengine.connection
import json
from flask import Flask, send_file, request, jsonify, render_template, abort, url_for
from flask_mongoengine import MongoEngine

# flask_mongoengine.connection.create_connections()
# from pymongo import MongoClient
# from flask_pymongo import PyMongo
import certifi

from config import config
from model.map_data import MapData, Marker, MarkerType
from model.player_data import PlayerData
from controller.charting import Charting
# from utilities.database import col


# To run this from PyCharm's Python Console prompt (which lets you hit ^C):
# > runfile('D:/Work/SubnauticaMap/app.py', wdir='D:/Work/SubnauticaMap')
def init_database():
    return [Marker(name='Lifepod', bearing=0, distance=0, depth=0,  marker_type=MarkerType.LIFEPOD)]

# TODO: OAuth Authentication - https://realpython.com/flask-google-login/


app = Flask(__name__)

app.static_folder = config.app_config['ROOT_PATH'] + '/static'
app.template_folder = config.app_config['ROOT_PATH'].split('controller')[0] + '/view/templates'
app.config.from_object('config.config')
app.config['MONGODB_SETTINGS'] = config.mongo
app.config['MONGODB_SETTINGS']['connectTimeoutMS'] = 200
app.config['MONGODB_SETTINGS']['tlsCAFile'] = certifi.where()
db = MongoEngine(app, app.config)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/register')
def register_player():
    map_data = init_database()
    player = PlayerData(name="Test Player", map_data=map_data)
    player.save()
    return f"Player {player.name} Registered"


@app.route('/marker', methods=['PUT', 'POST'])
def add_marker():
    error = None
    try:
        heading = float(request.form['heading'])
        distance = int(request.form['distance'])
        depth = int(request.form['depth'])
        marker_name = int(request.form['name'])
        marker_type = int(request.form['marker_type'])

        new_marker = Marker(heading, distance, depth, marker_name, marker_type)
        PlayerData.map_data.update(push__markers=new_marker)

    except KeyError:
        abort(400, description="Missing value - please make sure to fill in all fields")
    except ValueError:
        abort(400, description="Bad value - please use integers in all numeric fields")

    return "Marker added"


@app.route(rule='/mapdata', methods=['GET'])
def output_map_data():

    player_data = PlayerData.objects(name='Test Player').first()
    return jsonify(Charting.get_plot_data(player_data.map_data))


# When querying non-map user data, use partial querying:
# https://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields
# Film(title='The Shawshank Redemption', year=1994, rating=5).save()
# f = Film.objects.only('title').first()

@app.route(rule='/map', methods=['GET'])
def generate_map():

    player_data = PlayerData.objects(name='Test Player').first()
    return render_template('map.html', markers=Charting.get_plot_data(player_data.map_data))


if __name__ == '__main__':
    app.run(host=config.server['host'], port=config.server['port'], debug=False)

