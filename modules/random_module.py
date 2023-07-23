import random
import mysql.connector
import time
import threading
from modules.config import db_config

class RandomValueGenerator:

    def __init__(self):
        self.running = False
        self.thread = threading.Thread(target=self.generate_random_values, daemon=True)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

    def generate_random_values(self):
        while self.running:
            cnx = mysql.connector.connect(**db_config)
            cursor = cnx.cursor(dictionary=True)
            # Update values for each station
            station_ids = [0, 1, 2, 3, 4]
            for station_id in station_ids:
                temperature = random.randint(20, 46)
                load = random.randint(50, 81)
                voltage = random.uniform(40000, 40050)

                self.update_station_values(cursor, cnx, station_id, temperature, load)
                self.update_station_voltage(cursor, cnx, station_id, voltage)
            cursor.close()
            cnx.close()

            time.sleep(5)

    def update_station_values(self, cursor, cnx, station_id, temperature, load):
        try:
            query = "UPDATE stations SET Temperature = %s, `Load` = %s WHERE ID = %s"
            cursor.execute(query, (temperature, load, station_id))
            cnx.commit()

        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")

    def update_station_voltage(self, cursor, cnx, station_id, voltage):
        try:
            query = "UPDATE stations SET Voltage = %s WHERE ID = %s"
            cursor.execute(query, (voltage, station_id))
            cnx.commit()

        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
