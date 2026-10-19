
# AgroGuardian 🌱

**An AI-ready agricultural monitoring rover simulation for sustainable farming.**

AgroGuardian is a Python-based prototype that simulates an agricultural rover monitoring environmental conditions, evaluating irrigation needs, managing battery power, using solar energy, and returning to a charging station when its battery reserve becomes low.

The project is being developed for the Nebius Global AI Hackathon, Track 4: Physical AI.

> **Project status:** Simulation prototype. Physical hardware control and Nebius/NVIDIA model integration are planned future milestones. Sensor readings and power-management values are simulated and are not validated for real-world deployment.

## Features

- **Environmental monitoring:** Simulated soil moisture, temperature, humidity, water level, and sunlight readings.
- **Irrigation decisions:** Rule-based decisions using soil moisture and water availability.
- **Solar power estimation:** Estimates solar output from sunlight, panel area, and panel efficiency.
- **Battery simulation:** Models battery charge changes based on estimated energy production and consumption.
- **Rover management:** Simulates returning to a charging station and recharging.
- **Power safety:** Prioritizes returning to the station when the battery reserve is too low.
- **CSV logging:** Records monitoring cycles for later analysis.
- **Interactive dashboard:** Displays current readings, environmental alerts, and historical charts.
- **Downloadable reports:** Exports monitoring data and reconstructed alert history.
- **Automated tests:** Tests key battery, rover, irrigation, and power-management behaviors.

## Technology stack

- Python
- Streamlit
- Pandas
- CSV data storage
- Python `unittest`

## Project structure

```text
AgriGaurdian/
├── main.py
├── app.py
├── sensors.py
├── safety.py
├── power_manager.py
├── battery.py
├── rover.py
├── logger.py
├── requirements.txt
├── README.md
└── tests/
    ├── test_decisions.py
    └── test_battery_rover.py
```

The `agroguardian_log.csv` file is generated automatically when the simulation records monitoring cycles.

## Requirements

- Python 3.10 or newer recommended
- pip
- Visual Studio Code or another Python editor

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AgriGaurdian
```

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

## Run the simulation

Start the rover simulation:

```bash
py main.py
```

The simulation generates sensor readings, evaluates irrigation decisions, manages power modes, updates battery charge, and logs monitoring cycles.

Press `Ctrl+C` to stop the simulation.

## Run the dashboard

Open a second terminal in the project directory and run:

```bash
py -m streamlit run app.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

The dashboard displays monitoring readings, rover status, environmental alerts, historical charts, and downloadable CSV reports.

Keep the simulation running in one terminal to generate new data for the dashboard.

## Run automated tests

Run the test suite:

```bash
py -m unittest discover -s tests -v
```

The current prototype has 18 automated tests covering key decision-making, battery, and rover behaviors.

## Current limitations

- Sensor readings are randomized rather than collected from physical sensors.
- Irrigation is recommended by software; no physical irrigation hardware is controlled.
- Battery capacity, solar-panel specifications, energy consumption, and return thresholds are illustrative simulation values.
- The rover does not yet use physical navigation or obstacle detection.
- Alert thresholds are demonstration settings and require crop-specific validation.
- The dashboard reconstructs historical alerts from logged sensor readings.
- Nebius Token Factory and NVIDIA open-source model integration remain future development tasks.

## Roadmap

- [x] Simulated environmental sensors
- [x] Rule-based irrigation decisions
- [x] Battery and solar power simulation
- [x] Rover return-to-station behavior
- [x] CSV monitoring logs
- [x] Interactive dashboard and environmental alerts
- [x] Historical alert display and downloadable reports
- [x] Initial automated test suite
- [ ] Improve and validate station-to-field charging behavior
- [ ] Add configuration for crop-specific thresholds
- [ ] Integrate a Nebius-hosted AI model
- [ ] Integrate a suitable NVIDIA open-source model
- [ ] Add AI-assisted environmental analysis
- [ ] Prepare a demonstration and evaluation results
- [ ] Test on real hardware, if available

## Contributing

Contributions, bug reports, and suggestions are welcome. Please test changes before submitting them.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
