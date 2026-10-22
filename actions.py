
"""AgroGuardian action coordination and simulated execution."""

from safety import evaluate_irrigation


ALLOWED_ACTIONS = {
    "IRRIGATE",
    "MONITOR",
    "ALERT_OPERATOR",
    "RETURN_TO_STATION",
}


def decide_actions(readings, pest_result=None, power_result=None):
    """Propose actions from sensor and assessment results."""
    actions = []

    # Returning to the station takes priority.
    if (
        power_result is not None
        and power_result.get("mode") == "RETURN_TO_STATION"
    ):
        return [{
            "action": "RETURN_TO_STATION",
            "reason": "Power manager requires the rover to return.",
        }]

    irrigation_result = evaluate_irrigation(readings)

    if irrigation_result["irrigate"]:
        actions.append({
            "action": "IRRIGATE",
            "reason": irrigation_result["reason"],
        })

    if pest_result is not None:
        risk = str(pest_result.get("risk_level", "")).upper()

        if risk == "HIGH":
            actions.append({
                "action": "ALERT_OPERATOR",
                "reason": "High pest risk detected; inspect the crop.",
            })
        elif risk == "MODERATE":
            actions.append({
                "action": "ALERT_OPERATOR",
                "reason": "Moderate pest risk; monitor crop conditions.",
            })

    if not actions:
        actions.append({
            "action": "MONITOR",
            "reason": "No immediate action is recommended.",
        })

    return actions


def validate_action(action, readings=None, power_result=None):
    """Validate an action and its required safety conditions."""
    if not isinstance(action, dict):
        return {
            "approved": False,
            "reason": "Action must be a dictionary.",
        }

    action_name = action.get("action")

    if action_name not in ALLOWED_ACTIONS:
        return {
            "approved": False,
            "reason": f"Unknown action: {action_name!r}",
        }

    if not isinstance(action.get("reason"), str) or not action["reason"].strip():
        return {
            "approved": False,
            "reason": "Action must include a non-empty text reason.",
        }

    # Irrigation requires current readings and must pass the safety module.
    if action_name == "IRRIGATE":
        if not isinstance(readings, dict):
            return {
                "approved": False,
                "reason": "Current sensor readings are required for irrigation.",
            }

        try:
            irrigation_result = evaluate_irrigation(readings)
        except (KeyError, TypeError, ValueError):
            return {
                "approved": False,
                "reason": "Sensor readings are missing or invalid.",
            }

        if not irrigation_result["irrigate"]:
            return {
                "approved": False,
                "reason": irrigation_result["reason"],
            }

    # Returning is approved only when the power manager requires it.
    if action_name == "RETURN_TO_STATION":
        if (
            not isinstance(power_result, dict)
            or power_result.get("mode") != "RETURN_TO_STATION"
        ):
            return {
                "approved": False,
                "reason": "Return action requires power-manager authorization.",
            }

    return {
        "approved": True,
        "reason": "Action passed validation.",
    }


def execute_simulated_action(action, readings=None, power_result=None):
    """Simulate an action only after validating its safety conditions."""
    validation = validate_action(
        action,
        readings=readings,
        power_result=power_result,
    )

    if not validation["approved"]:
        return {
            "executed": False,
            "action": action.get("action")
            if isinstance(action, dict) else None,
            "message": validation["reason"],
        }

    return {
        "executed": True,
        "action": action["action"],
        "message": (
            f"SIMULATION ONLY: {action['action']} - "
            f"{action['reason']}"
        ),
    }
