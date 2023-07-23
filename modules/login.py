import tkinter as tk
import mysql.connector
from tkinter import messagebox

from modules import config

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Авторизація")
        self.geometry("300x200")
        self.configure(bg="#f2f2f2")
        self.create_widgets()
        self.authenticated = False
        self.username = ""
        self.attempt_count = 0  # Додаємо лічильник спроб

    def create_widgets(self):
        # Налаштування стилів
        self.option_add("*Font", "Arial 12")

        # Елементи на вікні авторизації
        username_label = tk.Label(self, text="Логін:", bg="#f2f2f2")
        username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        password_label = tk.Label(self, text="Пароль:", bg="#f2f2f2")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self, text="Увійти", command=self.login_button_click, bg="#4caf50", fg="#ffffff")
        login_button.pack()

    def login(self, username, password):
        # Здійснення перевірки логіна та пароля у базі даних
        try:
            # Встановлення з'єднання з базою даних
            conn = mysql.connector.connect(**config.db_config)
            cursor = conn.cursor()

            # Виконання запиту на перевірку авторизаційних даних
            query = "SELECT polzovatel FROM polzovatel WHERE polzovatel = %s AND parol = %s"
            cursor.execute(query, (username, password))

            # Отримання результату запиту
            result = cursor.fetchone()

            # Закриття з'єднання з базою даних
            cursor.close()
            conn.close()

            # Перевірка результату запиту
            if result:
                self.authenticated = True
                self.username = result[0]
                return True
            else:
                return False

        except mysql.connector.Error as err:
            messagebox.showerror("Помилка з'єднання", str(err))
            return False

    def login_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.login(username, password):
            messagebox.showinfo("Успішна авторизація", "Авторизація пройшла успішно!")
            self.destroy()  # Закриття вікна авторизації після успішної авторизації
        else:
            self.attempt_count += 1  # Збільшуємо лічильник спроб
            if self.attempt_count >= 3:  # Якщо користувач зробив 3 невдалі спроби
                messagebox.showerror("Помилка авторизації", "Ви зробили три невдалі спроби входу. Програма буде закрита.")
                self.destroy()  # Закриття програми
            else:
                messagebox.showerror("Помилка авторизації", "Неправильний логін або пароль!")

    def is_authenticated(self):
        return self.authenticated

    def get_username(self):
        return self.username
