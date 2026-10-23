
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from action_logger import log_action, AUDIT_FIELDS


class TestActionLogger(unittest.TestCase):

    def test_approved_action_is_logged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_path = Path(temp_dir) / "audit.csv"

            with patch("action_logger.AUDIT_FILE", audit_path):
                log_action(
                    {"action": "MONITOR", "reason": "Routine check"},
                    {"approved": True, "reason": "Action passed validation."},
                    {
                        "executed": True,
                        "message": "SIMULATION ONLY: MONITOR",
                    },
                )

            with audit_path.open(
                newline="", encoding="utf-8"
            ) as csv_file:
                rows = list(csv.DictReader(csv_file))

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["action"], "MONITOR")
            self.assertEqual(rows[0]["approved"], "True")
            self.assertEqual(rows[0]["executed"], "True")
            self.assertEqual(rows[0]["reason"], "Routine check")

    def test_rejected_action_is_logged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_path = Path(temp_dir) / "audit.csv"

            with patch("action_logger.AUDIT_FILE", audit_path):
                log_action(
                    {"action": "IRRIGATE", "reason": "Soil is dry"},
                    {
                        "approved": False,
                        "reason": "Water tank too low.",
                    },
                )

            with audit_path.open(
                newline="", encoding="utf-8"
            ) as csv_file:
                rows = list(csv.DictReader(csv_file))

            self.assertEqual(rows[0]["approved"], "False")
            self.assertEqual(rows[0]["executed"], "False")
            self.assertEqual(
                rows[0]["validation_reason"],
                "Water tank too low.",
            )

    def test_audit_has_expected_columns(self):
        self.assertIn("timestamp", AUDIT_FIELDS)
        self.assertIn("validation_reason", AUDIT_FIELDS)
        self.assertIn("execution_message", AUDIT_FIELDS)


if __name__ == "__main__":
    unittest.main()
