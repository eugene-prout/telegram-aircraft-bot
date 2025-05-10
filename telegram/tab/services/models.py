from dataclasses import dataclass

from tab.core.models import FlightObservation


@dataclass
class AircraftInformationResponse:
    name: str
    description: str


@dataclass
class FlightResponse:
    observations: list[FlightObservation]
    radar_map: bytes
