# importing the required modules

import requests
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.style as st
import numpy as np

# This thread is used to get latitude and longitude of the specified location and also rejects any location
# creating a lock so that it can be used by threads to avoid mixing of resources

lock = threading.Lock()

class Coordinates:
    coordinates = []

    def __init__(self, add):
        self.add = add

    def findCoordinates(self):
        link = 'http://maps.googleapis.com/maps/api/geocode/json'
        address = self.add
        params = { 'address': address }
        response = requests.get(link, params = params)
        time.sleep(1)
        data = response.json()
        lat = data['results'][0]['geometry']['location']['lat']
        Coordinates.coordinates.append(lat)
        lon = data['results'][0]['geometry']['location']['lng']
        Coordinates.coordinates.append(lon)
        
    def getCoordinates(self):
        return Coordinates.coordinates

# This thread will send request to fetch weather conditions of specified city

class City:
    weather_params = {}

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def findWeather(self):
        coor = self.coordinates
        lat = coor[0]
        lon = coor[1]
        user_api = 'f50cf750f8468c9127cf0a7aa1a37409'
        unit = 'metric'
        api = 'http://api.openweathermap.org/data/2.5/weather?lat='
        link = api + str(lat) + '&lon=' + str(lon) + '&mode=json&units=' + unit + '&APPID=' + user_api
        response = requests.get(link)
        time.sleep(1)
        data = response.json()
        weather = data['weather'][0]['main']
        temp = data['main']['temp']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        wind_speed = data['wind']['speed']
        City.weather_params = {'weather': weather, 'temp': temp, 'pressure': pressure, 'humidity': humidity, 'min_temp': min_temp, 'max_temp': max_temp, 'wind_speed': wind_speed}
    
    def getWeather(self):
        return City.weather_params

loc = input('Enter location: ')
c1 = Coordinates(loc)
c1.findCoordinates()
coordinates = c1.getCoordinates()
c2 = City(coordinates)
c2.findWeather()
test = c2.getWeather()
print (test)
# Write to DB
# Check if entered city exists in the world
# Create city class and separate out all necessary weather conditions
# Make subplots to show the comparisons
# Make Gui
# Do necessary analysis and predict future trends using ML/DL

