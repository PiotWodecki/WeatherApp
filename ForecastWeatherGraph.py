import os
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from RequestHandler import get_forecast_for_plot


class ForecastWeatherGraph(tk.Frame):

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
        button.pack(pady=(40, 10))

        self.city_text = tk.StringVar()
        city_entry = tk.Entry(self, textvariable=self.city_text, width='19',
                              font=('Courier New', 35, 'bold'),
                              justify=tk.CENTER)
        city_entry.pack(pady=10)

        check_current_weather_button = tk.Button(self, text="Sprawdź",
                                                 bg='gray26', fg='gray87',
                                                 width='35',
                                                 height='2',
                                                 font=('Courier New', 15, 'bold'),
                                                 command=self.plot_forecast)
        check_current_weather_button.pack(pady=10)
        self.photo = tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Plots/', 'plot1.png'))

        #######################
        # self.canvas = tk.Canvas(self, width=600, height=350)
        # self.canvas.pack(fill=tk.BOTH, expand =1)

    def plot_forecast(self):
        city = self.city_text.get()
        weather_df = get_forecast_for_plot(city)

        if weather_df:
            weather_df = weather_df.set_index('Dates')
            fig, ax = plt.subplots()
            ax.plot(weather_df)
            plt.xticks(rotation=60)
            plt.xlabel('Dzień', fontsize=18)
            plt.ylabel('Temperatura', fontsize=18)
            ax.set_ylabel('Temperatura ($^\circ$C)')

            cur_dir = os.path.dirname(os.path.abspath(__file__))
            plots_dir = os.path.join(cur_dir, 'Plots/', 'plot1.png')

            plt.grid()
            fig.savefig(plots_dir, transparent=True, bbox_inches='tight')

            self.img = Image.open(plots_dir)
            self.img = self.img.resize((600, 350), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            panel = tk.Label(self, image=self.img)
            panel.pack(side=tk.TOP, pady=10)
        ##to działą!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        # self.canvas.create_image(0,0, anchor=tk.CENTER, image=img)
        # self.canvas.image = img
        #################################################
        else:
            messagebox.showerror('Error', 'Cannot find city {}'.format(city))



