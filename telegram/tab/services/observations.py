from tab.core.models import LatLong
from tab.services import flight_api
from tab.services.models import AircraftInformationResponse, FlightResponse


async def get_flights_near_user(current_pos: LatLong) -> FlightResponse:
    observations, map = await flight_api.get_flights(current_pos)

    return FlightResponse(observations, map)


async def get_aircraft_information(aircraft_name: str) -> AircraftInformationResponse:
    name, description = await flight_api.get_aircraft_info(aircraft_name)

    return AircraftInformationResponse(name, description)
