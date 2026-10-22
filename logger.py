
import csv
from pathlib import Path

LOG_FILE = Path("agriguardian_log.csv")

FIELDS = [
    "timestamp",
    "soil_moisture",
    "temperature",
    "humidity",
    "water_level",
    "sunlight",
    "solar_power_watts",
    "battery_percent",
    "distance_to_station",
    "power_mode",
    "rover_status",
    "irrigation",
    "pests_observed",
    "plants_inspected",
    "plants_damaged",
    "pest_pressure_per_plant",
    "damage_percent",
    "pest_risk_level",
    "pest_alert",
]


def log_cycle(
    readings,
    power_mode,
    rover_status,
    irrigation,
    pest_result=None,
):
    """Save environmental and optional pest-monitoring data."""

    file_exists = LOG_FILE.exists()

    # Check whether an existing CSV uses the current schema.
    if file_exists and LOG_FILE.stat().st_size > 0:
        with LOG_FILE.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            existing_fields = next(csv.reader(file), [])

        if existing_fields != FIELDS:
            raise ValueError(
                "The existing CSV uses an older or different format. "
                "Back up agriguardian_log.csv, then rename or move it "
                "before restarting the simulation."
            )

    row = {
        "timestamp": readings["timestamp"],
        "soil_moisture": readings["soil_moisture"],
        "temperature": readings["temperature"],
        "humidity": readings["humidity"],
        "water_level": readings["water_level"],
        "sunlight": readings["sunlight"],
        "solar_power_watts": readings["solar_power_watts"],
        "battery_percent": readings["battery_percent"],
        "distance_to_station": readings["distance_to_station"],
        "power_mode": power_mode,
        "rover_status": rover_status,
        "irrigation": irrigation,
        "pests_observed": "",
        "plants_inspected": "",
        "plants_damaged": "",
        "pest_pressure_per_plant": "",
        "damage_percent": "",
        "pest_risk_level": "",
        "pest_alert": "",
    }

    if pest_result is not None:
        row.update({
            "pests_observed": readings.get("pests_observed", ""),
            "plants_inspected": readings.get("plants_inspected", ""),
            "plants_damaged": readings.get("plants_damaged", ""),
            "pest_pressure_per_plant": (
                pest_result["pest_pressure_per_plant"]
            ),
            "damage_percent": pest_result["damage_percent"],
            "pest_risk_level": pest_result["risk_level"],
            "pest_alert": pest_result["alert"],
        })

    with LOG_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if not file_exists or LOG_FILE.stat().st_size == 0:
            writer.writeheader()

        writer.writerow(row)


if __name__ == "__main__":
    print("AgriGuardian logger is ready.")
