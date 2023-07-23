#Цей тест перевіряє, чи правильно працює функція turn_off_station() в модулі station. Ця функція відповідає за вимкнення певної станції в базі даних.

#Специфічно, цей тест перевіряє наступні речі:

#Чи викликається mysql.connector.connect() для встановлення з'єднання з базою даних.
#Чи виконується SQL-запит для оновлення стану активності станції в базі даних до "Неактивна".
#Чи виконується SQL-запит для додавання події "Неактивна" для відповідної станції в таблицю station_events в базі даних.
#Чи викликається метод commit() об'єкта mysql.connector.connect(), щоб зберегти зміни в базі даних.
#Чи викликається функція open() для запису в файл інформації про вимкнення станції.
#Усі ці перевірки виконуються за допомогою технології макетування (mocking), яка дозволяє імітувати роботу різних частин коду. Зауважте, що в цьому тесті реальна база даних або файлова система не використовуються - замість цього ми "імітуємо" їхню роботу. Це дозволяє зробити тест більш надійним і незалежним від зовнішніх факторів.

from unittest.mock import patch, MagicMock, mock_open
import unittest
import modules.station as station

class TestStation(unittest.TestCase):
    def setUp(self):
        self.patcher1 = patch('mysql.connector.connect')
        self.patcher2 = patch('os.getcwd')
        self.patcher3 = patch('builtins.open', new_callable=mock_open)
        self.mock_connect = self.patcher1.start()
        self.mock_getcwd = self.patcher2.start()
        self.mock_open = self.patcher3.start()
        self.mock_cursor = MagicMock()
        self.mock_connect().cursor.return_value = self.mock_cursor

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        self.patcher3.stop()

    def test_turn_off_station(self):
        self.mock_cursor.execute.side_effect = [True, True]
        self.mock_connect().commit.side_effect = [True, True]
        station.turn_off_station(1)
        self.mock_cursor.execute.assert_any_call("UPDATE stations SET Activity = %s WHERE ID = %s", ("Неактивна", 1))
        self.mock_cursor.execute.assert_any_call("INSERT INTO station_events (station_id, event) VALUES (%s, %s)", (1, "Неактивна"))
        self.mock_connect().commit.assert_called()
        self.mock_open.assert_called()





if __name__ == '__main__':
    unittest.main()

