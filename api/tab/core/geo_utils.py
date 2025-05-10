from math import atan2, cos, degrees, pi, radians, sin, sqrt

from tab.core.models import BoundingBox, LatLong


def get_bearing(from_position: LatLong, to_position: LatLong) -> float:
    dLon = to_position.longitude - from_position.longitude

    x = cos(radians(to_position.latitude)) * sin(radians(dLon))

    y = cos(radians(from_position.latitude)) * sin(radians(to_position.latitude)) - sin(
        radians(from_position.latitude)
    ) * cos(radians(to_position.latitude)) * cos(radians(dLon))

    bearing = atan2(x, y)

    return degrees(bearing)


def convert_bearing_to_eight_point_cardinal(bearing: float):
    if bearing < 0:
        bearing += 360

    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]

    compass_lookup = round(bearing / 45)
    return compass_brackets[compass_lookup]


def haversine_distance(p1: LatLong, p2: LatLong) -> float:
    """
    Calculates the distance between two points in kilometers.
    """
    R = 6373.0  # Approximate radius of earth in km

    lat1, lon1 = radians(p1.latitude), radians(p1.longitude)
    lat2, lon2 = radians(p2.latitude), radians(p2.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def translate_latlong(position: LatLong, latitude_delta, longitude_delta) -> LatLong:
    """
    Translates a position by the given delta. The delta is specified in meters.
    """
    EARTH_RADIUS_METERS = 6_371_000

    meters_per_degree_of_latitude = (2 * pi * EARTH_RADIUS_METERS) / 360
    meters_per_degree_of_longitude = meters_per_degree_of_latitude * cos(
        radians(position.latitude)
    )

    delta_lat_degrees = latitude_delta / meters_per_degree_of_latitude
    delta_lon_degrees = longitude_delta / meters_per_degree_of_longitude

    return LatLong(
        position.latitude + delta_lat_degrees, position.longitude + delta_lon_degrees
    )


def create_bounding_box(current_pos: LatLong, distance: float) -> BoundingBox:
    """
    Given a position, return the bounding box of the distance from the position in the four cardinal directions.
    """

    return BoundingBox(
        top_left=translate_latlong(current_pos, distance, -distance),
        top_right=translate_latlong(current_pos, distance, distance),
        bottom_left=translate_latlong(current_pos, -distance, -distance),
        bottom_right=translate_latlong(current_pos, -distance, distance),
    )
