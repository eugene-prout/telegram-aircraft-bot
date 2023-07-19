import math


def translate_latlong(lat, long, lat_translation_meters, long_translation_meters):
    """method to move any lat,long point by provided meters in lat and long direction.
    params :
        lat,long: lattitude and longitude in degrees as decimal values, e.g. 37.43609517497065, -122.17226450150885
        lat_translation_meters: movement of point in meters in lattitude direction.
                                positive value: up move, negative value: down move
        long_translation_meters: movement of point in meters in longitude direction.
                                positive value: left move, negative value: right move
    """
    earth_radius = 6378.137

    # Calculate top, which is lat_translation_meters above
    m_lat = (1 / ((2 * math.pi / 360) * earth_radius)) / 1000
    lat_new = lat + (lat_translation_meters * m_lat)

    # Calculate right, which is long_translation_meters right
    m_long = (1 / ((2 * math.pi / 360) * earth_radius)) / 1000
    # 1 meter in degree
    long_new = long + (long_translation_meters * m_long) / math.cos(
        lat * (math.pi / 180)
    )

    return lat_new, long_new


def create_box(current_pos, AREA=30_000 * math.sin(math.pi / 4)):
    new_br = translate_latlong(current_pos[0], current_pos[1], -AREA, AREA)
    new_tl = translate_latlong(current_pos[0], current_pos[1], AREA, -AREA)
    return new_tl, new_br
