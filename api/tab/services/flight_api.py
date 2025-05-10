from FlightRadar24 import Flight, FlightRadar24API

from tab.core.models import BoundingBox

fr_api = FlightRadar24API()


def get_flights_in_bounding_box(bounding_box: BoundingBox) -> list[Flight]:
    box = fr_api.get_bounds(
        {
            "tl_x": bounding_box.top_left.longitude,
            "tl_y": bounding_box.top_left.latitude,
            "br_x": bounding_box.bottom_right.longitude,
            "br_y": bounding_box.bottom_right.latitude,
        }
    )

    # TODO: map this to domain models.
    return fr_api.get_flights(bounds=box, details=True)
