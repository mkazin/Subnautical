from utilities.geometry import geographical_distance, pol2cart # reverse_bearing


class Charting(object):
    @staticmethod
    def get_plot_data(markers):
        output = []
        for mark in markers:
            tunnel_distance = mark.distance
            try:
                surface_distance = geographical_distance(
                    tunnel_distance=tunnel_distance, depth=mark.depth)
            except KeyError:
                print('Warning: missing depth on marker: {0}'.format(mark))
                surface_distance = tunnel_distance

            # Convert polar coordinate information to Cartesian coordinates (x, y)
            x, y = pol2cart(surface_distance, mark.bearing)
            marker = {'x': int(x), 'y': int(y), 'depth': int(mark.depth), 'name': mark.name, 'marker_type': str(mark.marker_type)}
            output.append(marker)
        return output
