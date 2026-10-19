
class Battery:
    def __init__(self, charge_percent=100):
        self.charge_percent = float(charge_percent)

    def update(self, solar_power_watts, consumption_watts, duration_seconds):
        """
        Update battery charge using estimated energy production
        and consumption over a time interval.
        """
        # Energy = power x time
        solar_energy_wh = solar_power_watts * duration_seconds / 3600
        consumed_energy_wh = consumption_watts * duration_seconds / 3600

        # Demo battery capacity; replace with real hardware specs later.
        battery_capacity_wh = 100

        net_energy_wh = solar_energy_wh - consumed_energy_wh
        change_percent = (net_energy_wh / battery_capacity_wh) * 100

        self.charge_percent = max(
            0,
            min(100, self.charge_percent + change_percent),
        )

        return round(self.charge_percent, 2)


if __name__ == "__main__":
    battery = Battery(charge_percent=70)

    print("Starting battery:", battery.charge_percent, "%")

    new_charge = battery.update(
        solar_power_watts=10,
        consumption_watts=20,
        duration_seconds=60,
    )

    print("Battery after 60 seconds:", new_charge, "%")
