# 🌤️ Weather Map Plotting Module

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg?style=flat-square&logo=python" alt="Python 3.12">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/Build-Stable-brightgreen.svg?style=flat-square" alt="Build Status">
</p>

## 📊 Overview

This module creates professional weather maps in **panson format** for a specified region and time period. It fetches actual weather data from meteorological stations and generates visual representations with temperature, dew point, and wind information.

The module implements all the requirements specified in the project documentation, including:
- Creating 1500x1500px weather maps
- Covering the region from lat 34, lon 110 (top-left) to lat 21, lon 120 (bottom-right)
- Plotting weather parameters: T (temperature), Td (dew point), ff (wind speed), dd (wind direction)
- Adding station identification numbers to the right of each weather symbol in light gray
- Generating maps for dates at 3-day intervals
- Storing maps in the `maps/` folder with appropriate naming
- Exporting weather data to `weather.csv`

## 🎯 Features

| Feature | Description |
|--------|-------------|
| 🌡️ **Temperature Mapping** | Displays temperature (T) in Northwest position with red color |
| 💧 **Dew Point Mapping** | Shows dew point (Td) in Southwest position with green color |
| 💨 **Wind Visualization** | Presents wind speed (ff) and direction (dd) as wind barbs in center |
| 🏷️ **Station Identification** | Adds station IDs in light gray to the right of each symbol |
| 📅 **Periodic Processing** | Generates maps for every 3rd day of the year |
| 📁 **Organized Output** | Saves maps in `maps/` directory with timestamped filenames |
| 📥 **Data Export** | Exports all weather data to `weather.csv` |

## 🖼️ Example Weather Map

![Example Weather Map](maps/2025-03-23_1200_weather_map.png)

*Example of a generated weather map showing temperature, dew point, and wind data*

## ⚙️ Requirements

- **Python 3.12**
- Required Python packages:
  - `metpy` - Meteorological calculations and plotting
  - `meteostat` - Weather data fetching
  - `cartopy` - Geospatial data processing
  - `matplotlib` - Plotting library
  - `pandas` - Data manipulation
  - `numpy` - Numerical computing

## 🚀 Installation

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

## ▶️ Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the module to generate weather maps for 2023 (testing)
python weather_map_plotter.py
```

For production use with 2025 data, modify the script to use year 2025 instead of 2023.

## 🛠️ Configuration

The module is configured to create weather maps for the following region:
- **Top-left corner**: Latitude 34, Longitude 110
- **Bottom-right corner**: Latitude 21, Longitude 120
- **Map size**: 1500x1500 pixels
- **Data interval**: Every 3 days
- **Display parameters**: T, Td, ff, dd
- **Station IDs**: Displayed to the right of symbols in light gray

## 📁 Output Structure

```
weather_plot_puanson/
├── maps/                          # Generated weather maps
│   ├── 2025-01-01_0000_weather_map.png
│   ├── 2025-01-01_1200_weather_map.png
│   └── ...
├── weather.csv                    # Exported weather data
├── weather_map_plotter.py         # Main implementation
└── api_get_data.py                # Data fetching utilities
```

## 📊 Data Format

The weather data is exported in CSV format with the following columns:
- **T**: Temperature (°C)
- **Td**: Dew point temperature (°C)
- **ff**: Wind speed (m/s)
- **dd**: Wind direction (degrees)
- **station_id**: Meteorological station identifier
- **lat/lon**: Station coordinates
- **name**: Station name

## 👥 Author

**F2re** - *Meteorological Data Visualization Specialist*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## 🆘 Support

For questions, bug reports, or contributions, please refer to the project repository guidelines and contact the development team through established channels.