
import csv
from pathlib import Path

import streamlit as st
import pandas as pd

from logger import LOG_FILE
from streamlit_autorefresh import st_autorefresh
# Page configuration

st.set_page_config(
    page_title="AgriGuardian Dashboard",
    page_icon="🌱",
    layout="wide",
)
# Refresh the dashboard on streamlit every 5 seconds
st_autorefresh(interval=5000, key="agroguardian_refresh")
from logger import LOG_FILE

st.title("🌱 AgriGuardian")
st.subheader("Agricultural Monitoring Rover Dashboard")

st.caption(
    "Live simulation data, environmental monitoring, "
    "battery status, and irrigation decisions."
)



# Load recorded data

def load_data():
    if not LOG_FILE.exists():
        return pd.DataFrame()

    try:
        with LOG_FILE.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            rows = list(csv.DictReader(file))

        return pd.DataFrame(rows)
    except (OSError, csv.Error):
        return pd.DataFrame()


data = load_data()

if data.empty:
    st.warning(
        "No logged data found yet. Run `py main.py` "
        "for a few cycles, then refresh this dashboard."
    )
    st.stop()


# Convert numeric columns from CSV text into numbers
numeric_columns = [
    "soil_moisture",
    "temperature",
    "humidity",
    "water_level",
    "sunlight",
    "solar_power_watts",
    "battery_percent",
    "distance_to_station",
]

for column in numeric_columns:
    if column in data.columns:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

latest = data.iloc[-1]



# Latest readings

st.markdown("## Latest readings")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Soil moisture",
    f"{latest['soil_moisture']:.1f}%",
)

col2.metric(
    "Temperature",
    f"{latest['temperature']:.1f} °C",
)

col3.metric(
    "Battery",
    f"{latest['battery_percent']:.1f}%",
)

col4.metric(
    "Solar output",
    f"{latest['solar_power_watts']:.2f} W",
)



# Rover and irrigation status

st.markdown("## Rover status")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Rover mode",
    str(latest.get("power_mode", "Unknown")),
)

col2.metric(
    "Rover status",
    str(latest.get("rover_status", "Unknown")),
)

col3.metric(
    "Distance to station",
    f"{latest['distance_to_station']:.1f} m",
)

irrigation = str(latest.get("irrigation", "Unknown"))

if irrigation == "True":
    st.success("Irrigation recommended for this cycle.")
elif irrigation == "False":
    st.info("Irrigation not recommended for this cycle.")
else:
    st.warning("Irrigation is paused or no decision is recorded.")


# -----------------------------
# Environmental safety alerts
# -----------------------------
st.markdown("## Environmental alerts")

alerts = []

if latest["soil_moisture"] < 20:
    alerts.append(
        ("CRITICAL", "Soil moisture is critically low.")
    )
elif latest["soil_moisture"] < 30:
    alerts.append(
        ("WARNING", "Soil moisture is low.")
    )

if latest["temperature"] > 35:
    alerts.append(
        ("WARNING", "Temperature is very high.")
    )

if latest["water_level"] < 10:
    alerts.append(
        ("CRITICAL", "Water tank level is critically low.")
    )
elif latest["water_level"] < 20:
    alerts.append(
        ("WARNING", "Water tank level is low.")
    )

if latest["battery_percent"] <= 25:
    alerts.append(
        ("CRITICAL", "Battery is low; return to station.")
    )
elif latest["battery_percent"] <= 40:
    alerts.append(
        ("WARNING", "Battery reserve is getting low.")
    )

if not alerts:
    st.success("No environmental alerts at this time.")
else:
    for severity, message in alerts:
        if severity == "CRITICAL":
            st.error(f"🚨 {severity}: {message}")
        else:
            st.warning(f"⚠️ {severity}: {message}")


# Historical charts

st.markdown("## Environmental history")

chart_data = data[
    ["soil_moisture", "temperature", "humidity"]
].copy()

chart_data.columns = [
    "Soil moisture (%)",
    "Temperature (°C)",
    "Humidity (%)",
]

st.line_chart(chart_data)

st.markdown("## Battery and solar history")

power_data = data[
    ["battery_percent", "solar_power_watts"]
].copy()

power_data.columns = [
    "Battery (%)",
    "Solar output (W)",
]

st.line_chart(power_data)



# Raw records

with st.expander("View recorded sensor data"):
    st.dataframe(data, use_container_width=True)

# Download monitoring report

st.markdown("## Download reports")

monitoring_csv = data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download full monitoring report",
    data=monitoring_csv,
    file_name="agroguardian_monitoring_report.csv",
    mime="text/csv",
)

# -----------------------------
# Historical environmental alerts
# -----------------------------
st.markdown("## Alert history")

alert_records = []

for _, row in data.iterrows():
    timestamp = row.get("timestamp", "Unknown")

    if row["soil_moisture"] < 20:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "CRITICAL",
            "Alert": "Soil moisture critically low",
        })
    elif row["soil_moisture"] < 30:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "WARNING",
            "Alert": "Soil moisture low",
        })

    if row["temperature"] > 35:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "WARNING",
            "Alert": "Temperature very high",
        })

    if row["water_level"] < 10:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "CRITICAL",
            "Alert": "Water tank critically low",
        })
    elif row["water_level"] < 20:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "WARNING",
            "Alert": "Water tank level low",
        })

    if row["battery_percent"] <= 25:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "CRITICAL",
            "Alert": "Battery low",
        })
    elif row["battery_percent"] <= 40:
        alert_records.append({
            "Timestamp": timestamp,
            "Severity": "WARNING",
            "Alert": "Battery reserve low",
        })

if alert_records:
    alerts_df = pd.DataFrame(alert_records)

    st.dataframe(
        alerts_df.iloc[::-1],
        use_container_width=True,
    )

    alert_csv = alerts_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download alert history",
        data=alert_csv,
        file_name="agroguardian_alert_history.csv",
        mime="text/csv",
    )

    st.caption(f"Total historical alerts: {len(alerts_df)}")
else:
    st.success("No historical alerts found in recorded data.")

st.caption(f"Recorded monitoring cycles: {len(data)}")
