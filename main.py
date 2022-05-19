import plotly.graph_objects as go
import requests
import time
import datetime


class WeatherApp:
    def __init__(self, url):
        self.__days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        self.url: str = url
        self.raw_data: dict = {}
        self.temperature = {str: [int, int]}  # {day: [high, low]}

        # have seven-day period start today, not monday
        today_date = datetime.datetime.today()
        weekday_index = datetime.datetime.weekday(today_date)
        dow = self.__days_of_week
        self.shifted_week = [dow[(i + weekday_index) % len(dow)] for i in range(len(dow))]

        # construct temperature dict
        self.temperature = {k: [None, None] for k in self.shifted_week}

        # configuration
        self.y_margin = 5  # degrees

    def load_data(self, url: str | None = None):
        if url is None:
            url = self.url
        raw_data = requests.get(url)
        status_code = raw_data.status_code
        attempts = 1
        time_between_requests = 2

        # attempts to retrieve data until success
        while status_code != 200:
            raw_data = requests.get(url)
            status_code = raw_data.status_code
            time.sleep(time_between_requests)
            attempts += 1

        message_text = f"Weather data was retrieved in {str(attempts)} attempt(s) from:\n{url}\n"
        print(message_text)  # TODO: remove

        return raw_data

    # this function isolates API data format incompatibilities
    # default: GeoJSON (RFC 7946) @ https://datatracker.ietf.org/doc/html/rfc7946
    def translate_data(self, raw_data):
        # pattern matching solution (unknown 1-3 then alternating high/low)
        # reason: updating not real time; inconsistent format

        # find the first recognized 'name'
        start_index, flag = 0, False
        for i, each_datum in enumerate(raw_data.json()['properties']['periods']):
            if flag or each_datum['name'] in self.__days_of_week:
                start_index, flag = i, True
                break

        # transpose data starting at first recognized 'name' (day of week)
        data_list = list(raw_data.json()['properties']['periods'])
        temperature_list = list(self.temperature.values())  # values isolated for modification
        # initial index assignments
        transfer_index = self.shifted_week.index(data_list[start_index]['name'])
        data_index = start_index
        binary_index = 0
        for i in range(len(data_list)):
            temperature_list[transfer_index][binary_index] = data_list[data_index].get(
                'temperature')  # noqa ['temperature'] pycharm error
            # update indices
            transfer_index = (transfer_index + binary_index) % len(temperature_list)
            data_index = (data_index + 1) % len(data_list)
            binary_index = (binary_index + 1) % 2

        # print(temperature_list)
        # print(temperature_list is self.temperature)
        # print(temperature_list[0][1] is self.temperature[list(self.temperature.keys())[0]])
        # print(temperature_list[0] is self.temperature[list(self.temperature.keys())[0]])
        # print(self.temperature)
        # # TODO: passing around globals. don't do this. pass data between functions

        return self.temperature

    def graph_data(self, data_to_graph: dict):
        high_temp = [data_to_graph[i][0] for i in self.shifted_week]
        low_temp = [data_to_graph[i][1] for i in self.shifted_week]
        x = self.shifted_week

        temp_scatter = go.Figure()

        temp_scatter.add_trace(go.Scatter(
            x=x,
            y=high_temp,
            name="spline",
            mode='lines',
            line_shape='spline',
            line=dict(color="red")
        ))  # pycharm bug
        temp_scatter.add_trace(go.Scatter(
            x=x,
            y=low_temp,
            name="spline",
            mode='lines',
            line_shape='spline',
            line=dict(color="blue"),
            fill='tonexty',
            fillcolor='gold'
        ))  # pycharm bug

        temp_scatter.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="LightSteelBlue",
            showlegend=False,
            xaxis_range=[-.5, 6.5]
        )

        temp_range = [min(low_temp) - self.y_margin, max(high_temp) + self.y_margin]
        temp_scatter.update(layout_yaxis_range=temp_range)

        # temp_scatter.update_traces(hoverinfo='text+name', mode='lines+markers')
        # temp_scatter.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

        temp_scatter.show()

        return None


if __name__ == "__main__":
    app = WeatherApp('https://api.weather.gov/gridpoints/EWX/155,90/forecast')
    data = app.load_data()
    translated_data = app.translate_data(data)
    app.graph_data(translated_data)
