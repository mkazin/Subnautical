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
    marker_type = EnumField(MarkerType)
    x = IntField()
    y = IntField()
    # DecimalField(min_value=-2000.00, max_value=2000.0, force_string=False, precision=2, rounding='ROUND_HALF_UP')


# class MarkerType(EmbeddedDocument):
#     name = StringField()
#     color = StringField()
#     size = IntField()


# MARKER_LIFEPOD = {'name': 'Lifepod', 'color': '#907F00', 'polarcolor': 35, 'size': 120}
# MARKER_WRECK = {'name': 'Wreck', 'color': '#BBBBBB', 'polarcolor': 190, 'size': 90}
# MARKER_THERMAL = {'name': 'Thermal Vent', 'color': '#B83030', 'polarcolor': 55, 'size': 120}
# MARKER_HABITAT = {'name': 'Habitat', 'color': '#00FF00', 'polarcolor': 290, 'size': 150}
# MARKER_REAPER = {'name': 'REAPER', 'color': '#FF0000', 'polarcolor': 0, 'size': 120}
# MARKER_AURORA = {'name': 'Aurora', 'color': '#3030FF', 'polarcolor': 150, 'size': 180}
# MARKER_ALTERA = {'name': 'Altera', 'color': '#3030FF', 'polarcolor': 150, 'size': 180}
# MARKER_EXPLORE = {'name': 'Explore', 'color': '#000000', 'polarcolor': 0, 'size': 200}
# MARKER_RESOURCE = {'name': 'Resource', 'color': '#CCCC00', 'polarcolor': 0, 'size': 250}
# MARKER_ZONE = {'name': 'Zone Marker', 'color': '#00007F', 'polarcolor': 0, 'size': 250}
# MARKER_PEEP = {'name': 'Peep Vent', 'color': '#330033', 'polarcolor': 0, 'size': 250}
# MARKER_ARCH = {'name': 'Alien Arch', 'color': '#7FFF7F', 'polarcolor': 0, 'size': 250}
# MARKER_OTHER = {'name': 'Other', 'color': '#2F7FFF', 'polarcolor': 0, 'size': 250}

# MARKER_TYPES = [
#     MARKER_LIFEPOD,
#     MARKER_WRECK,
#     # MARKER_THERMAL,
#     MARKER_HABITAT,
#     MARKER_REAPER,
#     # MARKER_AURORA,
#     MARKER_ALTERA,
#     # MARKER_RESOURCE,
#     # MARKER_EXPLORE,
#     # MARKER_PEEP,
#     # MARKER_ARCH,
#     MARKER_OTHER,
#     MARKER_ZONE,
# ]
