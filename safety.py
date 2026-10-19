
def evaluate_irrigation(readings):
    """
    Decide whether irrigation is safe and necessary.
    """

    soil_moisture = readings["soil_moisture"]
    water_level = readings["water_level"]
    temperature = readings["temperature"]

    # Safety checks first
    if water_level < 10:
        return {
            "irrigate": False,
            "reason": "Water tank too low."
        }

    # Irrigation decision
    if soil_moisture < 30:
        return {
            "irrigate": True,
            "reason": "Soil is dry; irrigation is recommended."
        }

    if temperature > 35 and soil_moisture < 40:
        return {
            "irrigate": True,
            "reason": "High temperature and relatively dry soil."
        }

    return {
        "irrigate": False,
        "reason": "Soil moisture is sufficient."
    }

def evaluate_irrigation(readings):
    """
    Decide whether irrigation is safe and necessary.
    """

    soil_moisture = readings["soil_moisture"]
    water_level = readings["water_level"]
    temperature = readings["temperature"]

    # Safety checks first
    if water_level < 10:
        return {
            "irrigate": False,
            "reason": "Water tank too low."
        }

    # Irrigation decision
    if soil_moisture < 30:
        return {
            "irrigate": True,
            "reason": "Soil is dry; irrigation is recommended."
        }

    if temperature > 35 and soil_moisture < 40:
        return {
            "irrigate": True,
            "reason": "High temperature and relatively dry soil."
        }

    return {
        "irrigate": False,
        "reason": "Soil moisture is sufficient."
    }
if __name__ == "__main__":
    test_readings = {
        "soil_moisture": 20,
        "water_level": 80,
        "temperature": 32
    }

    print(evaluate_irrigation(test_readings))