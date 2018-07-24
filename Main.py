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

class CoordinatesThread(threading.Thread):
    coordinates = []

    def __init__(self, add):
        threading.Thread.__init__(self)
        self.add = add

    def run(self):
        lock.acquire()
        link = 'http://maps.googleapis.com/maps/api/geocode/json'
        address = self.add
        params = { 'address': address }
        response = requests.get(link, params = params)
        # time.sleep(1)
        data = response.json()
        loc = data['results'][0]['address_components'][0]['long_name']
        if address == loc:
            lat = data['results'][0]['geometry']['location']['lat']
            CoordinatesThread.coordinates.append(lat)
            lon = data['results'][0]['geometry']['location']['lng']
            CoordinatesThread.coordinates.append(lon)
        else:
            pass
        lock.release()
        
    def getCoordinates(self):
        return CoordinatesThread.coordinates

# This thread will send request to fetch weather conditions of specified city

class CityThread (threading.Thread):
    weather_params = []

    def __init__(self, loc):
        threading.Thread.__init__(self)
        self.loc = loc

    def run(self):
        location = self.loc
        link = ''
        
# Use the city api call
# Write to DB
# Check if entered city exists in the world
# Create city class and separate out all necessary weather conditions
# Make subplots to show the comparisons
# Make Gui
# Do necessary analysis and predict future trends using ML/DL

