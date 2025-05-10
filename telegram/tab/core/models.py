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
