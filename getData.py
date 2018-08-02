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