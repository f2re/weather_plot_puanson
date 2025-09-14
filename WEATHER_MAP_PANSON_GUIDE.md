# Weather Map Creation with Panson Symbols using MetPy and Matplotlib

This document explains how to create weather maps with panson symbols using MetPy and matplotlib, covering:

1. Temperature (T) - shown as numbers
2. Dew point (Td) - shown as numbers
3. Wind speed (ff) and direction (dd) - shown as wind barbs
4. Proper coordinate transformation
5. Creating a 1500x1500px map for a specific region

## Key Components

### 1. Setting up the Environment

```python
import numpy as np
import matplotlib.pyplot as plt
from metpy.plots import StationPlot
from metpy.calc import wind_components
from metpy.units import units
import cartopy.crs as ccrs
import cartopy.feature as cfeature
```

### 2. Coordinate Transformations

For weather maps, we typically use `ccrs.PlateCarree()` projection which works with standard latitude/longitude coordinates:

```python
# Create axes with PlateCarree projection
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Set the extent of the map to our region
ax.set_extent([110, 120, 21, 34], crs=ccrs.PlateCarree())
```

### 3. Creating a 1500x1500px Map

To create a map with exact pixel dimensions:

```python
# For 1500x1500px at 100 DPI
dpi = 100
figsize = (1500 / dpi, 1500 / dpi)  # 15 inches x 15 inches
fig = plt.figure(figsize=figsize, dpi=dpi)
```

### 4. Panson Symbols Placement

Using MetPy's `StationPlot` class for proper symbol placement:

```python
# Create station plot
stationplot = StationPlot(ax, station_lons, station_lats, 
                         transform=ccrs.PlateCarree(), fontsize=10)

# Temperature (T) - Northwest position
stationplot.plot_parameter('NW', temperatures, color='red')

# Dew point (Td) - Southwest position
stationplot.plot_parameter('SW', dew_points, color='green')

# Wind barbs - Center position
stationplot.plot_barb(u_wind, v_wind, color='black')
```

### 5. Wind Component Conversion

Convert meteorological wind direction and speed to u, v components:

```python
# Wind components calculation
u_wind, v_wind = wind_components(
    wind_speeds * units('m/s'), 
    wind_dirs * units('degrees')
)

# Convert to knots for standard plotting
u_wind_knots = u_wind.to('knots')
v_wind_knots = v_wind.to('knots')
```

## Implementation Files

The following Python files demonstrate different aspects of weather map creation:

1. `weather_map_panson.py` - Basic implementation
2. `advanced_weather_map_panson.py` - Advanced features and styling
3. `file_weather_data_panson.py` - Loading data from files with unit handling

## Standard Meteorological Conventions

- Temperature (T): Displayed in the Northwest (NW) position, typically in red
- Dew point (Td): Displayed in the Southwest (SW) position, typically in green
- Wind barbs: Displayed at the center position, showing speed and direction
- Wind direction: Meteorological convention (direction FROM which wind blows)
- Wind speed: Converted to knots for standard meteorological plots

## Coordinate System Notes

When working with different projections:

```python
# For PlateCarree (standard lat/lon)
projection = ccrs.PlateCarree()

# For Lambert Conformal (often used for mid-latitude regions)
projection = ccrs.LambertConformal(central_longitude=115, central_latitude=27.5)

# When plotting data that's in lat/lon coordinates on any projection:
stationplot = StationPlot(ax, lons, lats, transform=ccrs.PlateCarree())
```

The `transform` parameter is crucial - it tells Matplotlib what coordinate system your data is in, regardless of what projection you're using for the map display.

## Output Quality

For high-quality output:

```python
# Save with high DPI for better quality
plt.savefig('weather_map.png', dpi=300, bbox_inches='tight')
```