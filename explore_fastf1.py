"""
Quick exploration of FastF1 capabilities
"""
import fastf1
import pandas as pd

# Enable cache for faster loading
fastf1.Cache.enable_cache('/tmp/fastf1_cache')

print("FastF1 version:", fastf1.__version__)
print("\n" + "="*60)
print("Loading 2024 Abu Dhabi GP data as example...")
print("="*60 + "\n")

try:
    # Load a recent race session
    session = fastf1.get_session(2024, 'Abu Dhabi', 'R')
    session.load()

    print("✓ Session loaded successfully!")
    print(f"\nEvent: {session.event['EventName']}")
    print(f"Date: {session.event['EventDate']}")
    print(f"Session: {session.name}")

    # Get list of drivers
    drivers = session.drivers
    print(f"\n📊 Drivers in session: {len(drivers)}")

    # Get some driver info
    print("\nDriver details:")
    for drv in drivers[:5]:  # Show first 5
        driver = session.get_driver(drv)
        print(f"  {drv}: {driver['FullName']} - {driver['TeamName']}")

    # Show available telemetry data
    print("\n📡 Available telemetry channels:")
    laps = session.laps
    if not laps.empty:
        fastest_lap = laps.pick_fastest()
        telemetry = fastest_lap.get_telemetry()
        print(f"  Columns: {list(telemetry.columns)}")
        print(f"  Sample rate: ~{len(telemetry)} data points per lap")

    # Show lap data columns
    print("\n🏁 Available lap data:")
    print(f"  Columns: {list(laps.columns)}")

    # Weather data
    print("\n🌤️  Weather data available:")
    weather = session.weather_data
    if not weather.empty:
        print(f"  Columns: {list(weather.columns)}")

    # Car data
    print("\n🏎️  Car data available:")
    if not laps.empty:
        car_data = fastest_lap.get_car_data()
        print(f"  Columns: {list(car_data.columns)}")

    # Position data
    print("\n📍 Position data available:")
    if not laps.empty:
        pos_data = fastest_lap.get_pos_data()
        print(f"  Columns: {list(pos_data.columns)}")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying to load 2023 season data instead...")

    try:
        session = fastf1.get_session(2023, 'Monaco', 'R')
        session.load()
        print("✓ 2023 Monaco GP loaded successfully!")

        drivers = session.drivers
        print(f"\n📊 Drivers: {len(drivers)}")

        laps = session.laps
        print(f"🏁 Total laps: {len(laps)}")

        if not laps.empty:
            fastest = laps.pick_fastest()
            telemetry = fastest.get_telemetry()
            print(f"\n📡 Telemetry columns: {list(telemetry.columns)}")

    except Exception as e2:
        print(f"❌ Also failed: {e2}")
