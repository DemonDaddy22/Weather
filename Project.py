# importing the required modules

import requests
import time
import threading
#import matplotlib.pyplot as plt
#import matplotlib.style as st
import numpy as np
import mysql.connector
from tkinter import *
import datetime

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
        params = {'address': address}

        try:
            response = requests.get(link, params=params)
            time.sleep(1)
            data = response.json()
            lat = data['results'][0]['geometry']['location']['lat']
            Coordinates.coordinates.append(lat)
            lon = data['results'][0]['geometry']['location']['lng']
            Coordinates.coordinates.append(lon)
            Coordinates.coordinates = Coordinates.coordinates
        except Exception as e:
            print(e)

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
        City.weather_params = {'weather': weather, 'temp': temp, 'pressure': pressure, 'humidity': humidity,
                               'min_temp': min_temp, 'max_temp': max_temp, 'wind_speed': wind_speed}

    def getWeather(self):
        return City.weather_params


class saveDB:
    def __init__(self, add, dictionary):
        self.add = add
        self.dictionary = dictionary


    def save(self):
        if not self.dictionary :
            pass
        else:
            now = datetime.datetime.now()
            day = str(now.day)
            month = str(now.month)
            year = str(now.year)
            if len(day) == 1:
                day = '0' + str(now.day)
            if len(month) == 1:
                month = '0' + str(now.month)
            date = day + "-" + month + "-" + year
            sql = "insert into openweather values(null,'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(date,self.add.upper(),
                                                                                        self.dictionary.get("weather"),
                                                                                        self.dictionary.get("temp"),
                                                                                        self.dictionary.get("pressure"),
                                                                                        self.dictionary.get("humidity"),
                                                                                        self.dictionary.get("min_temp"),
                                                                                        self.dictionary.get("max_temp"),
                                                                                        self.dictionary.get("wind_speed"))
            con = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="mysql")
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()


cities = ['Tokyo','New York','Rio de Janeiro','London','Cape Town']
i = 0
loc = ""
while i<len(cities):

    try:
        loc = cities[i]
        print(loc)
        Coordinates.coordinates = []
        c1 = Coordinates(loc)
        x = c1.findCoordinates()
        coordinates = c1.getCoordinates()
        if len(coordinates)!=0:
            c2 = City(coordinates)
            print(c2.coordinates)
            test = {}
            if len(coordinates)==0:
                i = i
                print("Here Now!")
            else:
                c2.findWeather()
                test = c2.getWeather()
                if len(test)==0:
                    i=i
                    print("Here!")
                else:
                    i = i + 1
                    #c3 = saveDB(loc, test)
                    #c3.save()
                    print("Saved!")
        else:
            break
    except Exception as e:
        print("Check the connection!")

class DataBase_Retrieval:
    def getData(self):
        con = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='mysql')
        cursor = con.cursor()
        sql = 'select * from openweather'
        cursor.execute(sql)
        cities = []
        final_dict = {}
        # Creating a list with distinct cities
        for row in cursor:
            if row[2] not in cities:
                cities.append(row[2])
            else:
                continue
        print(cities)

        for city in cities:
            cursor1 = con.cursor()
            sql = 'select * from openweather ORDER BY Sno'
            cursor1.execute(sql)
            weather = []
            temp = []
            pressure = []
            humidity = []
            min_temp = []
            max_temp = []
            wind_speed = []
            date1 = []
            for row in cursor1:
                print(row[2])
                print(city)
                if city == row[3]:
                    format_str = '%d/%m/%Y'  # The format
                    datetime_obj = datetime.datetime.strptime(row[2], format_str)
                    date1.append(datetime_obj)
                    weather.append(row[4])
                    temp.append(float(row[5]))
                    pressure.append(float(row[6]))
                    humidity.append(float(row[7]))
                    min_temp.append(float(row[8]))
                    max_temp.append(float(row[9]))
                    wind_speed.append(float(row[10]))
                else:
                    pass

            dict1 = {'date1':date1,'weather': weather, 'temp': temp, 'pressure': pressure, 'humidity': humidity, 'min_temp': min_temp,
                     'max_temp': max_temp, 'wind_speed': wind_speed}
            final_dict.setdefault(city, []).append(dict1)

        return final_dict

import matplotlib.pyplot as plt
import matplotlib.style as st
# import MainModule as mm

class Graphs:
    def makeGraph1(self, data,startDate,endDate):
        self.data = data
        temp = self.data['temp']
        date2 = self.data['date1']
        pressure = self.data['pressure']
        humidity = self.data['humidity']
        min_temp = self.data['min_temp']
        max_temp = self.data['max_temp']
        wind_speed = self.data['wind_speed']
        weather = self.data['weather']
        startIndex = 0
        endIndex = 0
        for i in range(len(date2)):
            if date2[i] == startDate:
                startIndex = i
            elif date2[i] == endDate:
                endIndex = i
            else:
                pass
        endIndex = endIndex + 1
        n = endIndex - startIndex
        count = list(range(1, n + 1))

        st.use('bmh')
        plt.figure()
        plt.subplot(221)
        plt.plot(count, max_temp[startIndex:endIndex], 'o', count, max_temp[startIndex:endIndex], '#3ec9b6', count, min_temp[startIndex:endIndex], 'o', count, min_temp[startIndex:endIndex], '#e84efc')
        plt.grid(True)
        plt.xlabel('Days')
        plt.ylabel('Temp')
        plt.xticks(list(range(0, n + 1)))

        plt.subplot(222)
        plt.plot(count, pressure[startIndex:endIndex], 'o', count, pressure[startIndex:endIndex], '#eaa141')
        plt.grid(True)
        plt.xlabel('Days')
        plt.ylabel('Pressure')
        plt.xticks(list(range(0, n + 1)))

        plt.subplot(223)
        plt.plot(count, humidity[startIndex:endIndex], 'o', count, humidity[startIndex:endIndex], '#ea2e6d')
        plt.grid(True)
        plt.xlabel('Days')
        plt.ylabel('Humidity')
        plt.xticks(list(range(0, n + 1)))

        plt.subplot(224)
        plt.plot(count, wind_speed[startIndex:endIndex], 'o', count, wind_speed[startIndex:endIndex], '#9ed13a')
        plt.grid(True)
        plt.xlabel('Days')
        plt.ylabel('Wind Speed')
        plt.xticks(list(range(0, n + 1)))

    def makeGraph2(self, data, parameter, startDate, endDate):
        # make data a dictionary with keys as city names
        self.data = data
        self.parameter = parameter
        self.startDate = startDate
        self.endDate = endDate

        colors = ['#a5c1ef', '#96ef94', '#f7c259', '#e597f4', '#ff7a94', '#22b0b7', '#21b73a', '#d5db29', '#cd37e8', '#4c62e0']  # list including 10 colors
        n = len(colors)
        i = 0
        try:
            for key in self.data:
                result_dict = self.data[key]
                date2 = result_dict['date1']
                for i in range(len(date2)):
                    if date2[i] == self.startDate:
                        startIndex = i
                    elif date2[i] == self.endDate:
                        endIndex = i
                    else:
                        pass
                endIndex = endIndex + 1
                n = endIndex - startIndex
                count = list(range(1, n + 1))
                if self.parameter.upper() == 'TEMPERATURE':
                    temp = result_dict['temp']
                    plt.plot(count, temp[startIndex:endIndex], color=colors[i], label=key)

                elif self.parameter.upper() == 'HUMIDITY':
                    humidity = result_dict['humidity']
                    plt.plot(count, humidity[startIndex:endIndex], color=colors[i], label=key)

                elif self.parameter.upper() == 'WIND SPEED':
                    wind_speed = result_dict['wind_speed']
                    plt.plot(count, wind_speed[startIndex:endIndex], color=colors[i], label=key)

                elif self.parameter.upper() == 'PRESSURE':
                    pressure = result_dict['pressure']
                    plt.plot(count, pressure[startIndex:endIndex], color=colors[i], label=key)

                else:
                    print('Incorrect option')
                    break

                if i < n - 1:
                    i += 1
                else:
                    i = 0

        except Exception as e:
            print(e)

        plt.xlabel('Days')
        plt.ylabel('self.parameter')
        plt.grid(True)
        plt.legend(loc=2)
        plt.show()

import mysql.connector

class DataBase_Retrieval:
    def getData(self):
        con = mysql.connector.connect(user = 'root', password = '', host = '127.0.0.1', database = 'mysql')
        cursor = con.cursor()
        sql = 'select * from openweather'
        cursor.execute(sql)
        cities = []
        final_dict = {}
        # Creating a list with distinct cities
        for row in cursor:
            if row[1] not in cities:
                cities.append(row[1])
            else:
                continue

        for city in cities:
            weather = []
            temp = []
            pressure = []
            humidity = []
            min_temp = []
            max_temp = []
            wind_speed = []
            for row in cursor:
                if city == row[1]:
                    weather.append(row[2])
                    temp.append(row[3])
                    pressure.append(row[4])
                    humidity.append(row[5])
                    min_temp.append(row[6])
                    max_temp.append(row[7])
                    wind_speed.append(row[8])
                else:
                    pass
            
            dict1 = {'weather': weather, 'temp': temp, 'pressure': pressure, 'humidity': humidity, 'min_temp': min_temp, 'max_temp': max_temp, 'wind_speed': wind_speed}
            final_dict.setdefault(city, []).append(dict1)

        return final_dict
        
dr = DataBase_Retrieval()
data = dr.getData()
print(data)
city1 = input("Enter City: ")
startDate = input("Enter Start Date: ")
endDate = input("Enter End Date: ")
data1  = data[city1.upper()][0]
graph1 = Graphs()
graph2 = Graphs()
graph1.makeGraph1(data1, startDate, endDate)

# Validate the date entered by user
# Make GUI
# Check whether Graph 2 works correctly
