
import random
import time

from sensors import read_sensors
from safety import evaluate_irrigation
from power_manager import decide_power_mode
from battery import Battery
from rover import Rover
from logger import log_cycle
from pest_monitor import evaluate_pest_risk
from actions import decide_actions, validate_action, execute_simulated_action

def simulate_pest_readings():
    """Generate simulated pest observations for prototype testing."""

    plants_inspected = 20
    pests_observed = random.randint(0, 25)
    plants_damaged = random.randint(0, 8)

    return {
        "pests_observed": pests_observed,
        "plants_inspected": plants_inspected,
        "plants_damaged": plants_damaged,
    }

def process_actions(readings, pest_result=None, power_result=None):
    """Propose, validate, and simulate AgroGuardian actions."""

    proposed_actions = decide_actions(
        readings,
        pest_result=pest_result,
        power_result=power_result,
    )

    print("\n--- Action Coordination ---")

    for action in proposed_actions:
        print(f"Proposed action: {action['action']}")
        print(f"Reason: {action['reason']}")

        validation = validate_action(
    action,
    readings=readings,
    power_result=power_result,
)

        if validation["approved"]:
            result = execute_simulated_action(
    action,
    readings=readings,
    power_result=power_result,
)
            print(result["message"])
        else:
            print("Action rejected; it was not simulated.")

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
            pest_result = None

            print(f"\n--- Cycle {cycle} ---")
            print(f"Rover status: {rover.status}")
            print(f"Battery: {battery.charge_percent:.2f}%")
            print(
                f"Distance to station: "
                f"{rover.distance_to_station:.1f} m"
            )

            # Charge the rover before resuming field monitoring.
            if rover.is_at_station():
                rover.recharge(battery)

                readings["battery_percent"] = battery.charge_percent
                readings["distance_to_station"] = (
                    rover.distance_to_station
                )

                # No pest assessment is performed while charging.
                log_cycle(
                    readings,
                    power_mode,
                    rover.status,
                    irrigation_result,
                )

                time.sleep(2)
                continue

            # Evaluate power requirements before field activities.
            power = decide_power_mode(readings)
            power_mode = power["mode"]

            print(f"Power mode: {power_mode}")
            print(f"Reason: {power['reason']}")

            if power_mode == "RETURN_TO_STATION":
                irrigation_result = "PAUSED"

                print("ACTION: Field tasks paused; returning.")
                process_actions(readings, power_result=power)
                rover.return_to_station()

                # Simulated energy consumption during the return journey.
                battery.update(
                    solar_power_watts=0,
                    consumption_watts=25,
                    duration_seconds=60,
                )

            elif rover.status == "FIELD":
                # Simulate pest observations during field monitoring.
                pest_readings = simulate_pest_readings()
                pest_result = evaluate_pest_risk(pest_readings)

                # Add pest counts to the readings sent to the logger.
                readings.update(pest_readings)

                print("\n--- Crop Pest Monitoring ---")
                print(
                    f"Pests observed: "
                    f"{pest_readings['pests_observed']}"
                )
                print(
                    f"Plants inspected: "
                    f"{pest_readings['plants_inspected']}"
                )
                print(
                    f"Plants damaged: "
                    f"{pest_readings['plants_damaged']}"
                )
                print(
                    f"Pest pressure: "
                    f"{pest_result['pest_pressure_per_plant']:.2f} "
                    f"pests/plant"
                )
                print(
                    f"Crop damage: "
                    f"{pest_result['damage_percent']:.1f}%"
                )
                print(f"Pest risk: {pest_result['risk_level']}")
                print(f"Pest alert: {pest_result['alert']}")
                print(
                    f"Recommendation: "
                    f"{pest_result['recommendation']}"
                )

                # Evaluate irrigation independently of pest risk.
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
                process_actions(
    readings,
    pest_result=pest_result,
    power_result=power,
)

                # Update the battery after field operations.
                battery.update(
                    solar_power_watts=readings["solar_power_watts"],
                    consumption_watts=18,
                    duration_seconds=60,
                )

            else:
                # Never perform field tasks while returning to the station.
                print("Field tasks paused while rover is returning.")

            # Save the latest rover state.
            readings["battery_percent"] = round(
                battery.charge_percent, 2
            )
            readings["distance_to_station"] = (
                rover.distance_to_station
            )

            # Log pest results only when an assessment was performed.
            log_cycle(
                readings,
                power_mode,
                rover.status,
                irrigation_result,
                pest_result=pest_result,
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
