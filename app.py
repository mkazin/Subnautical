# import flask_mongoengine.connection
from flask import Flask, send_file, request, jsonify, render_template
from flask_mongoengine import MongoEngine

# flask_mongoengine.connection.create_connections()
# from pymongo import MongoClient
# from flask_pymongo import PyMongo
import certifi

import subnautical
from model.map_data import MapData, Marker, MarkerType
from model.player_data import PlayerData
from controller.charting import Charting
# from utilities.database import col

def rebuild_my_database():
    # map_data = MapData()
    map_data = []
    map_data.append(Marker(name='Lifepod', bearing=0, distance=0, depth=0,  marker_type=MarkerType.LIFEPOD))
    map_data.append(Marker(name='Vent Garden Hab', bearing=345, distance=1280, depth=336,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Mercury 2', bearing=336, distance=1407, depth=223,  marker_type=MarkerType.RESOURCE))
    map_data.append(Marker(name='Seamonkey Habitat', bearing=330, distance=1262, depth=232,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Maida''s Habitat', bearing=335, distance=1088, depth=375,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Benzene Habitat', bearing=322.5, distance=1382, depth=610,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Greenhouse Habitat', bearing=310, distance=1521, depth=221,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Maida''s Greenhouse? Outpost Zero?', bearing=310, distance=1607, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Shipwreck Habitat', bearing=335, distance=1012, depth=95,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Δ - Delta Landing', bearing=345, distance=634, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Φ - Phi Robotics Lab', bearing=50, distance=1100, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name=' - Outpost Zero', bearing=225, distance=380, depth=0,  marker_type=MarkerType.ALTERA))
    # map_data.append(Marker(name='Ϙ - Koppa Mining Site', bearing=, distance=, depth=,  marker_type=MarkerType.))
    map_data.append(Marker(name='Ω - Omega Lab', bearing=322.5, distance=1422, depth=200,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Shallows Base', bearing=345, distance=235, depth=5,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Crash Site', bearing=187, distance=235, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Kelp Forest', bearing=90, distance=265, depth=30,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Fragments Habitat', bearing=48, distance=272, depth=35,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Penglingwatch', bearing=85, distance=1453, depth=0,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Titanium Dig Site', bearing=75, distance=1053, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Hydraulic Bridge', bearing=67.5, distance=837, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Ore Tunnel Habitat', bearing=90, distance=964, depth=0,  marker_type=MarkerType.HABITAT))
    map_data.append(Marker(name='Spires Entrance', bearing=80, distance=832, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Architect Cable Tunnel', bearing=85, distance=847, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Architect Cable Passage', bearing=95, distance=1050, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Pengling Harvest', bearing=97.5, distance=1019, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Ion Cube Nodes', bearing=97.5, distance=1091, depth=0,  marker_type=MarkerType.RESOURCE))
    map_data.append(Marker(name='Spires Frozen Waterfall', bearing=105, distance=936, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Spires Northern Passage', bearing=98, distance=822, depth=0,  marker_type=MarkerType.ZONE))  # THIS IS WHERE THE PRIMARY TELEPORTER IS LOCATED
    map_data.append(Marker(name='Spires Architect Cache', bearing=135, distance=978, depth=0,  marker_type=MarkerType.ALIEN_SITE))
    map_data.append(Marker(name='Ice Worm Graveyard', bearing=125, distance=870, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Ice Worm Carcass', bearing=125, distance=784, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Ore Tunnel B', bearing=125, distance=943, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Spires Tall Waterfall', bearing=125, distance=1000, depth=0,  marker_type=MarkerType.ZONE))
    map_data.append(Marker(name='Architect Elevator Dock', bearing=90, distance=728, depth=0,  marker_type=MarkerType.ALTERA))
    map_data.append(Marker(name='Teleporter Tunnel', bearing=70, distance=725, depth=50,  marker_type=MarkerType.ZONE))
    # map_data.append(Marker(name='', bearing=, distance=, depth=0,  marker_type=MarkerType.))
    # map_data.append(Marker(name='', bearing=, distance=, depth=,  marker_type=MarkerType.))

    # player_data = PlayerData(player_id="me", map_data=map_data, marker_colors=None)
    # data = PlayerData(name="me", map_data=map_data)  #, marker_colors=None)
    # print(map_data.markers)
    return map_data


# TODO: OAuth Authentication - https://realpython.com/flask-google-login/

app = Flask(__name__)

app.static_folder = subnautical.app_config['ROOT_PATH'] + '/static'
app.template_folder = subnautical.app_config['ROOT_PATH'].split('controller')[0] + '/view/templates'
print(app.template_folder)

# print(app.config)
print(subnautical.config)
app.config.from_object('subnautical.config')
# print(app.config)
app.config['MONGODB_SETTINGS'] = subnautical.config
# print(app.config.from_pyfile('subnautical.py'))
# print(app.config)
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



@app.route('/')
def hello_world():
    return render_template('index.html')
    # return 'Hello World 2!'


@app.route('/register')
def register_player():

    # bearing = float(request.form['bearing'])
    # distance = int(request.form['distance'])
    map_data = rebuild_my_database()
    # print(map_data)
    player = PlayerData(name="Test Player", map_data=map_data)
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
    return generate_map()
    # player_data = PlayerData.objects(name='Test Player').first()
    # return render_template('map.html', markers=Charting.get_plot_data(player_data.map_data))
    # return jsonify(Charting.get_plot_data(player_markers))


# When querying non-map user data, use partial querying:
# https://docs.mongoengine.org/guide/querying.html#retrieving-a-subset-of-fields
# Film(title='The Shawshank Redemption', year=1994, rating=5).save()
# f = Film.objects.only('title').first()

@app.route(rule='/map', methods=['GET'])
def generate_map():

    player_data = PlayerData.objects(name='Test Player').first()
    return render_template('map.html', markers=Charting.get_plot_data(player_data.map_data))



if __name__ == '__main__':
    app.run()
