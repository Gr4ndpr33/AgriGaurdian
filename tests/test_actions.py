
import unittest

from actions import (
    decide_actions,
    validate_action,
    execute_simulated_action,
)


class TestAgroGuardianActions(unittest.TestCase):

    def setUp(self):
        self.readings = {
            "soil_moisture": 20,
            "water_level": 80,
            "temperature": 25,
        }

    def test_dry_soil_proposes_irrigation(self):
        actions = decide_actions(self.readings)

        self.assertEqual(actions[0]["action"], "IRRIGATE")

    def test_high_pest_risk_proposes_alert(self):
        pest_result = {"risk_level": "HIGH"}

        actions = decide_actions(
            self.readings,
            pest_result=pest_result,
        )

        names = [item["action"] for item in actions]
        self.assertIn("ALERT_OPERATOR", names)

    def test_return_to_station_takes_priority(self):
        power_result = {"mode": "RETURN_TO_STATION"}

        actions = decide_actions(
            self.readings,
            power_result=power_result,
        )

        self.assertEqual(
            actions,
            [{
                "action": "RETURN_TO_STATION",
                "reason": "Power manager requires the rover to return.",
            }],
        )

    def test_unknown_action_is_rejected(self):
        result = validate_action({
            "action": "DISPENSE_CHEMICAL",
            "reason": "Test action",
        })

        self.assertFalse(result["approved"])

    def test_valid_action_is_approved(self):
        result = validate_action({
            "action": "MONITOR",
            "reason": "Routine monitoring",
        })

        self.assertTrue(result["approved"])

    def test_execution_is_simulated(self):
        result = execute_simulated_action({
            "action": "MONITOR",
            "reason": "Routine monitoring",
        })

        self.assertTrue(result["executed"])
        self.assertIn("SIMULATION ONLY", result["message"])

    def test_unknown_action_cannot_execute(self):
        result = execute_simulated_action({
            "action": "UNSAFE_ACTION",
            "reason": "Test",
        })

        self.assertFalse(result["executed"])


if __name__ == "__main__":
    unittest.main()
