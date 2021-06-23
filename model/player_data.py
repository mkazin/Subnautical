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
