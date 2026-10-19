
# AgriGuardian power-management settings

MIN_RETURN_THRESHOLD = 25.0
MAX_RETURN_THRESHOLD = 40.0
BASE_RETURN_RESERVE = 15.0
DISTANCE_RESERVE_FACTOR = 0.1
SOLAR_ASSIST_THRESHOLD = 8.0


def decide_power_mode(readings):
    """
    Select the rover's power mode.

    Returning to the charging station takes priority
    over using solar power for normal field activities.
    """

    battery = float(readings["battery_percent"])
    solar_power = float(readings["solar_power_watts"])
    distance = max(0.0, float(readings["distance_to_station"]))

    # Calculate a conservative battery threshold for returning.
    estimated_reserve = (
        BASE_RETURN_RESERVE
        + distance * DISTANCE_RESERVE_FACTOR
    )

    return_threshold = max(
        MIN_RETURN_THRESHOLD,
        min(estimated_reserve, MAX_RETURN_THRESHOLD),
    )

    # Safety takes priority over solar availability.
    if battery <= return_threshold:
        return {
            "mode": "RETURN_TO_STATION",
            "reason": (
                "Battery reserve is too low for normal tasks."
            ),
            "return_threshold": round(return_threshold, 1),
        }

    # Solar power can assist normal field operations.
    if solar_power >= SOLAR_ASSIST_THRESHOLD:
        return {
            "mode": "SOLAR_ASSIST",
            "reason": (
                "Solar output is sufficient to assist the battery."
            ),
            "return_threshold": round(return_threshold, 1),
        }

    # Otherwise, operate using stored battery energy.
    return {
        "mode": "BATTERY",
        "reason": (
            "Solar output is too low; use stored energy."
        ),
        "return_threshold": round(return_threshold, 1),
    }
