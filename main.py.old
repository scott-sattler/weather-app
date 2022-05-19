import requests
import time
import tkinter as tk
from tkinter import font
# from tkinter import *
from tkinter.constants import LEFT, RIGHT, CENTER


class Application:
    def __init__(self):
        # set up application window
        self.root = tk.Tk()
        self.root.geometry("450x400")
        #self.root.config(background="white")
        self.root.winfo_toplevel().title("Weather Application")
        self.root.wm_attributes('-toolwindow', 'True')  # removes title bar icon
        self.root.resizable(False, False)
        self.root.default_font = font.nametofont("TkDefaultFont")
        self.root.default_font.configure(size=12)
        self.frame = tk.Frame(self.root, width=400, height=100, background="gray34")

        # assign static and dynamic variables
        self.url = 'https://api.weather.gov/gridpoints/EWX/155,90/forecast'
        self.load_message = tk.StringVar()
        self.weather_data_date = tk.StringVar()
        self.weather_data_forecast = tk.StringVar()
        self.viewing_index = 0
        self.data = None

        # initialize / preload widget data
        self.load_message.set(" \n \n")  # to preserve formatting
        self.weather_data_date.set("")
        self.weather_data_forecast.set("Load weather data to begin.")

        # create widgets
        self.load_label = tk.Label(self.root,
                                   textvariable=self.load_message)
        self.weather_button = tk.Button(self.frame,
                                        text="Load Weather Data",
                                        command=self.load_data)
        self.browse_button_forward = tk.Button(self.frame,
                                               text="Forward",
                                               command=lambda: self.browse_data(1))
        self.browse_button_backward = tk.Button(self.frame,
                                                text="Backward",
                                                command=lambda: self.browse_data(-1))
        self.display_title = tk.Label(self.root,
                                      text="Forecast")
        self.display_label_1 = tk.Label(self.root,
                                        textvariable=self.weather_data_date)
        self.display_label_2 = tk.Label(self.root,
                                        textvariable=self.weather_data_forecast)

        # configure and format/style
        self.display_title.config(font=("arial", 20, "bold"))
        self.display_label_2.config(wraplength=300, justify="center")

        self.frame.pack(padx=10, pady=15)
        self.weather_button.pack(side='left', padx=10, pady=10)
        self.browse_button_forward.pack(side='right', padx=10, pady=10)
        self.browse_button_backward.pack(side='right')
        self.load_label.pack()
        self.display_title.pack()
        self.display_label_1.pack()
        self.display_label_2.pack()

        # mainloop
        self.root.mainloop()

    def load_data(self):
        self.data = requests.get(self.url)
        status_code = self.data.status_code
        attempts = 1
        time_between_requests = 2

        # attempts to retrieve data until success
        while status_code != 200:
            self.data = requests.get(self.url)
            status_code = self.data.status_code
            time.sleep(time_between_requests)
            attempts += 1

        message_text = "Weather data was retrieved in " + str(attempts) + " attempt(s) from:\n" + self.url + "\n"
        self.load_message.set(message_text)

        self.viewing_index = 0
        self.weather_data_date.set("")
        self.weather_data_forecast.set('Navigate using Forward/Backward.')

    def browse_data(self, value):
        # checks data is loaded
        if self.data is not None:
            self.viewing_index += value
            data_list_length = len(self.data.json()['properties']['periods'])
            # boundary tests for list traversal
            if (self.viewing_index > -1) and (self.viewing_index < data_list_length):
                date = self.data.json()['properties']['periods'][self.viewing_index]['startTime'][0:10]
                name = self.data.json()['properties']['periods'][self.viewing_index]['name']
                text_output = name + ": " + date
                self.weather_data_date.set(text_output)
                self.weather_data_forecast.set(
                    self.data.json()['properties']['periods'][self.viewing_index]['detailedForecast'])
            else:
                self.weather_data_date.set("")
                self.weather_data_forecast.set("No additional data.")
                if self.viewing_index < 0:
                    self.viewing_index = -1
                else:
                    self.viewing_index = data_list_length


app = Application()

