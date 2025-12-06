# 🏎️ F1 Telemetry Dashboard

A beautiful, interactive dashboard for analyzing Formula 1 telemetry data using FastF1 and Dash/Plotly.

## Features

### 📊 Data Visualizations
- **Lap Time Analysis** - Compare lap times across drivers throughout the session
- **Speed Comparison** - Overlay speed traces on fastest laps
- **Detailed Telemetry** - Speed, Throttle, Brake, and Gear data in synchronized charts
- **Track Position Map** - Visualize driver racing lines with speed data
- **Tire Strategy** - Visual timeline of tire compounds used by each driver
- **Weather Conditions** - Air temp, track temp, humidity, wind, and rainfall data

### 🎨 Styling
- Dark theme inspired by modern crypto/finance dashboards
- Purple/violet accent colors
- Smooth gradients and glassmorphism effects
- Responsive grid layout
- Clean, modern typography (Inter font)

### 🔧 Session Selection
- Years: 2023-2025
- All Grand Prix events
- Session types: Race, Qualifying, Practice 1-3, Sprint

## Installation

Dependencies are already installed:
```bash
pip3 install fastf1 dash plotly
```

## Usage

1. **Start the dashboard:**
```bash
python3 f1_dashboard.py
```

2. **Open your browser:**
Navigate to `http://127.0.0.1:8050`

3. **Select your session:**
   - Choose Year (2025 for current season)
   - Select Grand Prix (Abu Dhabi for tomorrow's finale!)
   - Pick session type (Race, Qualifying, etc.)
   - Click "Load Session Data"

4. **Compare drivers:**
   - Select 2-5 drivers from the dropdown
   - All charts update automatically

## Available Data

### Telemetry Channels
- Speed (km/h)
- Throttle percentage
- Brake on/off
- RPM
- Gear selection
- DRS status
- 3D position (X, Y, Z)

### Lap Data
- Lap times
- Sector times (1, 2, 3)
- Tire compound
- Tire age
- Pit stops
- Track position

### Environmental
- Air temperature
- Track temperature
- Humidity
- Wind speed/direction
- Rainfall

## Dashboard Sections

1. **Session Selector** - Choose year, race, and session type
2. **Driver Comparison** - Multi-select dropdown for drivers
3. **Lap Time Analysis** - Line chart showing lap progression
4. **Speed Comparison** - Fastest lap speed traces
5. **Detailed Telemetry** - 4-panel synchronized view
6. **Track Position Map** - Circuit layout with racing lines
7. **Tire Strategy** - Visual stint timeline
8. **Weather Conditions** - Metric cards with session weather

## Tips

- **Compare teammates** to see performance differences
- **Analyze qualifying** to understand where time is gained/lost
- **Study tire strategy** in races to see stint lengths
- **Use track map** to identify braking zones and racing lines
- **Check weather** for wet race analysis

## Data Source

All data is fetched from the official F1 live timing API via the FastF1 library.
Data is cached locally in `/tmp/fastf1_cache` for faster subsequent loads.

## Notes

- First load of a session may take 30-60 seconds (downloads data)
- Subsequent loads are much faster (uses cache)
- Some sessions may have incomplete data (especially recent ones)
- 2025 Abu Dhabi GP data will be available after the race completes

## Enjoy! 🏁
