
import unittest

from battery import Battery
from rover import Rover


class TestAgroGuardianBattery(unittest.TestCase):

    def test_battery_drops_when_consumption_exceeds_solar(self):
        battery = Battery(charge_percent=70)

        battery.update(
            solar_power_watts=0,
            consumption_watts=20,
            duration_seconds=60,
        )

        self.assertLess(battery.charge_percent, 70)

    def test_battery_increases_when_solar_exceeds_consumption(self):
        battery = Battery(charge_percent=50)

        battery.update(
            solar_power_watts=40,
            consumption_watts=10,
            duration_seconds=60,
        )

        self.assertGreater(battery.charge_percent, 50)

    def test_battery_never_exceeds_100_percent(self):
        battery = Battery(charge_percent=99)

        battery.update(
            solar_power_watts=1000,
            consumption_watts=0,
            duration_seconds=3600,
        )

        self.assertEqual(battery.charge_percent, 100)


class TestAgroGuardianRover(unittest.TestCase):

    def test_rover_reaches_station_after_multiple_returns(self):
        rover = Rover(distance_to_station=100)

        rover.return_to_station()
        self.assertEqual(rover.distance_to_station, 70)
        self.assertEqual(rover.status, "RETURNING")

        rover.return_to_station()
        self.assertEqual(rover.distance_to_station, 40)

        rover.return_to_station()
        self.assertEqual(rover.distance_to_station, 10)

        rover.return_to_station()
        self.assertEqual(rover.distance_to_station, 0)
        self.assertEqual(rover.status, "CHARGING")
        self.assertTrue(rover.is_at_station())

    def test_rover_becomes_ready_when_battery_is_full(self):
        rover = Rover(distance_to_station=0)
        battery = Battery(charge_percent=95)

        rover.recharge(battery)

        self.assertEqual(battery.charge_percent, 100)
        self.assertEqual(rover.status, "FIELD")

    def test_rover_moves_towards_station(self):
        rover = Rover(distance_to_station=100)

        rover.return_to_station()

        self.assertEqual(rover.distance_to_station, 70)
        self.assertEqual(rover.status, "RETURNING")

    def test_rover_cannot_charge_before_reaching_station(self):
        rover = Rover(distance_to_station=50)
        battery = Battery(charge_percent=40)

        rover.recharge(battery)

        self.assertEqual(battery.charge_percent, 40)

    def test_rover_charges_at_station(self):
        rover = Rover(distance_to_station=0)
        battery = Battery(charge_percent=40)

        rover.recharge(battery)

        self.assertEqual(battery.charge_percent, 45)
        self.assertEqual(rover.status, "CHARGING")


if __name__ == "__main__":
    unittest.main()
