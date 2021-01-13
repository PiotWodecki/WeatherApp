import tkinter as tk
from tkinter import messagebox

from CommonUtils import create_df_from_statistical_data, show_correlations, derive_nth_day_feature, \
    handle_col_to_remove, create_backward_elimination, create_file_with_ols, open_notepad, get_location
from RequestHandler import get_statistical_data, get_current_air_pollution_data


class CurrentAirPolutionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='gray26')
        label = tk.Label(self, text="Pokaż obecne zanieczyszczenia", background='gray26',
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

        check_current_weather_button = tk.Button(self, text="Sprawdź",
                                                 bg='gray26', fg='gray87',
                                                 width='35',
                                                 height='2',
                                                 font=('Courier New', 15, 'bold'),
                                                 command=self.display_air_polution)
        check_current_weather_button.pack(pady=10)

        self.co_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.co_lbl.pack(pady=10)

        self.no_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.no_lbl.pack(pady=10)

        self.o3_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.o3_lbl.pack(pady=10)

        self.so2_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.so2_lbl.pack(pady=10)

        self.pm_2_5_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.pm_2_5_lbl.pack(pady=10)

        self.pm10_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.pm10_lbl.pack(pady=10)

        self.nh3_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.nh3_lbl.pack(pady=10)

    def display_air_polution(self):
        city = self.city_text.get()
        polutions = get_current_air_pollution_data(city)

        if polutions:
            self.co_lbl['text'] = 'Koncentracja tlenku węgla CO: {} μg/m3'.format(polutions[0])
            self.no_lbl['text'] = 'Koncentracja tlenku azotu NO: {} μg/m3'.format(polutions[1])
            self.o3_lbl['text'] = 'Koncentracja dwutlenku azotu NO2: {} μg/m3'.format(polutions[2])
            self.so2_lbl['text'] = 'Koncentracja ozonu O3: {} μg/m3'.format(polutions[3])
            self.pm_2_5_lbl['text'] = 'Koncentracja dwutlenku siarki SO2: {} μg/m3'.format(polutions[4])
            self.pm10_lbl['text'] = 'Koncentracja pyłu zawieszone PM2.5: {} μg/m3'.format(polutions[5])
            self.nh3_lbl['text'] = 'Koncentracja pyłu zawieszone PM10: {} μg/m3'.format(polutions[6])
        else:
            messagebox.showerror('Error', 'Cannot find city {}'.format(city))
