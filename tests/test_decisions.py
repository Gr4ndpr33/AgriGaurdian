
import unittest

from safety import evaluate_irrigation
from power_manager import decide_power_mode


class TestAgroGuardianSafety(unittest.TestCase):

    def test_dry_soil_recommends_irrigation(self):
        readings = {
            "soil_moisture": 20,
            "water_level": 80,
            "temperature": 25,
        }

        result = evaluate_irrigation(readings)

        self.assertTrue(result["irrigate"])

    def test_low_water_tank_blocks_irrigation(self):
        readings = {
            "soil_moisture": 15,
            "water_level": 5,
            "temperature": 30,
        }

        result = evaluate_irrigation(readings)

        self.assertFalse(result["irrigate"])
        self.assertEqual(result["reason"], "Water tank too low.")

    def test_sufficient_soil_moisture(self):
        readings = {
            "soil_moisture": 60,
            "water_level": 80,
            "temperature": 25,
        }

        result = evaluate_irrigation(readings)

        self.assertFalse(result["irrigate"])


class TestAgroGuardianPower(unittest.TestCase):

    def test_low_battery_triggers_return(self):
        readings = {
            "battery_percent": 20,
            "solar_power_watts": 15,
            "distance_to_station": 100,
        }

        result = decide_power_mode(readings)

        self.assertEqual(result["mode"], "RETURN_TO_STATION")

    def test_strong_solar_output_uses_solar_assist(self):
        readings = {
            "battery_percent": 70,
            "solar_power_watts": 15,
            "distance_to_station": 100,
        }

        result = decide_power_mode(readings)

        self.assertEqual(result["mode"], "SOLAR_ASSIST")

    def test_low_solar_output_uses_battery(self):
        readings = {
            "battery_percent": 70,
            "solar_power_watts": 2,
            "distance_to_station": 100,
        }

        result = decide_power_mode(readings)

        self.assertEqual(result["mode"], "BATTERY")


    def test_low_battery_overrides_strong_solar(self):
        readings = {
            "battery_percent": 20,
            "solar_power_watts": 500,
            "distance_to_station": 100,
        }

        result = decide_power_mode(readings)

        self.assertEqual(result["mode"], "RETURN_TO_STATION")

    def test_battery_at_return_threshold_triggers_return(self):
        readings = {
            "battery_percent": 25,
            "solar_power_watts": 0,
            "distance_to_station": 100,
        }

        result = decide_power_mode(readings)

        self.assertEqual(result["mode"], "RETURN_TO_STATION")

    def test_high_battery_and_no_solar_uses_battery(self):
        readings = {
            "battery_percent": 80,
            "solar_power_watts": 0,
            "distance_to_station": 100,
        }

        result = decide_power_mode(readings)

        self.assertEqual(result["mode"], "BATTERY")

if __name__ == "__main__":
    unittest.main()