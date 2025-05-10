import random

from FlightRadar24 import Flight

from tab.core.geo_utils import get_bearing, haversine_distance
from tab.core.models import LatLong, FlightObservation


def create_flight_observation(flight: Flight, user_pos: LatLong) -> FlightObservation:
    angle = get_bearing(user_pos, LatLong(flight.latitude, flight.longitude))
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
            user_pos, LatLong(flight.latitude, flight.longitude)
        ),
        aircraft=flight.aircraft_model,
        photo=photo,
        aircraft_latitude=flight.latitude,
        aircraft_longitude=flight.longitude,
        callsign=flight.callsign,
    )
