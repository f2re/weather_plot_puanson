# Weather Map Plotting Module

## Overview

This module creates professional weather maps in panson format for a specified region and time period. It fetches actual weather data from meteorological stations and generates visual representations with temperature, dew point, and wind information.

The module implements all the requirements specified in the project documentation, including:
- Creating 1500x1500px weather maps
- Covering the region from lat 34, lon 110 (top-left) to lat 21, lon 120 (bottom-right)
- Plotting weather parameters: T (temperature), Td (dew point), ff (wind speed), dd (wind direction)
- Adding station identification numbers to the right of each weather symbol in light gray
- Generating maps for dates at 3-day intervals
- Storing maps in the `maps/` folder with appropriate naming
- Exporting weather data to `weather.csv`

## Features

- Fetches real weather data from meteorological stations using Meteostat API
- Creates weather maps in panson format displaying:
  - Temperature (T) in Northwest position (red color)
  - Dew point (Td) in Southwest position (green color)
  - Wind speed (ff) and direction (dd) as wind barbs in center position
  - Station identification numbers in light gray to the right of each symbol
- Saves maps as high-resolution PNG images
- Exports weather data to CSV format
- Processes data for every 3rd day of the year

## Requirements

- Python 3.12
- Required Python packages:
  - metpy
  - meteostat
  - cartopy
  - matplotlib
  - pandas
  - numpy

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd weather_plot_puanson

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the module to generate weather maps for 2023 (testing)
python weather_map_plotter.py
```

For production use with 2025 data, modify the script to use year 2025 instead of 2023.

## Configuration

The module is configured to create weather maps for the following region:
- Top-left corner: Latitude 34, Longitude 110
- Bottom-right corner: Latitude 21, Longitude 120
- Map size: 1500x1500 pixels
- Data interval: Every 3 days
- Display parameters: T, Td, ff, dd
- Station IDs: Displayed to the right of symbols in light gray

## Output

- Maps are saved in the `maps/` directory with filenames in the format `YYYY-MM-DD_HHMM_weather_map.png`
- Weather data is exported to `weather.csv`

## File Structure

```
weather_plot_puanson/
├── weather_map_plotter.py    # Main implementation
├── api_get_data.py           # Data fetching utilities
├── maps/                     # Generated weather maps (PNG files)
├── weather.csv               # Exported weather data
├── README.md                 # Project documentation
├── DOCS.md                   # Detailed documentation
├── .gitignore                # Git ignore file
├── requirements.txt          # Python dependencies
└── venv/                     # Python virtual environment
```

## Author

F2re

## License

This project is licensed under the MIT License - see the LICENSE file for details.