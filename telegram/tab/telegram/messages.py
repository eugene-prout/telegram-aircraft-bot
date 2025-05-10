from dataclasses import dataclass


@dataclass
class RepeatCallback:
    latitude: float
    longitude: float


@dataclass
class AircraftInformationCallback:
    name: str
