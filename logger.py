
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
]


def log_cycle(readings, power_mode, rover_status, irrigation):
    """Save one AgriGuardian monitoring cycle to a CSV file."""

    file_exists = LOG_FILE.exists()

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
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
        })


if __name__ == "__main__":
    print("AgriGuardian logger is ready.")
