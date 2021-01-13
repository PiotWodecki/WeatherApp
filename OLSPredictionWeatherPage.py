import tkinter as tk
from tkinter import messagebox

from CommonUtils import create_df_from_statistical_data, show_correlations, derive_nth_day_feature, \
    handle_col_to_remove, create_backward_elimination, create_file_with_ols, open_notepad, get_location
from RequestHandler import get_statistical_data


class OLSPredictionWeatherPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='gray26')
        label = tk.Label(self, text="Pokaż model regresji liniowej dla miasta", background='gray26',
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
                                                 command=self.create_ols_for_city)
        check_current_weather_button.pack(pady=10)

        self.info_lbl = tk.Label(self, text='', font=('Courier New', 18, 'bold'), bg='gray26', fg='white')
        self.info_lbl.pack(pady=(50,10))

    def create_ols_for_city(self):
        city = self.city_text.get()
        weather_data = get_statistical_data(city)
        if weather_data:
            df = create_df_from_statistical_data(weather_data)
            corrs = show_correlations(df)
            df = derive_nth_day_feature(df, df.columns, 3)
            df = handle_col_to_remove(df)
            ols_data_to_print = create_backward_elimination(df, 'meantemp')
            create_file_with_ols(city, corrs, ols_data_to_print)
            open_notepad()
            self.info_lbl['text'] = "Model został zapisany do pliku OLS.txt"
        else:
            messagebox.showerror('Error', 'Cannot find city {}'.format(city))
