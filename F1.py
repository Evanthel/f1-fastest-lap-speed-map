# Step 1: Import libraries

import fastf1 as ff1                      
import numpy as np                        
import matplotlib.pyplot as plt           
from matplotlib.collections import LineCollection  
import os

# Create cache folder if it doesn't exist
os.makedirs('cache', exist_ok=True)
ff1.Cache.enable_cache('cache')


# Step 2: Set race parameters

year = 2025                     # Season
race = 'Japanese Grand Prix'    # Race name
session_type = 'R'              # R = Race session
driver = 'VER'                  # Driver code for Max Verstappen


# Step 3: Load the session
session = ff1.get_session(year, race, session_type)
session.load()
event = session.event


# Step 4: Get Verstappen fastest lap telemetry
lap = session.laps.pick_driver(driver).pick_fastest()
telemetry = lap.get_telemetry()

# Extract track coordinates (position of the car)
x = telemetry['X'].values
y = telemetry['Y'].values

# Extract speed values at each point
speed = telemetry['Speed'].values


# Step 5: Create track segments

# Combine X and Y coordinates into points
points = np.array([x, y]).T.reshape(-1, 1, 2)

# Create segments between consecutive points
segments = np.concatenate([points[:-1], points[1:]], axis=1)


# Step 6: Plot the track

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot track outline
ax.plot(x, y, color='black', linewidth=2, linestyle='-', zorder=0)

# Create colored line segments based on speed
lc = LineCollection(segments, cmap='plasma', linewidth=4)

# Assign speed values to determine color
lc.set_array(speed)

# Add segments to the plot
line = ax.add_collection(lc)

# Create colorbar to show speed scale
cbar = plt.colorbar(line, ax=ax)
cbar.set_label('Speed (km/h)')


# Step 7: Final styling
ax.set_title(
    "Max Verstappen - 2025 Japanese Grand Prix Winning Race\nFastest Lap Speed Map",
    fontsize=14
)

ax.axis('off')
plt.tight_layout()
plt.show()