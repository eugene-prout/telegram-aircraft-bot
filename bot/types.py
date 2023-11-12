from dataclasses import dataclass


@dataclass
class LatLong:
    latitude: float
    longitude: float


@dataclass
class BoundingBox:
    top_left: LatLong
    top_right: LatLong
    bottom_left: LatLong
    bottom_right: LatLong


@dataclass
class RepeatCallback:
    latitude: float
    longitude: float
