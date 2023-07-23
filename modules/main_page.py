import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import datetime
import modules.station as station
import modules.event as event_module
import modules.random_module as random_module
import modules.check_value as check_value
import threading
import sys
import os
import webbrowser

def send_email(to, subject, body):
    webbrowser.open(f"mailto:{to}?subject={subject}&body={body}")
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainPage(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.configure(bg="#f2f2f2")
        self.username = username
        self.station_tags = ["station_1", "station_2", "station_3", "station_4"]

        self.active_img = ImageTk.PhotoImage(Image.open(resource_path("modules/active.png")))
        self.inactive_img = ImageTk.PhotoImage(Image.open(resource_path("modules/inactive.png")))

        self.create_widgets()
        self.update_clock()
        self.update_stations()
        self.update_event_log()
        #self.generator = random_module.RandomValueGenerator()  # Ініціалізація генератора випадкових значень
        #self.generator.start()  # Запуск генератора випадкових значень
        #self.master.protocol("WM_DELETE_WINDOW", self.on_closing)  # Функція для виконання при виході з програми
        self.start_value_checking_thread()


#    def on_closing(self):
#        self.generator.stop()  # Зупинка генератора випадкових значень при закритті програми
#        self.master.destroy()

    def start_value_checking_thread(self):
        # Запуск перевірки значень в окремому потоці
        value_checking_thread = threading.Thread(target=check_value.check_values)
        value_checking_thread.daemon = True  # Встановлення флагу daemon, щоб потік автоматично завершився після закриття програми
        value_checking_thread.start()

    def create_widgets(self):
        # Заголовок сторінки
        header_label = tk.Label(self, text="Схема районів та підстанцій", font=("Arial", 16), bg="#f2f2f2")
        header_label.grid(row=0, column=0, columnspan=5, pady=20)

        # Ліва частина (карта та кнопки викликів)
        left_frame = tk.Frame(self, bg="#f2f2f2")
        left_frame.grid(row=1, column=0, sticky="n")

        # Створення холста
        self.canvas = tk.Canvas(left_frame, width=500, height=500)
        self.canvas.pack()

        # Відображення карти
        img = Image.open(resource_path("modules/map.png"))   # Замініть на шлях до вашої карти
        self.map_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.map_img, anchor="nw")

        # Розділення карти на регіони
        self.canvas.create_line(250, 0, 250, 500)  # Вертикальна лінія
        self.canvas.create_line(0, 250, 500, 250)  # Горизонтальна лінія

        # Відображення підстанцій
        self.canvas.create_image(50, 50, image=self.active_img, tags="station_1")  # Підстанція 1
        self.canvas.create_image(400, 50, image=self.active_img, tags="station_2")  # Підстанція 2
        self.canvas.create_image(50, 400, image=self.active_img, tags="station_3")  # Підстанція 3
        self.canvas.create_image(400, 400, image=self.active_img, tags="station_4")  # Підстанція 4

        self.canvas.tag_bind("station_1", "<Button-1>", self.open_station_info)
        self.canvas.tag_bind("station_2", "<Button-1>", self.open_station_info)
        self.canvas.tag_bind("station_3", "<Button-1>", self.open_station_info)
        self.canvas.tag_bind("station_4", "<Button-1>", self.open_station_info)

        # Кнопки "Виклик інженера" та "Виклик начальства"
        button_frame = tk.Frame(left_frame, bg="#f2f2f2")
        button_frame.pack(pady=10)

        engineer_button = tk.Button(button_frame, text="Виклик інженера", command=self.call_engineer, width=15)
        engineer_button.pack(side="left", padx=10)

        manager_button = tk.Button(button_frame, text="Виклик начальства", command=self.call_manager, width=15)
        manager_button.pack(side="left", padx=10)

        # Права частина (інформація про користувача, дату, час та журнал подій)
        right_frame = tk.Frame(self, bg="#f2f2f2")
        right_frame.grid(row=1, column=1, sticky="n")

        # Інформація про користувача, дату та час
        user_info = tk.StringVar()
        user_info.set(f"Користувач: {self.username}")
        user_label = tk.Label(right_frame, textvariable=user_info, font=("Arial", 12), bg="#f2f2f2")
        user_label.pack(padx=10, pady=5, anchor="w")

        self.date_info = tk.StringVar()
        date_label = tk.Label(right_frame, textvariable=self.date_info, font=("Arial", 12), bg="#f2f2f2")
        date_label.pack(padx=10, pady=5, anchor="w")

        self.time_info = tk.StringVar()
        time_label = tk.Label(right_frame, textvariable=self.time_info, font=("Arial", 12), bg="#f2f2f2")
        time_label.pack(padx=10, pady=5, anchor="w")

        self.voltage_info = tk.StringVar()
        voltage_label = tk.Label(right_frame, textvariable=self.voltage_info, font=("Arial", 12), bg="#f2f2f2")
        voltage_label.pack(padx=10, pady=5, anchor="w")

        # Журнал подій
        event_log_label = tk.Label(right_frame, text="Журнал подій:", font=("Arial", 12), bg="#f2f2f2")
        event_log_label.pack(padx=10, pady=5, anchor="w")

        self.event_log = ScrolledText(right_frame, width=40, height=20, font=("Arial", 12))
        self.event_log.pack(padx=10, pady=5)

    def open_station_info(self, event):
        station_id = self.canvas.gettags("current")[0].split("_")[1]
        x, y = event.x_root, event.y_root
        station.show_station_info(station_id, x, y)
        print(f"Station ID: {station_id}")


    def update_stations(self):
        for tag in self.station_tags:
            station_id = tag.split("_")[1]
            data = station.get_station_data(station_id)
            img = self.active_img if data["Activity"] == "Активна" else self.inactive_img
            self.canvas.itemconfig(tag, image=img)
        self.master.after(1000, self.update_stations)


    def update_clock(self):
        date = datetime.date.today().strftime("%d.%m.%Y")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        self.date_info.set(f"Дата: {date}")
        self.time_info.set(f"Час: {time}")

        voltage = station.get_station_data(0).get("voltage")
        #voltage = random_module.generate_random_values()  # Використання вашої функції generate_random_values
        self.voltage_info.set(f"Напруга: {voltage}")

        self.master.after(1000, self.update_clock)


    def update_event_log(self):
        events = event_module.get_all_events()
        self.event_log.delete("1.0", tk.END)
        for event in events:
            event_text = event['event']
            station_id = event['station_id']
            if station_id != 0:
                station_info = f" - {station_id} підстанція"
                event_text += station_info
            log_entry = f"[{event['event_time']}] {event_text}\n"
            self.event_log.insert(tk.END, log_entry)
        self.master.after(1000, self.update_event_log)


    def call_engineer(self):
        to = "engineer@example.com"  # Email інженера
        subject = "Виклик інженера"
        body = f"Виклик інженера від користувача: {self.username}"
        send_email(to, subject, body)
        station_id = "0"  # Замініть на потрібне значення для відповідної станції
        event_module.add_event("Виклик інженера", station_id)

    def call_manager(self):
        to = "manager@example.com"  # Email начальника
        subject = "Виклик начальства"
        body = f"Виклик начальства від користувача: {self.username}"
        send_email(to, subject, body)
        station_id = "0"  # Замініть на потрібне значення для відповідної станції
        event_module.add_event("Виклик начальства", station_id)

def show_main_page(username):
    window = tk.Tk()
    window.title("Головна сторінка")
    window.geometry("900x700")

    main_page = MainPage(window, username)
    main_page.pack(expand=True, fill="both")

    window.mainloop()

# Приклад виклику головної сторінки
if __name__ == "__main__":
    username = "admin"  # Замініть на реальне ім'я користувача
    show_main_page(username)