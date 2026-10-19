
class Rover:
    def __init__(self, distance_to_station=100):
        self.distance_to_station = max(
            0, float(distance_to_station)
        )
        self.status = (
            "CHARGING"
            if self.distance_to_station == 0
            else "FIELD"
        )
        self.charging_rate = 5  # Percentage points per cycle
        self.travel_distance_per_cycle = 30

    def return_to_station(self):
        """Move the rover closer to its charging station."""
        if self.distance_to_station <= 0:
            self.distance_to_station = 0
            self.status = "CHARGING"
            return

        self.status = "RETURNING"

        self.distance_to_station = max(
            0,
            self.distance_to_station
            - self.travel_distance_per_cycle,
        )

        print("\n--- Return Journey ---")
        print(
            f"Distance remaining: "
            f"{self.distance_to_station:.1f} metres"
        )

        if self.distance_to_station == 0:
            self.status = "CHARGING"
            print("Rover reached its charging station!")

    def recharge(self, battery):
        """Recharge only when the rover is at its station."""
        if self.distance_to_station > 0:
            print(
                "Cannot recharge: rover has not reached "
                "the station."
            )
            return

        self.status = "CHARGING"

        battery.charge_percent = min(
            100,
            battery.charge_percent + self.charging_rate,
        )

        print(
            f"Charging... Battery: "
            f"{battery.charge_percent:.2f}%"
        )

        if battery.charge_percent >= 100:
            self.status = "FIELD"
            print(
                "Battery full. Rover is ready for "
                "field monitoring."
            )

    def is_at_station(self):
        """Return True when the rover has reached its station."""
        return self.distance_to_station <= 0
