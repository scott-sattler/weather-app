
import json
import random

import plotly.graph_objects as go

import requests
import time
import datetime
import ast


class WeatherApp:



    def __init__(self, url):
        self.__days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        self.url: str = url
        self.raw_data: dict = {}
        self.temperature = {str: [int, int]}  # {day: [high, low]}
        self.reformatted_data: dict = {}

        # have seven-day period start today, not monday
        today_date = datetime.datetime.today()
        weekday_index = datetime.datetime.weekday(today_date)
        dow = self.__days_of_week
        self.shifted_week = [dow[(i + weekday_index) % len(dow)] for i in range(len(dow))]

        # construct temperature dict
        self.temperature = {k: [None, None] for k in self.shifted_week}

        # configuration
        self.y_margin = .25  # high/low temp * y_margin


    def load_data(self):
        self.raw_data = requests.get(self.url)
        status_code = self.raw_data.status_code
        attempts = 1
        time_between_requests = 2

        # attempts to retrieve data until success
        while status_code != 200:
            self.raw_data = requests.get(self.url)
            status_code = self.raw_data.status_code
            time.sleep(time_between_requests)
            attempts += 1

        message_text = "Weather data was retrieved in " + str(attempts) + " attempt(s) from:\n" + self.url + "\n"
        print(message_text)
        # self.load_message.set(message_text)

        self.viewing_index = 0
        # self.weather_data_date.set("")
        # self.weather_data_forecast.set('Navigate using Forward/Backward.')

        return self.raw_data


    def translate_data(self, raw_data):
        temp_list_rename = []
        temp_temp_list_rename = []
        temp_dict_rename = {}
        for i, each in enumerate(raw_data.json()['properties']['periods']):
            # if each['name'] in self.shifted_week:
            #     temp_list_rename.append(i)
            #     temp_temp_list_rename.append(each['temperature'])
            #     temp_dict_rename[each['name']] = each['temperature']

            if each['name'] in self.temperature.keys() or " " in each['name']:  # exclude overnight, etc.
                if each['isDaytime']:  # ast.literal_eval(each['isDaytime'].capitalize())
                    self.temperature[each['name']][0] = each['temperature']
                else:
                    self.temperature[each['name'].split()[0]][1] = each['temperature']

        # {... 'Monday': [87, 70], 'Tuesday': [83, 68], 'Wednesday': [87, None]}
        # if None in [i for i, j in self.temperature.values()] or None in [j for i, j in self.temperature.values()]:
        #     print("{... 'Monday': [87, 70], 'Tuesday': [83, 68], 'Wednesday': [87, None]}")
        for i, each in enumerate(self.temperature.values()):
            if each[0] is None:
                self.temperature[self.shifted_week[i]][0] = raw_data.json()['properties']['periods'][0]['temperature']
            elif each[1] is None:
                self.temperature[self.shifted_week[i]][1] = raw_data.json()['properties']['periods'][0]['temperature']




        # print(temp_temp_list_rename)
        # print(temp_dict_rename)
        print(self.temperature)
        # TODO: passing around globals. don't do this. pass data between functions
        return self.temperature


    def graph_data(self, data_to_graph: dict):

        # temp_temp = [random.choice(range(60, 90)) for i in range(len(self.days_of_week))]
        high_temp = [data_to_graph[i][0] for i in self.shifted_week]
        low_temp = [data_to_graph[i][1] for i in self.shifted_week]
        # temp_temp_upper = [random.choice(range(8)) for i in range(len(self.shifted_week))]
        # temp_temp_lower = [random.choice(range(8)) for i in range(len(self.shifted_week))]

        x = self.shifted_week

        # temp_scatter = go.Figure(data=go.Scatter(
        #     x=x,
        #     y=y,
        #     error_y=dict(
        #         type='data',  # value of error bar given in data coordinates
        #         symmetric=False,
        #         arrayminus=low_temp,
        #         visible=True)
        # ))

        temp_scatter = go.Figure()

        temp_scatter.add_trace(go.Scatter(x=x, y=high_temp, name="spline", mode='lines', line_shape='spline', line=dict(color="red")))  # pycharm bug
        temp_scatter.add_trace(go.Scatter(x=x, y=low_temp, name="spline", mode='lines', line_shape='spline', line=dict(color="blue")))  # pycharm bug

        temp_scatter.update_layout(showlegend=False)

        margin = 1 + self.y_margin
        temp_range = [int(max(high_temp) * margin), int(min(low_temp) * margin)]
        # temp_scatter.update(layout_yaxis_range=temp_range)

        # temp_scatter.update_traces(hoverinfo='text+name', mode='lines+markers')
        # temp_scatter.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

        temp_scatter.show()

        return None


if __name__ == "__main__":
    app = WeatherApp('https://api.weather.gov/gridpoints/EWX/155,90/forecast')
    data = app.load_data()
    translated_data = app.translate_data(data)
    app.graph_data(translated_data)
