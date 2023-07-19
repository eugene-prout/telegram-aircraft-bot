import plotly.express as px

import numpy
from math import sin, cos, sqrt, atan2, radians, cos, radians


def get_bearing(lat1, long1, lat2, long2):
    dLon = long2 - long1
    x = cos(radians(lat2)) * sin(radians(dLon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(
        radians(lat2)
    ) * cos(radians(dLon))
    brng = numpy.arctan2(x, y)
    brng = numpy.degrees(brng)

    return brng


def haversine_distance(p1: tuple[float, float], p2: tuple[float, float]):
    R = 6373.0  # Approximate radius of earth in km

    lat1, lon1 = radians(p1[0]), radians(p1[1])
    lat2, lon2 = radians(p2[0]), radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def plot_coords(positions_list: list[tuple[float, float]]):
    latitude_list = [pos[0] for pos in positions_list]
    longitude_list = [pos[1] for pos in positions_list]

    fig = px.scatter_mapbox(
        lat=latitude_list,
        lon=longitude_list,
        hover_name=range(len(positions_list)),
        zoom=8,
        height=800,
        width=800,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
