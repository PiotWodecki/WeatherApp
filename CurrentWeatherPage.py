import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from CommonUtils import get_location
from RequestHandler import get_weather


class CurrentWeatherPage(tk.Frame):

    #creating view of frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='gray26')
        label = tk.Label(self, text="Sprawdź obecną pogodę z Open Weather", background='gray26',
                         foreground='gray87', font=('Timeless', 30))
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Wróć",
                           bg='gray26', fg='gray87',
                           width='35',
                           height='2',
                           font=('Courier New', 15, 'bold'),
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(pady=(30, 10))

        self.current_city = get_location()
        self.city_text = tk.StringVar(self, value=self.current_city)
        city_entry = tk.Entry(self, textvariable=self.city_text, width='19',
                              font=('Courier New', 35, 'bold'),
                              justify=tk.CENTER)
        city_entry.pack(pady=10)

        check_current_weather_button = tk.Button(self, text="Sprawdź",
                                                 bg='gray26', fg='gray87',
                                                 width='35',
                                                 height='2',
                                                 font=('Courier New', 15, 'bold'),
                                                 command=self.check_current_weather_for_city)
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

    def check_current_weather_for_city(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        weather_icons = os.path.join(cur_dir, 'weather_icons/')
        city = self.city_text.get()
        weather = get_weather(city)

        if weather:
            self.location_lbl['text'] = 'Location: {}, {}'.format(weather[0], weather[1])
            img = ImageTk.PhotoImage(Image.open(weather_icons + '{}.png'.format(weather[3])))
            self.canvas.create_image(20, 20, anchor=tk.NW, image=img)
            self.canvas.image = img
            self.canvas.configure(bg='skyblue')
            self.temp_lbl['text'] = 'Temperature: {:.2f}°C'.format(weather[2])
            self.weather_lbl['text'] = 'Weather description: {}'.format(weather[5])
            self.pressure_lbl['text'] = 'Ciśnienie: {} hPa'.format(weather[6])
            self.humidity_lbl['text'] = 'Wilgotność: {} %'.format(weather[7])
            self.wind_speed_lbl['text'] = 'Wind speed: {} m/s'.format(weather[8])
        else:
            messagebox.showerror('Error', 'Cannot find city {}'.format(city))
