def convert_bearing_to_cardinal(bearing: float):
    if bearing < 0:
        bearing += 360

    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]

    compass_lookup = round(bearing / 45)
    return compass_brackets[compass_lookup]
