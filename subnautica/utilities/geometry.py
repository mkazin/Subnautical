import numpy as np


def reverse_bearing(bearing):
    """
    Bearing reversal calculation.
    Needed because bearing is taken by pointing self/Seamoth towards the player's Lifepod (origin)
    and recording (1) compass direction from the player to the Lifepod.
    Other data collected is (2) distance to Lifepod; and (3) depth
    """
    if bearing >= 180:
        return bearing - 180
    else:
        return bearing + 180


def geographical_distance(tunnel_distance, depth):
    """
      Calculates the distance as measured along the surface using
      distance taken in a bearing and depth.
      Since our map is 2D, we need to account for depth, which would otherwise make
      items appear farther away on the map than they actually are.
    """
    return int(np.sqrt((tunnel_distance * tunnel_distance) - (depth * depth)))


def pol2cart(r, bearing):
    """ Conversion of Polar coordinate to Cartesian.
    r - radius (or distance to origin)
    bearing - compass direction from current position to the origin point
    This is called "absolute bearing".
    For example, if y

    To read more start with:
    https://en.wikipedia.org/wiki/Bearing_(angle)
    """

    """
    Note that usually theta is measured against the X axis.
    However since I'm using True North as 0 degrees, we're actually
    measuring against the Y axis and so need to offset by 90 degrees. 
    """
    theta = (reverse_bearing(bearing) + 90) * 2 * np.pi / 360
    x = -(r * np.cos(theta))
    y = r * np.sin(theta)
    # print('Converted Bearing {0} degrees to Theta {1} radians at {2} m to ({3}, {4})'
    # .format(bearing, round(theta, 3), r, round(x, 3), round(y, 3)))
    return x, y
