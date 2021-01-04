import tkinter as tk


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='gray26')
        label = tk.Label(self, text="Witamy w aplikacji pogodowej!", background='gray26',
                         foreground='gray87', font=('Timeless', 30))
        label.pack(side="top", fill="x", pady=10)
        '#22b455'
        self.button1 = tk.Button(self, text="Sprawdź obecną pogodę",bg='gray26', fg='gray87',
                                 width='35',
                                 height='2',
                                 font=('Courier New', 15, 'bold'),
                                 command=lambda: controller.show_frame("CurrentWeatherPage"))

        self.button1.pack(pady=(40, 10))

        self.button2 = tk.Button(self, text="Sprawdź prognozę pogody dla 1 dnia",bg='gray26', fg='gray87',
                                 width='35',
                                 height='2',
                                 font=('Courier New', 15, 'bold'),
                                 command=lambda: controller.show_frame("ForecastWeatherPage"))
        self.button2.pack(pady=10)

        self.button3 = tk.Button(self, text="Wykres dla prognozy pogody", bg='gray26', fg='gray87',
                                 width='35',
                                 height='2',
                                 font=('Courier New', 15, 'bold'),
                                 command=lambda: controller.show_frame("ForecastWeatherGraph"))

        self.button3.pack(pady=10)

