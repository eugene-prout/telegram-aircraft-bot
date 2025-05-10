from math import pi, sin

import plotly.graph_objects as go
import wikipedia

from tab.core.flights import create_flight_observation
from tab.core.geo_utils import create_bounding_box
from tab.core.models import BoundingBox, FlightObservation, LatLong
from tab.services import flight_api
from tab.services.models import AircraftInformationResponse, FlightResponse


def get_flights_near_user(current_pos: LatLong) -> FlightResponse:
    maximum_cardinal_distance_from_user = 30_000 * sin(pi / 4)
    users_bounding_box = create_bounding_box(
        current_pos, maximum_cardinal_distance_from_user
    )

    flights_near_user = flight_api.get_flights_in_bounding_box(users_bounding_box)

    observations = [
        create_flight_observation(f, current_pos) for f in flights_near_user
    ]

    figure = generate_map(current_pos, observations)
    radar_map = figure.to_image(format="png")

    return FlightResponse(observations, radar_map)


def generate_map(user_position: LatLong, flights: list[FlightObservation]) -> go.Figure:
    """
    Generates a figure cropped to the bounding box.
    """
    latitude_list = [f.aircraft_latitude for f in flights]
    longitude_list = [f.aircraft_longitude for f in flights]
    labels = [f.callsign for f in flights]
    angles = [f.heading for f in flights]

    # TODO: Markers / text are hidden when close together, so there may be fewer markers than observations. The relevant GitHub issue has been closed without a codefix. 
    fig = go.Figure(
        go.Scattermap(
            mode="markers+text",
            lon=longitude_list,
            lat=latitude_list,
            marker={"size": 10, "symbol": "airport", "angle": angles, "allowoverlap": True},
            text=labels,
            textposition="bottom right",
        )
    )

    fig.add_scattermap(
        mode="markers+text",
        lon=[user_position.longitude],
        lat=[user_position.latitude],
        marker={"size": 10, "symbol": "circle", "allowoverlap": True},
        text=["You"],
        textposition="bottom right",
    )

    # TODO: Using magic numbers to control the zoom isn't ideal. This should be refactored to use the bounding box to crop the map. 
    fig.update_layout(
        map={
            "style": "basic",
            "zoom": 9,
            "center": {
                "lon": user_position.longitude,
                "lat": user_position.latitude
            },
        },
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=False,
    )

    return fig


def get_aircraft_information(aircraft_name: str) -> AircraftInformationResponse:
    wikipedia_summary = wikipedia.summary(aircraft_name, auto_suggest=False, sentences=3)

    return AircraftInformationResponse(aircraft_name, wikipedia_summary)
