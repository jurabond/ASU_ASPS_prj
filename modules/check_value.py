import time
import tkinter as tk
from tkinter import messagebox
import modules.station as station
from modules.station import turn_off_station

def check_values():
    # Ініціалізація флагів оповіщень для кожної станції
    alert_flags = {1: {"temperature": False, "load": False},
                   2: {"temperature": False, "load": False},
                   3: {"temperature": False, "load": False},
                   4: {"temperature": False, "load": False}}

    while True:
        # Отримання значень температури та навантаження для кожної підстанції
        station_ids = [1, 2, 3, 4]
        for station_id in station_ids:
            data = station.get_station_data(station_id)
            activity = data.get("Activity")
            temperature = int(data.get("Temperature"))
            load = int(data.get("Load"))

            # Перевірка граничних значень температури та навантаження
            if activity == "Активна":
                if temperature > 45 and not alert_flags[station_id]["temperature"]:
                    message = f"На підстанції {station_id} перевищена температура!"
                    answer = messagebox.askquestion("Попередження", message + "\nБажаєте вимкнути станцію?")
                    alert_flags[station_id]["temperature"] = True
                    if answer == "yes":
                        # Тут ви можете виконати дії для вимкнення станції
                        station.turn_off_station(station_id)
                elif temperature <= 45:
                    alert_flags[station_id]["temperature"] = False

                if load > 80 and not alert_flags[station_id]["load"]:
                    message = f"На підстанції {station_id} перевищене навантаження!"
                    answer = messagebox.askquestion("Попередження", message + "\nБажаєте вимкнути станцію?")
                    alert_flags[station_id]["load"] = True
                    if answer == "yes":
                        # Тут ви можете виконати дії для вимкнення станції
                        station.turn_off_station(station_id)
                elif load <= 80:
                    alert_flags[station_id]["load"] = False

        time.sleep(1)
