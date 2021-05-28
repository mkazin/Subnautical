import flask_mongoengine.connection
from flask import Flask, send_file, request, jsonify
from flask_mongoengine import MongoEngine

# flask_mongoengine.connection.create_connections()
# from pymongo import MongoClient
# from flask_pymongo import PyMongo
import ssl
import certifi
print(certifi.where())

import subnautical
from subnautica.model.map_data import MapData, Marker #, MarkerType
from subnautica.model.player_data import PlayerData
from subnautica.controller.charting import Charting
# from subnautica.utilities.database import db

def rebuild_my_database():
    map_data = MapData()
    map_data.add(Marker(name='Lifepod', bearing=0, distance=0, depth=0,  marker_type=Marker.MARKER_LIFEPOD))
    map_data.add(Marker(name='Vent Garden Hab', bearing=345, distance=1280, depth=336,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Mercury 2', bearing=336, distance=1407, depth=223,  marker_type=Marker.MARKER_OTHER))
    map_data.add(Marker(name='Seamonkey Habitat', bearing=330, distance=1262, depth=232,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Maida''s Habitat', bearing=335, distance=1088, depth=375,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Benzene Habitat', bearing=322.5, distance=1382, depth=610,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Greenhouse Habitat', bearing=310, distance=1521, depth=221,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Maida''s Greenhouse? Outpost Zero?', bearing=310, distance=1607, depth=0,  marker_type=Marker.MARKER_ALTERA))
    map_data.add(Marker(name='Shipwreck Habitat', bearing=335, distance=1012, depth=95,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Δ - Delta Landing', bearing=345, distance=634, depth=0,  marker_type=Marker.MARKER_ALTERA))
    # map_data.add(Marker(name='Φ - Phi Robotics Lab', bearing=, distance=, depth=0,  marker_type=Marker.MARKER_ALTERA))
    map_data.add(Marker(name=' - Outpost Zero', bearing=225, distance=380, depth=0,  marker_type=Marker.MARKER_ALTERA))
    # map_data.add(Marker(name='Ϙ - Koppa Mining Site', bearing=, distance=, depth=,  marker_type=Marker.))
    map_data.add(Marker(name='Ω - Omega Lab', bearing=322.5, distance=1422, depth=200,  marker_type=Marker.MARKER_ALTERA))
    map_data.add(Marker(name='Shallows Base', bearing=345, distance=235, depth=5,  marker_type=Marker.MARKER_HABITAT))
    map_data.add(Marker(name='Crash Site', bearing=187, distance=235, depth=0,  marker_type=Marker.MARKER_ALTERA))
    map_data.add(Marker(name='Kelp Forest', bearing=90, distance=265, depth=30,  marker_type=Marker.MARKER_ALTERA)) # TODO: switch to BIOME
    # map_data.add(Marker(name='', bearing=, distance=, depth=,  marker_type=Marker.))
    # map_data.add(Marker(name='', bearing=, distance=, depth=,  marker_type=Marker.))
    # map_data.add(Marker(name='', bearing=, distance=, depth=,  marker_type=Marker.))

    # player_data = PlayerData(player_id="me", map_data=map_data, marker_colors=None)
    data = PlayerData(name="me", map_data=map_data)  #, marker_colors=None)

    return data


# TODO: OAuth Authentication - https://realpython.com/flask-google-login/

app = Flask(__name__)
print(app.config)
print(subnautical.config)
app.config.from_object('subnautical.config')
print(app.config)
app.config['MONGODB_SETTINGS'] = subnautical.config
# print(app.config.from_pyfile('subnautical.py'))
print(app.config)
# db = MongoEngine(app)
# print(db.config)
app.config['MONGODB_SETTINGS']['connectTimeoutMS'] = 200
app.config['MONGODB_SETTINGS']['tlsCAFile'] = certifi.where()
print(app.config)

db = MongoEngine(app, app.config)
# db.connect(subnautical.database, connectTimeoutMS=200, tlsCAFile=certifi.where())
print(db.config)
# print(db.connection)

# client = MongoClient(subnautical.config['host'], connectTimeoutMS=200, tlsCAFile=certifi.where())
# print(client.stats)
# print(client.stats.ssl)
# client.stats.ssl = False
# print(client.stats)
# print(client.list_database_names())

# player_data = rebuild_my_database()


@app.route('/')
def hello_world():
    return 'Hello World 2!'


@app.route('/register')
def register_player():

    # bearing = float(request.form['bearing'])
    # distance = int(request.form['distance'])
    player = PlayerData(name="Test Player", map_data=MapData())
    player.save()  # Performs an insert
    return f"Player {player.name} Registered"


@app.route('/marker', methods=['PUT'])
def add_marker():
    bearing = float(request.form['bearing'])
    distance = int(request.form['distance'])
    depth = int(request.form['depth'])
    marker_name = int(request.form['name'])
    marker_type = int(request.form['marker_type'])

    new_marker = Marker(bearing, distance, depth, marker_name, marker_type)

    PlayerData.map_data.update(push__markers=new_marker)

    # new_marker.save()
    return "Coordinate added"


@app.route(rule='/mapdata', methods=['GET'])
def output_map_data():
    return jsonify(Charting.get_plot_data(player_markers))


# When querying non-map user data, use partial querying:
# https://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields
# Film(title='The Shawshank Redemption', year=1994, rating=5).save()
# f = Film.objects.only('title').first()

@app.route(rule='/map', methods=['GET'])
def generate_map():

    # TODO: cache the map until the map data actually changes
    return send_file(Charting.generate_map(player_markers))


if __name__ == '__main__':
    app.run()
