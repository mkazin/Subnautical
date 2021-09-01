from mongoengine import *
from enum import Enum


class MarkerType(Enum):
    # Consider ways to avoid spoilers in this dropdown
    UNKNOWN = 0
    LIFEPOD = 1
    HABITAT = 2
    ZONE = 3
    ALTERA = 4
    RESOURCE = 5
    DANGER = 6
    ALIEN_SITE = 7
    PORTAL = 8


class Marker(EmbeddedDocument):
    bearing = IntField()
    distance = IntField()
    depth = IntField()
    name = StringField()
    marker_type = EnumField(MarkerType, required=False)

    marker_type_name = StringField(required=False, db_field="type")
    color = StringField(required=False)

    x = IntField()
    y = IntField()


#
# class MapData(Document):
#     player_id = StringField(required=True, primary_key=True)
#     markers = EmbeddedDocumentListField(Marker, required=False, default=None)
#     map_data = EmbeddedDocumentListField(Marker, required=False, default=None)
#


