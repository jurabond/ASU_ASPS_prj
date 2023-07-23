import mysql.connector
from modules import config

def create_table():
    try:
        # Встановлення з'єднання з базою даних
        conn = mysql.connector.connect(**config.db_config)
        cursor = conn.cursor()

        # Запит на створення таблиці
        query = """
        CREATE TABLE polzovatel (
            id INT AUTO_INCREMENT PRIMARY KEY,
            polzovatel VARCHAR(255) NOT NULL,
            parol VARCHAR(255) NOT NULL,
            dostup INT NOT NULL
        )
        """
        cursor.execute(query)

        # Додавання користувача
        insert_query = "INSERT INTO polzovatel (polzovatel, parol, dostup) VALUES (%s, %s, %s)"
        values = ("admin", "0000", 1)
        cursor.execute(insert_query, values)

        # Підтвердження змін
        conn.commit()

        # Закриття з'єднання з базою даних
        cursor.close()
        conn.close()

        print("Таблиця створена та користувач доданий.")

    except mysql.connector.Error as err:
        print("Помилка створення таблиці або додавання користувача:", err)

# Виклик функції для створення таблиці та додавання користувача
create_table()