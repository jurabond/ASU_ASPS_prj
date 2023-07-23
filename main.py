from modules import login, main_page

def main():
    # Створення вікна авторизації
    login_window = login.LoginWindow()

    # Запуск головного циклу вікна авторизації
    login_window.mainloop()

    # Перевірка, чи була успішна авторизація
    if login_window.is_authenticated():
        print("Авторизація пройшла успішно!")

        # Отримання інформації про користувача
        username = login_window.get_username()

        # Виклик функції головної сторінки та передача інформації про користувача
        main_page.show_main_page(username)

    else:
        print("Помилка авторизації!")

if __name__ == "__main__":
    main()