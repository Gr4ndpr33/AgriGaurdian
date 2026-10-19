
import random
from datetime import datetime


def read_sensors():
    """
    Simulate AgriGuardian's environmental and power sensors.
    """

    # Environmental sensors
    soil_moisture = round(random.uniform(10, 80), 1)
    temperature = round(random.uniform(15, 40), 1)
    humidity = round(random.uniform(20, 90), 1)
    water_level = round(random.uniform(0, 100), 1)

    # Power sensors (simulated)
    sunlight = round(random.uniform(0, 1000), 1)  # W/m²
    battery_percent = round(random.uniform(15, 100), 1)
    distance_to_station = round(random.uniform(0, 150), 1)  # metres

    # Two small solar panels mounted beside the camera
    total_panel_area = 0.08  # square metres, example design
    panel_efficiency = 0.20

    solar_power_watts = round(
        sunlight * total_panel_area * panel_efficiency, 2
    )

    readings = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "water_level": water_level,
        "sunlight": sunlight,
        "solar_power_watts": solar_power_watts,
        "battery_percent": battery_percent,
        "distance_to_station": distance_to_station,
    }

    return readings


if __name__ == "__main__":
    data = read_sensors()

    print("=== AgriGuardian Sensor Report ===")
    for sensor, value in data.items():
        print(f"{sensor}: {value}")

import random
from datetime import datetime


def read_sensors():
    """
    Simulate AgriGuardian's environmental and power sensors.
    """

    # Environmental sensors
    soil_moisture = round(random.uniform(10, 80), 1)
    temperature = round(random.uniform(15, 40), 1)
    humidity = round(random.uniform(20, 90), 1)
    water_level = round(random.uniform(0, 100), 1)

    # Power sensors (simulated)
    sunlight = round(random.uniform(0, 1000), 1)  # W/m²
    battery_percent = round(random.uniform(15, 100), 1)
    distance_to_station = round(random.uniform(0, 150), 1)  # metres

    # Two small solar panels mounted beside the camera
    total_panel_area = 0.08  # square metres, example design
    panel_efficiency = 0.20

    solar_power_watts = round(
        sunlight * total_panel_area * panel_efficiency, 2
    )

    readings = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "water_level": water_level,
        "sunlight": sunlight,
        "solar_power_watts": solar_power_watts,
        "battery_percent": battery_percent,
        "distance_to_station": distance_to_station,
    }

    return readings


if __name__ == "__main__":
    data = read_sensors()

    print("=== AgriGuardian Sensor Report ===")
    for sensor, value in data.items():
        print(f"{sensor}: {value}")
