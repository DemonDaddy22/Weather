# import requests
# import time

# url = 'http://maps.googleapis.com/maps/api/geocode/json'
# add = input('Enter address: ')
# params = {
#     'address' : add,
#     'sensor' : 'false',
#     # 'region' : 'india'
#     }
# response = requests.get(url, params = params)
# time.sleep(1)
# data = response.json()

# lat = data['results'][0]['geometry']['location']['lat']
# lon = data['results'][0]['geometry']['location']['lng']

# print (lat)
# print (lon)

# user_api = 'f50cf750f8468c9127cf0a7aa1a37409'
# unit = 'metric'
# api = 'http://api.openweathermap.org/data/2.5/weather?lat='
# link = api + str(lat) + '&lon=' + str(lon) + '&mode=json&units=' + unit + '&APPID=' + user_api
# response1 = requests.get(link)
# print(response1.text)
import matplotlib.pyplot as plt
import matplotlib.style as st

min_temp = [34.4, 35, 32.7, 36.9, 33.1]
max_temp = [37.8, 39.1, 35.5, 40.6, 36]
pressure = [1100,1043,1128,1179,1045]
humidity = [4,1,2,7,8]
wind_speed = [2.2,0.5,1.8,3.4,1.7]
n = len(min_temp)
count = list(range(1,n+1))
st.use('bmh')
plt.figure()
plt.subplot(221)
plt.plot(count, max_temp, 'o', count, max_temp, '#3ec9b6', label = 'Max Temp')
plt.plot( count, min_temp, 'o', count, min_temp, '#e84efc', label = 'Min Temp')
plt.grid(True)
plt.xlabel('Days')
plt.ylabel('Temp')
plt.xticks(list(range(0,n+1)))

plt.subplot(222)
plt.plot(count, pressure, 'o', count, pressure, '#eaa141')
plt.grid(True)
plt.xlabel('Days')
plt.ylabel('Pressure')
plt.xticks(list(range(0,n+1)))

plt.subplot(223)
plt.plot(count, humidity, 'o', count, humidity, '#ea2e6d')
plt.grid(True)
plt.xlabel('Days')
plt.ylabel('Humidity')
plt.xticks(list(range(0,n+1)))

plt.subplot(224)
plt.plot(count, wind_speed, 'o', count, wind_speed, '#9ed13a')
plt.grid(True)
plt.xlabel('Days')
plt.ylabel('Wind Speed')
plt.xticks(list(range(0,n+1)))

plt.show()
