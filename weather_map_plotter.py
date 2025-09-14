#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для построения погодных карт в формате пансонов
@author F2re
"""


import os
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Stations, Hourly
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from metpy.calc import wind_components
from metpy.units import units
from metpy.plots import StationPlot
import cartopy.crs as ccrs
import cartopy.feature as cfeature



class WeatherMapPlotter:
    """
    Класс для построения погодных карт с пансонами
    """
    
    def __init__(self, output_dir='maps'):
        """
        Инициализация построителя карт
        
        :param output_dir: Директория для сохранения карт
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Границы региона для построения карты
        self.lat_min = 21
        self.lat_max = 34
        self.lon_min = 110
        self.lon_max = 120
        
        # Размер карты
        self.map_width = 1500
        self.map_height = 1500



    def get_stations_in_region(self):
        """
        Получение списка метеостанций в заданном регионе
        
        :return: DataFrame со списком станций
        """
        # Создаем объект станций
        stations = Stations()
        
        # Ограничиваем регион
        stations = stations.bounds((self.lat_max, self.lon_min), (self.lat_min, self.lon_max))
        
        # Получаем список станций
        station_list = stations.fetch()
        
        print(f"Найдено {len(station_list)} станций в регионе")
        return station_list



    def get_weather_data_for_datetime(self, dt):
        """
        Получение погодных данных для всех станций в регионе на заданную дату и время
        
        :param dt: Дата и время для получения данных
        :return: DataFrame с погодными данными
        """
        # Получаем список станций
        stations = self.get_stations_in_region()
        
        if stations.empty:
            print("Не найдено станций в регионе")
            return pd.DataFrame()
        
        # Собираем данные со всех станций
        all_data = []
        
        for station_id, station_info in stations.iterrows():
            try:
                # Получаем данные за конкретный час
                # Запрашиваем данные с небольшим интервалом вокруг нужного времени
                start = dt - timedelta(minutes=30)
                end = dt + timedelta(minutes=30)
                
                # Запрашиваем данные
                data = Hourly(station_id, start, end)
                df = data.fetch()
                
                if not df.empty:
                    # Выбираем нужные параметры
                    df = df[['temp', 'dwpt', 'wspd', 'wdir']].copy()
                    df = df.rename(columns={
                        'temp': 'T',
                        'dwpt': 'Td',
                        'wspd': 'ff',
                        'wdir': 'dd'
                    })
                    
                    # Удаляем строки с NaN значениями
                    df = df.dropna()
                    
                    if not df.empty:
                        # Берем только ближайшую запись к запрошенному времени
                        df['time_diff'] = abs((df.index - dt).total_seconds())
                        df = df.loc[[df['time_diff'].idxmin()]]
                        df = df.drop('time_diff', axis=1)
                        
                        # Добавляем информацию о станции
                        df['station_id'] = station_id
                        df['lat'] = station_info['latitude']
                        df['lon'] = station_info['longitude']
                        df['name'] = station_info['name']
                        
                        all_data.append(df)
                    else:
                        print(f"Нет корректных данных для станции {station_id}")
                else:
                    print(f"Нет данных для станции {station_id}")
                    
            except Exception as e:
                print(f"Ошибка при получении данных для станции {station_id}: {e}")
                continue
        
        if all_data:
            # Объединяем все данные
            result = pd.concat(all_data)
            return result
        else:
            return pd.DataFrame()



    def get_dates_for_year(self, year=2025, interval=3):
        """
        Получение списка дат для заданного года с указанным интервалом
        
        :param year: Год
        :param interval: Интервал в днях
        :return: Список дат
        """
        dates = []
        current_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=interval)
            
        return dates



    def plot_weather_map(self, weather_data, dt):
        """
        Построение погодной карты с пансонами для заданной даты и времени
        
        :param weather_data: DataFrame с погодными данными
        :param dt: Дата и время для построения карты
        """
        if weather_data.empty:
            print("Нет данных для построения карты")
            return
        
        # Создаем фигуру с заданным размером (1500x1500 пикселей)
        dpi = 150
        figsize = (self.map_width / dpi, self.map_height / dpi)
        fig = plt.figure(figsize=figsize, dpi=dpi)
        
        # Создаем карту с проекцией PlateCarree
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        
        # Устанавливаем границы карты
        ax.set_extent([self.lon_min, self.lon_max, self.lat_min, self.lat_max], crs=ccrs.PlateCarree())
        
        # Добавляем картографические элементы с улучшенными цветами для лучшего UX
        ax.add_feature(cfeature.COASTLINE.with_scale('10m'), edgecolor='black', linewidth=0.8)
        ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':', edgecolor='gray')
        ax.add_feature(cfeature.LAND.with_scale('10m'), facecolor='whitesmoke')
        ax.add_feature(cfeature.OCEAN.with_scale('10m'), facecolor='lightsteelblue')
        
        # Добавляем сетку
        ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        
        # Подготавливаем данные для пансонов
        lats = weather_data['lat'].values
        lons = weather_data['lon'].values
        temps = weather_data['T'].values
        dew_points = weather_data['Td'].values
        wind_speeds = weather_data['ff'].values
        wind_dirs = weather_data['dd'].values
        station_ids = weather_data['station_id'].values  # Получаем идентификаторы станций
        
        # Удаляем строки с NaN значениями
        valid_indices = ~(np.isnan(temps) | np.isnan(dew_points) | np.isnan(wind_speeds) | np.isnan(wind_dirs))
        lats = lats[valid_indices]
        lons = lons[valid_indices]
        temps = temps[valid_indices]
        dew_points = dew_points[valid_indices]
        wind_speeds = wind_speeds[valid_indices]
        wind_dirs = wind_dirs[valid_indices]
        station_ids = station_ids[valid_indices]  # Фильтруем идентификаторы станций
        
        if len(lats) == 0:
            print("Нет корректных данных для построения карты")
            plt.close()
            return
        
        # Преобразуем скорость и направление ветра в компоненты u, v
        # Предполагаем, что скорость ветра в км/ч
        try:
            # Преобразуем в обычные массивы numpy
            wind_speeds_np = np.array(wind_speeds, dtype=float)
            wind_dirs_np = np.array(wind_dirs, dtype=float)
            
            u_wind, v_wind = wind_components(
                wind_speeds_np * units('km/h'), 
                wind_dirs_np * units('degrees')
            )
            
            # Создаем станционные пансоны с улучшенным расстоянием
            station_plot = StationPlot(
                ax, lons, lats, 
                transform=ccrs.PlateCarree(),
                fontsize=8,
                spacing=7
            )
            
            # Добавляем температуру (T) в северо-западной позиции (тёмно-красным цветом, жирный шрифт)
            station_plot.plot_parameter('NW', temps, color='darkred', fontsize=10, weight='bold')
            
            # Добавляем точку росы (Td) в юго-западной позиции (тёмно-зелёным цветом, жирный шрифт)
            station_plot.plot_parameter('SW', dew_points, color='darkgreen', fontsize=10, weight='bold')
            
            # Добавляем флаги ветра в центральной позиции с улучшенной толщиной линий
            # Преобразуем в узлы для стандартного отображения
            u_knots = u_wind.to('knots').m
            v_knots = v_wind.to('knots').m
            station_plot.plot_barb(u_knots, v_knots, color='black', linewidth=1.3)
            
            # Добавляем идентификаторы станций справа (в восточной позиции) светло-серым цветом
            # Преобразуем station_ids в строковый формат для отображения
            station_ids_text = [str(sid) for sid in station_ids]
            station_plot.plot_text('E', station_ids_text, color='lightgray', fontsize=8)
            
            # Добавляем заголовок с улучшенным стилем
            plt.title(f'Погодная карта за {dt.strftime("%Y-%m-%d %H:%M")}', fontsize=20, weight='bold')
            
            # Сохраняем карту
            filename = f"{self.output_dir}/{dt.strftime('%Y-%m-%d_%H%M')}_weather_map.png"
            plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"Карта сохранена в {filename}")
        except Exception as e:
            print(f"Ошибка при построении карты: {e}")
            plt.close()



    def process_year_data(self, year=2025):
        """
        Обработка данных за весь год с заданным интервалом
        Создает карты для 00:00 и 12:00 часов каждого дня
        
        :param year: Год для обработки
        """
        # Получаем список дат
        dates = self.get_dates_for_year(year)
        
        # Собираем все данные в один DataFrame
        all_weather_data = []
        
        # Обрабатываем каждую дату
        for date in dates:
            # Для каждой даты создаем карты для 00:00 и 12:00
            for hour in [0, 12]:
                dt = datetime(date.year, date.month, date.day, hour, 0)
                print(f"Обработка данных за {dt.strftime('%Y-%m-%d %H:%M')}")
                weather_data = self.get_weather_data_for_datetime(dt)
                
                if not weather_data.empty:
                    # Добавляем дату и время
                    weather_data['datetime'] = dt
                    all_weather_data.append(weather_data)
                    
                    # Создаем карту для этой даты и времени
                    self.plot_weather_map(weather_data, dt)
                else:
                    print(f"Нет данных для {dt.strftime('%Y-%m-%d %H:%M')}")
        
        # Сохраняем все данные в один CSV файл
        if all_weather_data:
            combined_data = pd.concat(all_weather_data)
            combined_data.to_csv('weather.csv', index=False)
            print("Все данные сохранены в weather.csv")
        else:
            print("Нет данных для сохранения")



if __name__ == "__main__":
    # Создаем экземпляр построителя карт
    plotter = WeatherMapPlotter()
    
    # Для тестирования используем доступный год (2023) вместо 2025
    # В реальном применении, когда данные за 2025 будут доступны, 
    # можно будет использовать именно 2025 год
    print("Обработка данных за 2025 год с интервалом 3 дня (для тестирования)")
    plotter.process_year_data(2025)
    
    # Когда данные за 2025 год станут доступны, можно будет использовать:
    # print("Обработка данных за 2025 год с интервалом 3 дня")
    # plotter.process_year_data(2025)
