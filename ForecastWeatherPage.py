import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime, date, timedelta

from CommonUtils import get_location
from RequestHandler import get_regular_forecast


class ForecastWeatherPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='gray26')
        label = tk.Label(self, text="Sprawdź prognozę pogody do 7 dni w przód z Open Weather", background='gray26',
                         foreground='gray87', font=('Timeless', 30))
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Wróć",
                           bg='gray26', fg='gray87',
                           width='35',
                           height='2',
                           font=('Courier New', 15, 'bold'),
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=(40, 10))

        self.current_city = get_location()
        self.city_text = tk.StringVar(self, value=self.current_city)
        city_entry = tk.Entry(self, textvariable=self.city_text, width='19',
                              font=('Courier New', 35, 'bold'),
                              justify=tk.CENTER)
        city_entry.pack(pady=10)

        time_now = datetime.now()
        time_max = date.today() + timedelta(days=7)

        self.calendar = DateEntry(self, width=43, justify=tk.CENTER, background='gray80', foreground='white', borderwidth=2,
                                  mindate=time_now, maxdate=time_max, dateformat=3, font=('Courier New', 15, 'bold'))
        self.calendar.pack(pady=10)

        check_current_weather_button = tk.Button(self, text="Sprawdź",
                                                 bg='gray26', fg='gray87',
                                                 width='35',
                                                 height='2',
                                                 font=('Courier New', 15, 'bold'),
                                                 command=self.check_forecast_weather_for_city)
        check_current_weather_button.pack(pady=10)

        self.location_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.location_lbl.pack()

        self.temp_lbl = tk.Label(self, text='', font=('Courier New', 15), bg='gray26', fg='white')
        self.temp_lbl.pack()

        self.pressure_lbl = tk.Label(self, text='', font=('Courier New', 15), bg='gray26', fg='white')
        self.pressure_lbl.pack()

        self.humidity_lbl = tk.Label(self, text='', font=('Courier New', 15), bg='gray26', fg='white')
        self.humidity_lbl.pack()

        self.wind_speed_lbl = tk.Label(self, text='', font=('Courier New', 15), bg='gray26', fg='white')
        self.wind_speed_lbl.pack()

        self.weather_lbl = tk.Label(self, text='', font=('Courier New', 15), bg='gray26', fg='white')
        self.weather_lbl.pack()

        self.canvas = tk.Canvas(self, bg='gray26', bd=0, highlightthickness=0)
        self.canvas.pack(pady=10)

    def check_forecast_weather_for_city(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        weather_icons = os.path.join(cur_dir, 'weather_icons/')
        city = self.city_text.get()
        date_forecast = self.calendar.get_date()
        date_difference = date_forecast - date.today()
        weather = get_regular_forecast(city, date_difference.days)

        if weather:
            self.location_lbl['text'] = 'Location: {}, {}'.format(weather[0], weather[1])
            self.img = ImageTk.PhotoImage(Image.open(weather_icons + '{}.png'.format(weather[3])))
            self.canvas.create_image(0, 0, anchor="nw", image=self.img)
            self.canvas.image = self.img
            self.canvas.configure(bg='skyblue')
            self.temp_lbl['text'] = 'Temperature: {:.2f}°C'.format(weather[2])
            self.weather_lbl['text'] = 'Weather description: {}'.format(weather[5])
            self.pressure_lbl['text'] = 'Ciśnienie: {} hPa'.format(weather[6])
            self.humidity_lbl['text'] = 'Wilgotność: {} %'.format(weather[7])
            self.wind_speed_lbl['text'] = 'Wind speed: {} m/s'.format(weather[8])
        else:
            messagebox.showerror('Error', 'Cannot find city {}'.format(city))
