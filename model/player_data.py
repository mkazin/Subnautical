from mongoengine import *
# import datetime
from .map_data import Marker, MapData

# class Page(Document):
#     title = StringField(max_length=200, required=True)
#     date_modified = DateTimeField(default=datetime.datetime.utcnow)


class PlayerData(Document):

    _id = ObjectIdField()
    name = StringField()
    # map_data = EmbeddedDocumentField(MapData)
    map_data = ListField(EmbeddedDocumentField(Marker))
    # marker_colors = ListField(EmbeddedDocumentField(???))

    # def __init__(self, player_id, map_data, marker_colors=None):
    #     self.player_id = player_id
    #     self.map_data = map_data
    #     # self.marker_colors = marker_colors

