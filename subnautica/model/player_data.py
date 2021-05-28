from mongoengine import *
# import datetime
from .map_data import MapData

# class Page(Document):
#     title = StringField(max_length=200, required=True)
#     date_modified = DateTimeField(default=datetime.datetime.utcnow)


class PlayerData(Document):

    id = ObjectIdField()
    name = StringField()
    map_data = EmbeddedDocumentField(MapData)
    # marker_colors = ListField(EmbeddedDocumentField(???))

    # def __init__(self, player_id, map_data, marker_colors=None):
    #     self.player_id = player_id
    #     self.map_data = map_data
    #     # self.marker_colors = marker_colors

