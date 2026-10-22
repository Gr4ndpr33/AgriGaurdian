
import unittest

from pest_monitor import evaluate_pest_risk


class TestAgriGuardianPestMonitor(unittest.TestCase):

    def test_high_crop_damage_triggers_alert(self):
        readings = {
            "pests_observed": 12,
            "plants_inspected": 20,
            "plants_damaged": 5,
        }

        result = evaluate_pest_risk(readings)

        self.assertEqual(result["risk_level"], "HIGH")
        self.assertTrue(result["alert"])
        self.assertEqual(result["damage_percent"], 25.0)

    def test_moderate_pest_pressure_triggers_alert(self):
        readings = {
            "pests_observed": 10,
            "plants_inspected": 20,
            "plants_damaged": 2,
        }


        result = evaluate_pest_risk(readings)

        self.assertEqual(result["risk_level"], "MODERATE")
        self.assertTrue(result["alert"])
        self.assertEqual(result["damage_percent"], 10.0)

    def test_low_pest_activity_does_not_trigger_alert(self):
        readings = {
            "pests_observed": 2,
            "plants_inspected": 20,
            "plants_damaged": 1,
        }

        result = evaluate_pest_risk(readings)

        self.assertEqual(result["risk_level"], "LOW")
        self.assertFalse(result["alert"])
        self.assertEqual(result["damage_percent"], 5.0)

    def test_zero_plants_inspected_is_rejected(self):
        readings = {
            "pests_observed": 0,
            "plants_inspected": 0,
            "plants_damaged": 0,
        }

        with self.assertRaises(ValueError):
            evaluate_pest_risk(readings)

    def test_damaged_plants_cannot_exceed_inspected(self):
        readings = {
            "pests_observed": 3,
            "plants_inspected": 10,
            "plants_damaged": 11,
        }

        with self.assertRaises(ValueError):
            evaluate_pest_risk(readings)

    def test_negative_pest_count_is_rejected(self):
        readings = {
            "pests_observed": -1,
            "plants_inspected": 10,
            "plants_damaged": 0,
        }

        with self.assertRaises(ValueError):
            evaluate_pest_risk(readings)

    def test_missing_reading_is_rejected(self):
        readings = {
            "pests_observed": 3,
            "plants_inspected": 10,
        }

        with self.assertRaises(ValueError):
            evaluate_pest_risk(readings)


if __name__ == "__main__":
    unittest.main()
