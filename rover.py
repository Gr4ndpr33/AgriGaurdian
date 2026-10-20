
class Rover:
    def __init__(self, distance_to_station=100):
        self.distance_to_station = max(0, float(distance_to_station))
        self.status = "CHARGING" if self.distance_to_station == 0 else "FIELD"
        self.charging_rate = 5
        self.travel_distance_per_cycle = 30
        self.field_distance_from_station = 100

    def return_to_station(self):
        if self.distance_to_station <= 0:
            self.distance_to_station = 0
            self.status = "CHARGING"
            return

        self.status = "RETURNING"
        self.distance_to_station = max(
            0,
            self.distance_to_station - self.travel_distance_per_cycle,
        )

        print("\n--- Return Journey ---")
        print(f"Distance remaining: {self.distance_to_station:.1f} metres")

        if self.distance_to_station == 0:
            self.status = "CHARGING"
            print("Rover reached its charging station!")

    def recharge(self, battery):
        if self.distance_to_station > 0:
            print("Cannot recharge: rover has not reached the station.")
            return

        self.status = "CHARGING"
        battery.charge_percent = min(
            100,
            battery.charge_percent + self.charging_rate,
        )

        print(f"Charging... Battery: {battery.charge_percent:.2f}%")

        if battery.charge_percent >= 100:
            self.distance_to_station = self.field_distance_from_station
            self.status = "FIELD"
            print("Battery full. Rover is ready for field monitoring.")
            print("Rover has left the charging station.")

    def is_at_station(self):
        return self.distance_to_station <= 0
