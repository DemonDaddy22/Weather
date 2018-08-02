import matplotlib.pyplot as plt
import matplotlib.style as st
import MainModule as mm

class Graphs:
    
    def makeGraph1(self, data):
        self.data = data
        temp = self.data['temp']
        pressure = self.data['pressure']
        humidity = self.data['humidity']
        min_temp = self.data['min_temp']
        max_temp = self.data['max_temp']
        wind_speed = self.data['wind_speed']
        weather = self.data['weather']
        n = len(temp)
        count = list(range(1,n+1))

        st.use('bmh')
        plt.figure()
        plt.subplot(221)
        plt.plot(count, max_temp, 'o', count, max_temp, '#3ec9b6', count, min_temp, 'o', count, min_temp, '#e84efc')
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

    def makeGraph2(self, data, parameter):
        # make data a dictionary with keys as city names
        self.data = data
        self.parameter = parameter
        colors = [] # list including 10 colors
        n = len(colors)
        i = 0
        try:
            for key in self.data:
                result_dict = self.data[key]
                if self.parameter.upper() == 'TEMPERATURE':
                    temp = result_dict['temp']
                    count = list(range(1,len(temp)+1))
                    plt.plot(count, temp, color = colors[i], label = key)

                elif self.parameter.upper() == 'HUMIDITY':
                    humidity = result_dict['humidity']
                    count = list(range(1,len(humidity)+1))
                    plt.plot(count, humidity, color = colors[i], label = key)
                
                elif self.parameter.upper() == 'WIND SPEED':
                    wind_speed = result_dict['wind_speed']
                    count = list(range(1,len(wind_speed)+1))
                    plt.plot(count, wind_speed, color = colors[i], label = key)

                else:
                    print ('Incorrect option')
                    break
                
                if i<n-1:
                    i += 1
                else:
                    i = 0

        except Exception as e:
            print(e)

        plt.xlabel('Days')
        plt.ylabel('self.parameter')
        plt.grid(True)
        plt.legend(loc = 2)
        plt.show()