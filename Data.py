import requests
import time
import numpy as np
import mysql.connector
import datetime

class Coordinates:
    coordinates = []

    def __init__(self, add):
        self.add = add

    def findCoordinates(self):
        key = your_key # key needs to be updated as it expires frequently (else add billing account to your project)
        link = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + key
        address = self.add
        params = {'address': address} 

        try:
            response = requests.get(link, params=params)
            time.sleep(1)
            data = response.json()
            # print()
            # print(data)
            # print()
            lat = data['results'][0]['geometry']['location']['lat']
            Coordinates.coordinates.append(lat)
            lon = data['results'][0]['geometry']['location']['lng']
            Coordinates.coordinates.append(lon)
        except Exception as e:
            print("Travelling to " +address+ " to find its coordinates...")

    def getCoordinates(self):
        return Coordinates.coordinates

class City:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def findWeather(self):
        self.weather_params = {}
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
        self.weather_params = {'weather': weather, 'temp': temp, 'pressure': pressure, 'humidity': humidity,
                               'min_temp': min_temp, 'max_temp': max_temp, 'wind_speed': wind_speed}

    def getWeather(self):
        return self.weather_params


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
            print("Weather Report of", now.strftime("%d-%m-%Y %H:%M"))
            time.sleep(0.5)
            if len(day) == 1:
                day = '0' + day
            if len(month) == 1:
                month = '0' + month
            date = day + "-" + month + "-" + year
            con = mysql.connector.connect(user="root", password="", host="127.0.0.1", database="db1")
            if con.is_connected():
                cursor = con.cursor()
                sql = "insert into Weather values(null,'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(date,self.add.upper(),
                                                                                            self.dictionary.get("weather"),
                                                                                            self.dictionary.get("temp"),
                                                                                            self.dictionary.get("pressure"),
                                                                                            self.dictionary.get("humidity"),
                                                                                            self.dictionary.get("min_temp"),
                                                                                            self.dictionary.get("max_temp"),
                                                                                            self.dictionary.get("wind_speed"))
                cursor.execute(sql)
                con.commit()
            else:
                print ("Connect your database please!")

cities = ['Tokyo','New York','Rio de Janeiro','London','Cape Town','Mumbai','Sydney','Paris','Munich','Toronto']
i = 0
loc = ""
while i<len(cities):
    try:
        loc = cities[i]
        # print(loc)
        Coordinates.coordinates = []
        c1 = Coordinates(loc)
        x = c1.findCoordinates()
        coordinates = c1.getCoordinates()
        if len(coordinates)!=0:
            c2 = City(coordinates)
            print("Reached",loc,"located at:",c2.coordinates)
            test = {}
            c2.findWeather()
            test = c2.getWeather()
            if len(test)!=0:
                i = i + 1
                c3 = saveDB(loc, test)
                c3.save()
                print(test)
                print("Saved!")
            else:
                pass
        else:
            continue
    except Exception as e:
        print("Error: ",e)
