
def evaluate_pest_risk(readings):
    """
    Assess simulated crop pest activity and visible plant damage.

    The thresholds are for software demonstrations only,
    not real-world pesticide or treatment decisions.
    """
    required_fields = {
        "pests_observed",
        "plants_inspected",
        "plants_damaged",
    }

    missing_fields = required_fields - readings.keys()
    if missing_fields:
        raise ValueError(
            f"Missing required readings: {sorted(missing_fields)}"
        )

    pests_observed = readings["pests_observed"]
    plants_inspected = readings["plants_inspected"]
    plants_damaged = readings["plants_damaged"]

    # Validate counts.
    for name, value in (
        ("pests_observed", pests_observed),
        ("plants_inspected", plants_inspected),
        ("plants_damaged", plants_damaged),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be a whole number.")

        if value < 0:
            raise ValueError(f"{name} cannot be negative.")

    if plants_inspected == 0:
        raise ValueError("At least one plant must be inspected.")

    if plants_damaged > plants_inspected:
        raise ValueError(
            "Damaged plants cannot exceed plants inspected."
        )

    # Calculate simulated monitoring indicators.
    pest_pressure = pests_observed / plants_inspected
    damage_percent = (
        plants_damaged / plants_inspected
    ) * 100

    # Illustrative thresholds for the prototype.
    if damage_percent >= 25 or pest_pressure >= 1.0:
        risk_level = "HIGH"
        alert = True
        recommendation = (
            "Inspect the affected crop area promptly and "
            "identify the pest before choosing a response."
        )

    elif damage_percent >= 10 or pest_pressure >= 0.5:
        risk_level = "MODERATE"
        alert = True
        recommendation = (
            "Inspect more plants and monitor pest activity "
            "for changes."
        )

    else:
        risk_level = "LOW"
        alert = False
        recommendation = (
            "Continue routine crop scouting and record "
            "new observations."
        )

    return {
        "pest_pressure_per_plant": round(pest_pressure, 2),
        "damage_percent": round(damage_percent, 2),
        "risk_level": risk_level,
        "alert": alert,
        "recommendation": recommendation,
    }
