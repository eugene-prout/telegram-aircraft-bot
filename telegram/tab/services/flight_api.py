import base64
import os
import httpx

from tab.core.models import FlightObservation, LatLong

API_BASE_URL = os.environ["API_URL"]

async def get_flights(position: LatLong) -> tuple[list[FlightObservation], bytes]:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/flights",
            json={"latitude": position.latitude, "longitude": position.longitude}
        )
        response.raise_for_status()
        parsed_response = response.json()

        observations = [
            FlightObservation(
                heading=obs["heading"],
                origin=obs["origin"],
                destination=obs["destination"],
                relative_angle=obs["relative_angle"],
                ground_distance=obs["ground_distance"],
                aircraft=obs["aircraft"],
                aircraft_latitude=obs["aircraft_latitude"],
                aircraft_longitude=obs["aircraft_longitude"],
                callsign=obs["callsign"],
                photo=obs.get("photo")
            )
            for obs in parsed_response["observations"]
        ]

        radar_map = base64.b64decode(parsed_response["radar_map"])

        return (observations, radar_map)


async def get_aircraft_info(aircraft_name: str) ->  tuple[str, str]:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{API_BASE_URL}/aircraft",
            json={"aircraft_name": aircraft_name}
        )
        response.raise_for_status()
        parsed_response = response.json()

        return (parsed_response["name"], parsed_response["description"])