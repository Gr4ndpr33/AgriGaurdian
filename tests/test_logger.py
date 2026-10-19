
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from logger import log_cycle


class TestAgroGuardianLogger(unittest.TestCase):

    def test_log_cycle_writes_readings_to_csv(self):
        readings = {
            "timestamp": "2026-10-19T10:00:00",
            "soil_moisture": 25.0,
            "temperature": 30.0,
            "humidity": 60.0,
            "water_level": 80.0,
            "sunlight": 500.0,
            "solar_power_watts": 8.0,
            "battery_percent": 70.0,
            "distance_to_station": 100.0,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "test_log.csv"

            # Redirect the logger to a temporary CSV file
            with patch("logger.LOG_FILE", csv_path):
                log_cycle(
                    readings,
                    "SOLAR_ASSIST",
                    "FIELD",
                    True,
                )

            with csv_path.open(
                "r", newline="", encoding="utf-8"
            ) as file:
                rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["soil_moisture"], "25.0")
        self.assertEqual(rows[0]["power_mode"], "SOLAR_ASSIST")
        self.assertEqual(rows[0]["rover_status"], "FIELD")
        self.assertEqual(rows[0]["irrigation"], "True")


if __name__ == "__main__":
    unittest.main()
