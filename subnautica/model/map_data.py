from mongoengine import *
from enum import Enum


class MarkerType(Enum):
    # Consider ways to avoid spoilers in this dropdown
    UNKNOWN = 0
    LIFEPOD = 1
    HABITAT = 2
    STORY_PLOT = 3
    RESOURCE = 4
    DANGER = 5
    ALIEN_SITE = 6
    PORTAL = 7


class Marker(EmbeddedDocument):
    bearing = IntField()
    distance = IntField()
    depth = IntField()
    name = StringField()
    marker_type = EnumField(MarkerType)
    x = IntField()
    y = IntField()
    # DecimalField(min_value=-2000.00, max_value=2000.0, force_string=False, precision=2, rounding='ROUND_HALF_UP')

    MARKER_LIFEPOD = {'name': 'Lifepod', 'color': '#907F00', 'polarcolor': 35, 'size': 120}
    MARKER_WRECK = {'name': 'Wreck', 'color': '#BBBBBB', 'polarcolor': 190, 'size': 90}
    MARKER_THERMAL = {'name': 'Thermal Vent', 'color': '#B83030', 'polarcolor': 55, 'size': 120}
    MARKER_HABITAT = {'name': 'Habitat', 'color': '#00FF00', 'polarcolor': 290, 'size': 150}
    MARKER_REAPER = {'name': 'REAPER', 'color': '#FF0000', 'polarcolor': 0, 'size': 120}
    MARKER_AURORA = {'name': 'Aurora', 'color': '#3030FF', 'polarcolor': 150, 'size': 180}
    MARKER_ALTERA = {'name': 'Altera', 'color': '#3030FF', 'polarcolor': 150, 'size': 180}
    MARKER_EXPLORE = {'name': 'Explore', 'color': '#000000', 'polarcolor': 0, 'size': 200}
    MARKER_RESOURCE = {'name': 'Resource', 'color': '#CCCC00', 'polarcolor': 0, 'size': 250}
    MARKER_ZONE = {'name': 'Zone Marker', 'color': '#00007F', 'polarcolor': 0, 'size': 250}
    MARKER_PEEP = {'name': 'Peep Vent', 'color': '#330033', 'polarcolor': 0, 'size': 250}
    MARKER_ARCH = {'name': 'Alien Arch', 'color': '#7FFF7F', 'polarcolor': 0, 'size': 250}
    MARKER_OTHER = {'name': 'Other', 'color': '#2F7FFF', 'polarcolor': 0, 'size': 250}

    MARKER_TYPES = [
        MARKER_LIFEPOD,
        MARKER_WRECK,
        # MARKER_THERMAL,
        MARKER_HABITAT,
        MARKER_REAPER,
        # MARKER_AURORA,
        MARKER_ALTERA,
        # MARKER_RESOURCE,
        # MARKER_EXPLORE,
        # MARKER_PEEP,
        # MARKER_ARCH
    ]

    # def __init__(self, bearing, distance, depth, name, marker_type=None):
    #     self.bearing = bearing
    #     self.distance = distance
    #     self.depth = depth
    #     self.name = name
    #     self.marker_type = marker_type if marker_type else Marker.MARKER_OTHER
    #     # self.x = None
    #     # self.y = None


class MapData(EmbeddedDocument):

    markers = ListField(EmbeddedDocumentField(Marker))
    # def __init__(self):
    #     self.markers = []

    def add(self, marker):
        self.markers.append(marker)

"""Old data from Repl.it

            data = []

            # Corrected bearing + has depth

            data.append(
                {'bearing': 225, 'distance': 1560, 'depth': 600, 'name': 'Sick Ray Habitat', 'type': MARKER_HABITAT})

            data.append(
                {'bearing': 235, 'distance': 1923, 'depth': 380, 'name': 'Northeast Habitat', 'type': MARKER_HABITAT})
            data.append({'bearing': 205, 'distance': 1436, 'depth': 750, 'name': 'Ghostwatch', 'type': MARKER_HABITAT})

            # Habitats
            data.append({'bearing': 184, 'distance': 1300, 'depth': 480, 'name': 'Northern Thermal Habitat',
                         'type': MARKER_HABITAT})
            data.append({'bearing': 160, 'distance': 1500, 'depth': 450, 'name': 'Nuclear Habitat',
                         'type': MARKER_HABITAT})  # Has Uraninite, Copper, Lead, Gold deposits
            data.append({'bearing': 145, 'distance': 1125, 'depth': 650, 'name': 'Fossilized Cave Habitat',
                         'type': MARKER_HABITAT})  # Has Everything! This sucker's nuclear!
            # data.append({'bearing': 145, 'distance': , 'depth': , 'name': 'Alien Base Habitat, 'type': MARKER_HABITAT}) # Thermal-powered
            data.append({'bearing': 330, 'distance': 655, 'depth': 15, 'name': 'Reaperwatch',
                         'type': MARKER_HABITAT})  # Bioreactor
            data.append({'bearing': 330, 'distance': 1180, 'depth': 256, 'name': 'Byte Habitat',
                         'type': MARKER_HABITAT})  # Bioreactor
            data.append({'bearing': 245, 'distance': 1967, 'depth': 350, 'name': 'Sharknest',
                         'type': MARKER_HABITAT})  # Bioreactor
            data.append({'bearing': 120, 'distance': 1380, 'depth': 1234, 'name': 'Lava River Habitat',
                         'type': MARKER_HABITAT})  # Thermal

            data.append({'bearing': 240, 'distance': 1337, 'depth': 1192, 'name': 'Lava Hidden Habitat',
                         'type': MARKER_HABITAT})  # Nuclear
            # data.append({'bearing': 240, 'distance': 1337, 'depth': 1192, 'name': 'Lava River Habitat', 'type': MARKER_HABITAT}) # Nuclear

            data.append({'bearing': 240, 'distance': 1500, 'depth': 200, 'name': 'NE Thermal Habitat',
                         'type': MARKER_HABITAT})  # Has Uraninite, Copper, Lead, Gold deposits, no Thermal reactor yet

            data.append({'bearing': 8, 'distance': 1580, 'depth': 400, 'name': 'Poop Factory',
                         'type': MARKER_HABITAT})  # Overlooks Treader stomping grounds.

            data.append({'bearing': 295, 'distance': 1450, 'depth': 1400, 'name': 'Alien Power Station',
                         'type': MARKER_EXPLORE})

            # Alien Arches
            data.append(
                {'bearing': 295, 'distance': 1450, 'depth': 1400, 'name': 'Alien Power Station', 'type': MARKER_ARCH})
            data.append({'bearing': 210, 'distance': 1112, 'depth': 0, 'name': 'Alien Arch - Primary?',
                         'type': MARKER_ARCH})  # powered, sends to Floating Island
            data.append({'bearing': 40, 'distance': 1081, 'depth': 0, 'name': 'Alien Arch - Floating Island',
                         'type': MARKER_ARCH})  # powered, sends to Alien Enforcement Platform

            data.append(
                {'bearing': 205, 'distance': 1600, 'depth': 165, 'name': 'Alien Arch - Enforcement Platform (in water)',
                 'type': MARKER_ARCH})  # powered, sends to Sea Emperor

            data.append({'bearing': 245, 'distance': 1717, 'depth': 300, 'name': 'Alien Arch - ???',
                         'type': MARKER_ARCH})  # Powered, connects to Alien Power Plant A
            data.append({'bearing': 125, 'distance': 892, 'depth': 225, 'name': 'Alien Arch - Mushroom Forest',
                         'type': MARKER_ARCH})  # Powered, connects to Alien Power Plant B
            data.append({'bearing': 225, 'distance': 1540, 'depth': 622, 'name': 'Alien Arch - Fossilized Cave',
                         'type': MARKER_ARCH})  # Powered, connects to Alien Power Plant C
            data.append({'bearing': 0, 'distance': 1275, 'depth': 292, 'name': 'Alien Arch - Crag Field',
                         'type': MARKER_ARCH})  # Powered, connects to Alien Power Plant D+

            # Lifepods
            data.append({'bearing': 163, 'distance': 1570, 'depth': 500, 'name': 'Lifepod 2', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 230, 'distance': 656, 'depth': 115, 'name': 'Lifepod 6',
                         'type': MARKER_LIFEPOD})  # 400m W-NW of lifepod 4
            data.append({'bearing': 355, 'distance': 940, 'depth': 180, 'name': 'Lifepod 7', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 125, 'distance': 1030, 'depth': 180, 'name': 'Lifepod 13', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 115, 'distance': 411, 'depth': 95, 'name': 'Lifepod 17', 'type': MARKER_LIFEPOD})

            # Caves
            data.append(
                {'bearing': 70, 'distance': 285, 'depth': 110, 'name': 'Jellyshroom Cave', 'type': MARKER_RESOURCE})

            # Wrecks
            data.append({'bearing': 115, 'distance': 530, 'depth': 85, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 80, 'distance': 430, 'depth': 105, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 70, 'distance': 365, 'depth': 100, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 60, 'distance': 362, 'depth': 100, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append(
                {'bearing': 155, 'distance': 1140, 'depth': 120, 'name': 'Wreck (on tree)', 'type': MARKER_WRECK})
            data.append({'bearing': 205, 'distance': 1595, 'depth': 215, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append(
                {'bearing': 240, 'distance': 567, 'depth': 110, 'name': 'Wreck + Sandstone cave', 'type': MARKER_WRECK})
            data.append({'bearing': 250, 'distance': 1587, 'depth': 215, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 325, 'distance': 510, 'depth': 100, 'name': 'Wreck', 'type': MARKER_EXPLORE})

            data.append({'bearing': 215, 'distance': 1595, 'depth': 370, 'name': 'Wreck',
                         'type': MARKER_WRECK})  # a little titanium left

            # Explore
            data.append(
                {'bearing': 320, 'distance': 425, 'depth': 265, 'name': 'Degasi Habitat & Magnetite + Gold to drill',
                 'type': MARKER_RESOURCE})  # NOTE: Cave entrance is on the SouthEast side of the cave's inside.

            data.append({'bearing': 0, 'distance': 1590, 'depth': 400, 'name': 'Treader Dancing Grounds',
                         'type': MARKER_EXPLORE})  # Resources

            data.append({'bearing': 255, 'distance': 1650, 'depth': 200,
                         'name': 'Fossilized Cave Trench Exit - everything, bring Cyclops',
                         'type': MARKER_RESOURCE})  #

            #

            # Alien Facilities - from Codes & Clues
            # data.append({'bearing': , 'distance': , 'depth': 800, 'name': 'Alien Base - Disease Research Facility', 'type': MARKER_EXPLORE}) # 800m deep within cave with Fossil Record, Southwest of "Enforcement Platform"
            # data.append({'bearing': , 'distance': , 'depth': 1000, 'name': 'Alien Base - Thermal Power Facility', 'type': MARKER_EXPLORE}) # Inside natural rock formation in are of volcanic activity( is that near one of my thermal bases?)
            data.append(
                {'bearing': 200, 'distance': 1125, 'depth': 0, 'name': 'Alien Base - Enforcement Platform (island)',
                 'type': MARKER_EXPLORE})

            #
            data.append(
                {'bearing': 225, 'distance': 1650, 'depth': 250, 'name': 'Thermal Vent', 'type': MARKER_THERMAL})

            # Zone mapping
            data.append({'bearing': 55, 'distance': 245, 'depth': 25, 'name': 'Kelp Forest', 'type': MARKER_ZONE})
            data.append({'bearing': 95, 'distance': 265, 'depth': 45, 'name': 'Kelp Forest', 'type': MARKER_ZONE})
            data.append({'bearing': 135, 'distance': 340, 'depth': 65, 'name': 'Kelp Forest', 'type': MARKER_ZONE})
            data.append({'bearing': 145, 'distance': 392, 'depth': 51, 'name': 'Kelp Forest', 'type': MARKER_ZONE})
            data.append({'bearing': 125, 'distance': 735, 'depth': 95, 'name': 'Kelp Forest', 'type': MARKER_ZONE})

            # Has depth, re-grab bearing
            data.append({'bearing': 255, 'distance': 1442, 'depth': 250, 'name': 'Lifepod 12', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 45, 'distance': 1065, 'depth': 300, 'name': 'Lifepod 19', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 15, 'distance': 740, 'depth': 230, 'name': 'Wreck (230m)', 'type': MARKER_WRECK})
            data.append({'bearing': 70, 'distance': 770, 'depth': 242, 'name': 'Fossilized Cave below + Blood Oil',
                         'type': MARKER_EXPLORE})
            data.append(
                {'bearing': 80, 'distance': 1121, 'depth': 500, 'name': 'Wrecked Habitat', 'type': MARKER_HABITAT})
            data.append(
                {'bearing': 120, 'distance': 331, 'depth': 280, 'name': 'Thermal Vent (280m)', 'type': MARKER_THERMAL})

            # Peep Vents
            data.append({'bearing': 215, 'distance': 1450, 'depth': 285, 'name': 'Peep Vent', 'type': MARKER_PEEP})

            # Missing depth and updated bearing:
            data.append({'bearing': 40, 'distance': 1567, 'depth': 405, 'name': 'Underwater Thermal Habitat',
                         'type': MARKER_HABITAT})

            data.append({'bearing': 195, 'distance': 535, 'name': 'Lifepod 3', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 240, 'distance': 876, 'name': 'Lifepod 4',
                         'type': MARKER_LIFEPOD})  # ~150m NW of Aurora port section
            data.append({'bearing': 0, 'distance': 0, 'name': 'Lifepod 5', 'type': MARKER_LIFEPOD})
            data.append({'bearing': 125, 'distance': 781, 'name': 'Lifepod 13', 'type': MARKER_LIFEPOD})

            data.append({'bearing': 125, 'distance': 619, 'name': 'Potential Harvest Havitat', 'type': MARKER_HABITAT})

            data.append({'bearing': 45, 'distance': 1742, 'name': 'Habitat', 'type': MARKER_HABITAT})

            data.append({'bearing': 60, 'distance': 1205, 'name': 'Wreck (big, possibly missed stuff!)',
                         'type': MARKER_EXPLORE})

            data.append(
                {'bearing': 70, 'distance': 730, 'name': 'Deep Shrooms + Blood Oil (190m)', 'type': MARKER_EXPLORE})

            data.append({'bearing': 45, 'distance': 800, 'name': 'Aerogel Cave', 'type': MARKER_HABITAT})
            data.append({'bearing': 70, 'distance': 625, 'name': 'Aerogel Habitat', 'type': MARKER_HABITAT})

            data.append({'bearing': 205, 'distance': 625, 'name': 'Main habitat', 'type': MARKER_HABITAT})
            # data.append({'bearing': , 'distance': , 'name': 'Lifepod habitat', 'type': MARKER_HABITAT})
            data.append({'bearing': 270, 'distance': 689, 'name': 'Aurora Habitat', 'type': MARKER_HABITAT})
            data.append({'bearing': 120, 'distance': 800, 'name': 'Westward Habitat', 'type': MARKER_HABITAT})
            data.append({'bearing': 345, 'distance': 300, 'name': 'Thermal Habitat', 'type': MARKER_HABITAT})

            data.append({'bearing': 315, 'distance': 617, 'name': 'Aurora Port Engine', 'type': MARKER_AURORA})

            data.append({'bearing': 240, 'distance': 1174, 'name': 'Aurora Entry', 'type': MARKER_AURORA})

            data.append({'bearing': 170, 'distance': 1415, 'name': 'Blood Oil', 'type': MARKER_RESOURCE})

            data.append({'bearing': 225, 'distance': 394, 'name': 'Thermal Cave', 'type': MARKER_THERMAL})
            data.append({'bearing': 255, 'distance': 1460, 'name': 'Thermal Vent', 'type': MARKER_THERMAL})
            data.append({'bearing': 345, 'distance': 314, 'name': 'Wreck + Thermal Vent', 'type': MARKER_THERMAL})

            data.append({'bearing': 110, 'distance': 880, 'name': 'DANGER: Reaper Leviathan', 'type': MARKER_REAPER})
            data.append({'bearing': 160, 'distance': 1803, 'name': 'DANGER: Ghost Leviathan', 'type': MARKER_REAPER})

            data.append({'bearing': 170, 'distance': 440, 'name': 'Wreck (some titanium)', 'type': MARKER_WRECK})
            data.append({'bearing': 320, 'distance': 330, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 110, 'distance': 421, 'name': 'Wreck + cave', 'type': MARKER_WRECK})
            data.append({'bearing': 290, 'distance': 319, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 285, 'distance': 515, 'name': 'Wreck', 'type': MARKER_WRECK})

            data.append({'bearing': 210, 'distance': 728, 'name': 'Wreck', 'type': MARKER_WRECK})
            data.append({'bearing': 180, 'distance': 1000, 'name': 'Wreck @ Floating Islands', 'type': MARKER_WRECK})
            data.append({'bearing': 235, 'distance': 1288, 'name': 'Wreck', 'type': MARKER_WRECK})

            # data.append({'bearing': , 'distance': , 'name': '', 'type': MARKER_})
            # data.append({'bearing': , 'distance': , 'name': '', 'type': MARKER_})
            # data.append({'bearing': , 'distance': , 'name': '', 'type': MARKER_})
            # data.append({'bearing': , 'distance': , 'name': '', 'type': MARKER_})
            # data.append({'bearing': , 'distance': , 'name': '', 'type': MARKER_})
            # data.append({'bearing': , 'distance': , 'name': '', 'type': MARKER_})


"""
