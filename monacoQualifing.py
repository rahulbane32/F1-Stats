import fastf1
import matplotlib.pyplot as plt

# Enable cache
fastf1.Cache.enable_cache('cache')  # Creates a folder to store data

# Load session
session = fastf1.get_session(2023, 'Monaco', 'Q')
session.load()

# Get Verstappen's fastest lap
ver_lap = session.laps.pick_driver('VER').pick_fastest()
telemetry = ver_lap.get_car_data().add_distance()

# Plot speed trace
plt.plot(telemetry['Distance'], telemetry['Speed'])
plt.title("Max Verstappen Speed - Monaco Quali")
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.grid(True)
plt.show()
