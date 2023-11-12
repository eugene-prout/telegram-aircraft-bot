from dataclasses import dataclass
import math
from uuid import UUID
import plotly.express as px
import numpy
from math import sin, cos, sqrt, atan2, radians, cos, radians

from dataclasses import dataclass
import random
from typing import Optional

from FlightRadar24 import FlightRadar24API, Flight

from bot.types import BoundingBox, LatLong
import plotly.graph_objects as go


@dataclass
class FlightObservation:
    heading: float
    origin: str
    destination: str
    relative_angle: float
    ground_distance: float
    aircraft: str
    photo: Optional[str]
    flight: Optional[Flight]


def get_flights_near_user(current_pos: LatLong):
    users_bounding_box = create_bounding_box(current_pos)

    flights_near_user = get_flights_in_box(users_bounding_box)
    flights_near_user = load_flight_data(flights_near_user)

    observations = create_flight_observations(
        flights_near_user, (current_pos.latitude, current_pos.longitude)
    )

    figure = generate_base_map(users_bounding_box, observations)
    map = figure_as_bytes(figure)

    return observations, map


def get_bearing(lat1, long1, lat2, long2):
    dLon = long2 - long1
    x = cos(radians(lat2)) * sin(radians(dLon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(
        radians(lat2)
    ) * cos(radians(dLon))
    brng = numpy.arctan2(x, y)
    brng = numpy.degrees(brng)

    return brng


def convert_bearing_to_eight_point_cardinal(bearing: float):
    if bearing < 0:
        bearing += 360

    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]

    compass_lookup = round(bearing / 45)
    return compass_brackets[compass_lookup]


def convert_bearing_to_four_point_cardinal(bearing: float):
    if bearing < 0:
        bearing += 360

    compass_brackets = ["north", "east", "south", "west"]

    compass_lookup = round(bearing / 90) % 4

    return compass_brackets[compass_lookup]


def haversine_distance(p1: tuple[float, float], p2: tuple[float, float]):
    R = 6373.0  # Approximate radius of earth in km

    lat1, lon1 = radians(p1[0]), radians(p1[1])
    lat2, lon2 = radians(p2[0]), radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


@dataclass
class Boundaries:
    north: float
    east: float
    south: float
    west: float


def get_boundaries(box: BoundingBox):
    """
    Given a bounding box, return a list of boundaries such that they define the box.
    """
    return Boundaries(
        north=box.top_left.latitude,
        east=box.bottom_right.longitude,
        south=box.bottom_right.latitude,
        west=box.top_left.longitude,
    )


def add_flights_to_figure(fig, observations: list[FlightObservation]):
    new_latitude_list = [f.flight.latitude for f in observations]
    new_longitude_list = [f.flight.longitude for f in observations]
    labels = [f.flight.callsign for f in observations]
    print(labels)
    headings = [f.heading for f in observations]
    icons = [
        f"assets/plane_icons/{convert_bearing_to_four_point_cardinal(h)}.png"
        for h in headings
    ]

    fig.add_trace(
        px.scatter_mapbox(
            lat=new_latitude_list, lon=new_longitude_list, text=labels
        ).data[0]
    )

    return fig


def generate_base_map(box: BoundingBox, flights: list[FlightObservation]):
    """
    Generates a figure cropped to the bounding box.
    """
    latitude_list = [f.flight.latitude for f in flights]
    longitude_list = [f.flight.longitude for f in flights]
    labels = [f"{f.flight.callsign}-{f.aircraft}" for f in flights]
    markers = ["airport" for f in flights]

    fig = go.Figure(
        go.Scattermapbox(
            mode="markers+text",
            lon=longitude_list,
            lat=latitude_list,
            marker={"size": 10, "symbol": "airport"},
            text=labels,
            textposition="bottom right",
            textfont={"color": "white", "family": "Arial", "size": 16},
        )
    )

    boundaries = get_boundaries(box)

    # Zoom does nothing here as we are setting a fixed height, width and bounds
    fig.update_layout(
        mapbox={
            "accesstoken": "pk.eyJ1IjoiZXByb3V0IiwiYSI6ImNsb3ZwbTVrMDB0amMyaWxxbmw1dWJmbW8ifQ.reMtOM9cXG--eQLa2YHxLA",
            "style": "dark",
            "bounds": {
                "west": boundaries.west,
                "east": boundaries.east,
                "south": boundaries.south,
                "north": boundaries.north,
            },
        },
        height=800,
        width=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig


def figure_as_bytes(fig) -> bytes:
    return fig.to_image(format="png")


fr_api = FlightRadar24API()


def get_flights_in_box(bounding_box: BoundingBox):
    box = fr_api.get_bounds(
        {
            "tl_x": bounding_box.top_left.longitude,
            "tl_y": bounding_box.top_left.latitude,
            "br_x": bounding_box.bottom_right.longitude,
            "br_y": bounding_box.bottom_right.latitude,
        }
    )

    return fr_api.get_flights(bounds=box)


def load_flight_data(flights: list[Flight]):
    for f in flights:
        f.set_flight_details(fr_api.get_flight_details(f))
    return flights


def create_flight_observation(flight: Flight, user_pos: tuple[float, float]):
    angle = get_bearing(user_pos[0], user_pos[1], flight.latitude, flight.longitude)
    if flight.aircraft_images is None:
        photo = None
    else:
        try:
            photo = random.choice(flight.aircraft_images["medium"])["src"]
        except KeyError:
            # Maybe it's a helicopter?
            # Not sure the error cases here so need to have a think
            photo = flight.aircraft_images["sideview"]

    return FlightObservation(
        heading=flight.heading,
        origin=flight.origin_airport_name,
        destination=flight.destination_airport_name,
        relative_angle=angle,
        ground_distance=haversine_distance(
            (user_pos[0], user_pos[1]), (flight.latitude, flight.longitude)
        ),
        aircraft=flight.aircraft_model,
        photo=photo,
        flight=flight,
    )


def create_flight_observations(flights: list[Flight], user_pos: tuple[float, float]):
    return [create_flight_observation(f, user_pos) for f in flights]


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


def create_bounding_box(current_pos: LatLong, AREA=30_000 * math.sin(math.pi / 4)):
    """
    Given a LatLong pair, return the bounding box of size area from the position.
    Returns: (pos - area, pos + area), (pos + area, pos - area) to represent the top left, and top right
    """
    new_br = LatLong(
        *translate_latlong(current_pos.latitude, current_pos.longitude, -AREA, AREA)
    )
    new_bl = LatLong(
        *translate_latlong(current_pos.latitude, current_pos.longitude, -AREA, -AREA)
    )
    new_tl = LatLong(
        *translate_latlong(current_pos.latitude, current_pos.longitude, AREA, -AREA)
    )
    new_tr = LatLong(
        *translate_latlong(current_pos.latitude, current_pos.longitude, AREA, AREA)
    )

    return BoundingBox(new_tl, new_tr, new_bl, new_br)
