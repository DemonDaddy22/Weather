import matplotlib.pyplot as plt
import matplotlib.style as st
import mysql.connector
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
