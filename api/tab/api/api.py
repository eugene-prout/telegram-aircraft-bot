import base64
from fastapi import FastAPI
from tab.api.models import AircraftDescriptionRequest, AircraftInformationResponse, FlightObservationModel, FlightRequest, FlightsResponse
from tab.core.models import LatLong
from tab.services.observations import get_aircraft_information, get_flights_near_user

app = FastAPI()

@app.post("/flights")
async def post_flights(request: FlightRequest) -> FlightsResponse:
    data = get_flights_near_user(
        LatLong(request.latitude, request.longitude)
    )

    observations = []
    for obs in data.observations:
        observation = FlightObservationModel(
            heading=obs.heading,
            origin=obs.origin,
            destination=obs.destination,
            relative_angle=obs.relative_angle,
            ground_distance=obs.ground_distance,
            aircraft=obs.aircraft,
            aircraft_latitude=obs.aircraft_latitude,
            aircraft_longitude=obs.aircraft_longitude,
            callsign=obs.callsign,
            photo=obs.photo
        )
        observations.append(observation)

    response_model = FlightsResponse(
        observations=observations,
        radar_map=base64.b64encode(data.radar_map).decode("utf-8")
    )

    return response_model


@app.post("/aircraft")
async def post_aircraft(request: AircraftDescriptionRequest) -> AircraftInformationResponse:
    data = get_aircraft_information(request.aircraft_name)
    print(data)
    return AircraftInformationResponse(name=data.name, description=data.description)