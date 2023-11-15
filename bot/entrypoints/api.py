from quart import Quart, request

import json

from bot.entrypoints.AbstractEntrypoint import AbstractEntrypoint
from bot.services import GetAircraftInformation, GetFlights
from bot.types import LatLong

from marshmallow import Schema, ValidationError, fields


class AircraftDescriptionRequest(Schema):
    aircraft_name = fields.Str(required=True)


class FlightRequest(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


class APIEntrypoint(AbstractEntrypoint):
    def __init__(self):
        quart = Quart(__name__)

        quart.add_url_rule("/flights", view_func=get_flights, methods=["POST"])

        quart.add_url_rule(
            "/aircraft", view_func=get_aircraft_information, methods=["POST"]
        )

        self.app = quart

    def launch(self):
        self.app.run()


async def get_flights():
    user_data = await request.get_data()
    user_data = user_data.decode("utf-8")

    try:
        user_position = FlightRequest().loads(user_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    except json.decoder.JSONDecodeError:
        return {"error": "Invalid JSON"}, 400

    data = GetFlights(LatLong(user_position["latitude"], user_position["longitude"]))

    return data.as_json()


async def get_aircraft_information():
    user_data = await request.get_data()
    user_data = user_data.decode("utf-8")

    try:
        plane = AircraftDescriptionRequest().loads(user_data)
    except ValidationError as err:
        return {"error": err.messages}, 400
    except json.decoder.JSONDecodeError:
        return {"error": "Invalid JSON"}, 400

    data = GetAircraftInformation(plane["aircraft_name"])

    return data.as_json()
