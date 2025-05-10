from dataclasses import dataclass
from typing import Optional


@dataclass
class FlightObservation:
    heading: float
    origin: str
    destination: str
    relative_angle: float
    ground_distance: float
    aircraft: str
    aircraft_latitude: float
    aircraft_longitude: float
    callsign: str
    photo: Optional[str]


@dataclass
class LatLong:
    latitude: float
    longitude: float


@dataclass
class Boundaries:
    north: float
    east: float
    south: float
    west: float


@dataclass
class BoundingBox:
    top_left: LatLong
    top_right: LatLong
    bottom_left: LatLong
    bottom_right: LatLong
