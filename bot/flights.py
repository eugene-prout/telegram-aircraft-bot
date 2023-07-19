from dataclasses import dataclass
import random
from typing import Optional

from FlightRadar24 import FlightRadar24API, Flight
from bot.coordinates import get_bearing, haversine_distance


fr_api = FlightRadar24API()


@dataclass
class FlightObservation:
    heading: float
    origin: str
    destination: str
    relative_angle: float
    ground_distance: float
    aircraft: str
    photo: Optional[str]


def get_flights_in_box(
    top_left_box: tuple[float, float], bottom_right_box: tuple[float, float]
):
    box = fr_api.get_bounds(
        {
            "tl_x": top_left_box[1],
            "tl_y": top_left_box[0],
            "br_x": bottom_right_box[1],
            "br_y": bottom_right_box[0],
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
        photo = random.choice(flight.aircraft_images["medium"])["src"]

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
    )


def create_flight_observations(flights: list[Flight], user_pos: tuple[float, float]):
    return [create_flight_observation(f, user_pos) for f in flights]
