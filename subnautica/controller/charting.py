from copy import copy
import matplotlib as mpl
# Note: Agg is the Rendering backend needed on repl.it; You may need to use a different one.
mpl.use('Agg')
import matplotlib.pyplot as plt

from subnautica.utilities.geometry import geographical_distance, pol2cart # reverse_bearing
from subnautica.model.map_data import Marker  # , CoordinateType


class Charting(object):
    @staticmethod
    def generate_map(mapdata):
        Charting.plot_cartesian(mapdata)
        return 'graph-cartesian.png'
        # for marker in mapdata.markers:
        #     marker.bearing

    @staticmethod
    def plot_polar(data):
        """ Plot a Cartesian map using the given data """
        fig, ax = plt.subplots()

        ax = fig.add_subplot(111, projection='polar')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        theta_array = []
        r_array = []
        size_array = []
        color_array = []

        for mark in data:

            if mark['type'] not in Marker.MARKER_TYPES:
                # print('Skipping ', mark['type']['name']) # , '\n\tNot in: ', MARKER_TYPES)
                continue

            theta_array.append(mark['bearing'])
            r_array.append(mark['distance'])
            size_array.append(mark['type']['size'])
            color_array.append(mark['type']['color'])

            ax.annotate(mark['name'],
                        xy=(mark['bearing'], mark['distance']),
                        xytext=(mark['bearing'], mark['distance']),  # 0.05, 0.05),
                        horizontalalignment='left',
                        verticalalignment='bottom')

        ax.scatter(theta_array, r_array, size_array, c=color_array)

        rticks = [i * 100 for i in range(0, 12)]
        ax.set_rticks(rticks)
        ax.grid(True)
        #  ax.legend()
        fig.savefig('graph-polar.png')

    @staticmethod
    def get_plot_data(data):
        output = []
        for mark in data.markers:
            tunnel_distance = mark.distance
            try:
                surface_distance = geographical_distance(
                    tunnel_distance=tunnel_distance, depth=mark.depth)
            except KeyError:
                print('Warning: missing depth on marker: {0}'.format(mark))
                surface_distance = tunnel_distance

            # Convert polar coordinate information to Cartesean coordinates (x, y)
            x, y = pol2cart(surface_distance, mark.bearing)
            output_marker = copy(mark.__dict__)
            # output_marker.x = x
            # output_marker.y = y
            output_marker['x'] = x
            output_marker['y'] = y
            # output_marker = MarkerEncoder().encode(mark)
            print(output_marker)
            output.append(output_marker)
        return output

    @staticmethod
    def plot_cartesian(data):

        fig, ax = plt.subplots()

        for marker_type in Marker.MARKER_TYPES:

            x_array = []
            y_array = []
            color_array = []
            size_array = []
            label_array = []

            for mark in data.markers:
                if mark.marker_type is not marker_type:
                    continue

                # Convert tunnel distance (3D point-to-point) to surface distance (2D from points at sea level) for projection on a 2D map
                tunnel_distance = mark.distance
                try:
                    depth = mark.depth

                    # if depth > 0 and depth < 800:
                    #   continue

                    surface_distance = geographical_distance(
                        tunnel_distance=tunnel_distance, depth=depth)
                except KeyError:
                    print('Warning: missing depth on marker: {0}'.format(mark))
                    surface_distance = tunnel_distance

                # Convert polar coordinate information to Cartesean coordinates (x, y)
                x, y = pol2cart(surface_distance, mark.bearing)

                x_array.append(x)
                y_array.append(y)
                color_array.append(marker_type['color'])
                size_array.append(marker_type['size'])
                label_array.append(marker_type['name'])

                if mark.marker_type in [Marker.MARKER_EXPLORE, Marker.MARKER_RESOURCE]:
                    annotation = '{0}: {1}'.format(mark.marker_type['name'], mark.marker_name)
                elif mark.marker_type is Marker.MARKER_WRECK:
                    annotation = 'W'
                else:
                    annotation = mark.name

                ax.annotate(annotation,
                            xy=(x, y),
                            xytext=(x, y),  # 0.05, 0.05),
                            horizontalalignment='left',
                            verticalalignment='bottom')

            ax.scatter(x_array, y_array, size_array, c=color_array, label=marker_type['name'])

        #  rticks = [i * 100 for i in range(0, 12)]
        #  ax.set_rticks(rticks)
        ax.grid(True)
        ax.legend()
        fig.savefig('graph-cartesian.png', dpi=199)

    @staticmethod
    def plot_unit_circle():
        """
        Method to test bearing & polar coordinate transformations
        Expected result is for this data to draw the Unit circle (at r = 500m) of markers
        """
        MARKER_WAYPOINT = {'name': 'Waypoint', 'color': '#70707F', 'polarcolor': 200, 'size': 250}
        MARKER_TYPES.append(MARKER_WAYPOINT)
        test_data = [{'bearing': 0, 'distance': 500, 'name': '0 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 90, 'distance': 500, 'name': '90 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 180, 'distance': 500, 'name': '180 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 270, 'distance': 500, 'name': '270 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 45, 'distance': 500, 'name': '45 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 135, 'distance': 500, 'name': '135 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 225, 'distance': 500, 'name': '225 deg at 500', 'type': MARKER_WAYPOINT},
                     {'bearing': 315, 'distance': 500, 'name': '315 deg at 500', 'type': MARKER_WAYPOINT}]
        plot_cartesian(test_data)
        # plot_polar(test_data)

    # plot_polar(data)
    # plot_cartesian(data)
    # plot_unit_circle()
