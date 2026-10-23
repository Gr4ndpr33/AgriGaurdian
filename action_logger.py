
"""CSV audit logging for AgroGuardian action decisions."""

import csv
from datetime import datetime
from pathlib import Path


AUDIT_FILE = Path(__file__).resolve().parent / "action_audit.csv"

AUDIT_FIELDS = [
    "timestamp",
    "action",
    "reason",
    "approved",
    "validation_reason",
    "executed",
    "execution_message",
]


def log_action(action, validation, execution_result=None):
    """Append an action decision and its outcome to the audit CSV."""

    row = {
        "timestamp": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "action": action.get("action", "UNKNOWN"),
        "reason": action.get("reason", ""),
        "approved": validation.get("approved", False),
        "validation_reason": validation.get("reason", ""),
        "executed": (
            execution_result.get("executed", False)
            if execution_result is not None
            else False
        ),
        "execution_message": (
            execution_result.get("message", "")
            if execution_result is not None
            else "Not executed because validation failed."
        ),
    }

    file_exists = (
        AUDIT_FILE.exists() and AUDIT_FILE.stat().st_size > 0
    )

    with AUDIT_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=AUDIT_FIELDS
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)
