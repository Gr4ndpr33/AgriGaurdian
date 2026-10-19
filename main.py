
import time

from sensors import read_sensors
from safety import evaluate_irrigation
from power_manager import decide_power_mode
from battery import Battery
from rover import Rover
from logger import log_cycle


def run_agriguardian():
    battery = Battery(charge_percent=70)
    rover = Rover(distance_to_station=100)

    print("=== AGRIGUARDIAN ROVER ===")
    print("Press Ctrl+C to stop the simulation.")

    cycle = 0

    try:
        while True:
            cycle += 1
            readings = read_sensors()

            readings["battery_percent"] = battery.charge_percent
            readings["distance_to_station"] = rover.distance_to_station

            irrigation_result = "PAUSED"
            power_mode = "CHARGING"

            print(f"\n--- Cycle {cycle} ---")
            print(f"Rover status: {rover.status}")
            print(f"Battery: {battery.charge_percent:.2f}%")
            print(
                f"Distance to station: "
                f"{rover.distance_to_station:.1f} m"
            )

            # A rover at the station must charge before field work.
            if rover.is_at_station():
                rover.recharge(battery)

                # Record the state after charging.
                readings["battery_percent"] = battery.charge_percent
                readings["distance_to_station"] = (
                    rover.distance_to_station
                )

                log_cycle(
                    readings,
                    power_mode,
                    rover.status,
                    irrigation_result,
                )

                time.sleep(2)
                continue

            # Evaluate power needs before any field activity.
            power = decide_power_mode(readings)
            power_mode = power["mode"]

            print(f"Power mode: {power_mode}")
            print(f"Reason: {power['reason']}")

            if power_mode == "RETURN_TO_STATION":
                irrigation_result = "PAUSED"
                print("ACTION: Field tasks paused; returning.")
                rover.return_to_station()

                # Simulated energy used during this travel cycle.
                battery.update(
                    solar_power_watts=0,
                    consumption_watts=25,
                    duration_seconds=60,
                )

            elif rover.status == "FIELD":
                irrigation = evaluate_irrigation(readings)
                irrigation_result = irrigation["irrigate"]

                print(
                    f"Solar output: "
                    f"{readings['solar_power_watts']} W"
                )
                print(
                    f"Irrigation recommended: "
                    f"{irrigation['irrigate']}"
                )
                print(f"Reason: {irrigation['reason']}")

                battery.update(
                    solar_power_watts=readings["solar_power_watts"],
                    consumption_watts=18,
                    duration_seconds=60,
                )

            else:
                # Never perform normal field tasks while returning.
                print("Field tasks paused while rover is returning.")

            # Save the latest simulated state.
            readings["battery_percent"] = round(
                battery.charge_percent, 2
            )
            readings["distance_to_station"] = (
                rover.distance_to_station
            )

            log_cycle(
                readings,
                power_mode,
                rover.status,
                irrigation_result,
            )

            print(f"Updated battery: {battery.charge_percent:.2f}%")
            print("Monitoring cycle saved to CSV.")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nSimulation stopped.")
        print(f"Final battery: {battery.charge_percent:.2f}%")
        print(f"Rover status: {rover.status}")


if __name__ == "__main__":
    run_agriguardian()
