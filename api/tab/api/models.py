from typing import Optional
from pydantic import BaseModel


class FlightRequest(BaseModel):
    latitude: float
    longitude: float


class FlightObservationModel(BaseModel):
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


class FlightsResponse(BaseModel):
    observations: list[FlightObservationModel]
    radar_map: str


class AircraftDescriptionRequest(BaseModel):
    aircraft_name: str

class AircraftInformationResponse(BaseModel):
    name: str
    description: str
