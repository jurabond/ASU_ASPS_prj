import unittest
from unittest.mock import patch, Mock
import modules.check_value as check_value
import modules.station as station

class TestCheckValues(unittest.TestCase):

    @patch('modules.station.get_station_data')
    @patch('modules.station.turn_off_station')
    @patch('tkinter.messagebox.askquestion')  # Змінили на 'tkinter.messagebox.askquestion'
    def test_check_values(self, mock_askquestion, mock_turn_off_station, mock_get_station_data):
        # Припустимо, що станція повертає дані з підвищеною температурою і навантаженням
        mock_get_station_data.return_value = {"Activity": "Активна", "Temperature": 50, "Load": 90}

        # Припустимо, що користувач завжди відповідає "yes" на запитання про вимкнення станції
        mock_askquestion.return_value = "yes"

        # Запустимо check_values в окремому потоці, так як він має нескінченний цикл
        import threading
        check_values_thread = threading.Thread(target=check_value.check_values)
        check_values_thread.start()

        # Дочекаємось, поки функція check_values не виконає один цикл перевірки
        import time
        time.sleep(1)

        # Зупинимо виконання check_values
        check_values_thread.join(timeout=1)
        if check_values_thread.is_alive():
            raise Exception("check_values function is still running. It should have stopped by now.")

        # Перевіримо, що функція turn_off_station була викликана для кожної станції
        mock_turn_off_station.assert_has_calls([unittest.mock.call(i) for i in range(1, 5)])

if __name__ == "__main__":
    unittest.main()
