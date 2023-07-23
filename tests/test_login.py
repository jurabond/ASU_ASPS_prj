#Цей тест перевіряє поведінку методу login_button_click у класі LoginWindow. Саме цей метод відповідає за процес авторизації користувача.

#Ось основні етапи тесту:

#1. Створення моків (mocks): Тест створює "моки" для декількох методів і функцій, які використовуються в login_button_click. Це включає методи showinfo та showerror з messagebox (для відображення повідомлень користувачу), метод login класу LoginWindow (для перевірки авторизаційних даних користувача) та методи get для об'єктів username_entry та password_entry (для отримання введених користувачем даних).
#2.Налаштування моків: Тест вказує мокам, як повинні вести себе їхні методи. Наприклад, моки username_entry та password_entry налаштовані так, щоб повертати певні значення, коли їх метод get викликаний. Також налаштовується поведінка моку login, щоб він завжди повертав True, що означає, що авторизація пройшла успішно.
#3. Виклик методу: Тест викликає метод login_button_click, який має використовувати моки замість реальних об'єктів та методів.
#4. Перевірка результату: Після виклику методу тест перевіряє, чи були викликані моки відповідним чином. Він перевіряє, чи були викликані методи get для username_entry та password_entry, чи був викликаний метод login з правильними аргументами, та чи був викликаний showinfo (що відповідає успішній авторизації). Також перевіряється, що showerror не був викликаний, оскільки мок login налаштований повертати True.
#Цей тест перевіряє, чи правильно метод login_button_click використовує свої залежності (тобто інші методи та об'єкти) для виконання своєї роботи. Це допомагає виявити проблеми в коді, якщо метод не використовує свої залежності правильно.

import unittest
from unittest.mock import patch, create_autospec
import tkinter as tk
import modules.login as login
from tkinter import messagebox

class TestLogin(unittest.TestCase):
    @patch.object(messagebox, 'showinfo')
    @patch.object(messagebox, 'showerror')
    @patch.object(login.LoginWindow, 'login')
    def test_login_button_click(self, mock_login, mock_showerror, mock_showinfo):
        # Створимо екземпляр LoginWindow з мокнутими методами
        lw = login.LoginWindow()
        lw.username_entry = create_autospec(tk.Entry, instance=True)
        lw.password_entry = create_autospec(tk.Entry, instance=True)

        # Встановимо повернення значень для get()
        lw.username_entry.get.return_value = 'username'
        lw.password_entry.get.return_value = 'password'

        # Що поверне login
        mock_login.return_value = True

        # Викликаємо метод
        lw.login_button_click()

        # Перевіряємо, чи були викликані наші моки з правильними аргументами
        lw.username_entry.get.assert_called_once()
        lw.password_entry.get.assert_called_once()
        mock_login.assert_called_once_with('username', 'password')
        mock_showinfo.assert_called_once_with('Успішна авторизація', 'Авторизація пройшла успішно!')
        mock_showerror.assert_not_called()

if __name__ == "__main__":
    unittest.main()
