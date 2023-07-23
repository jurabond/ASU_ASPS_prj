import mysql.connector
from modules.config import db_config
import datetime

def get_all_events(station_id=None):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor(dictionary=True)

        if station_id is None:
            query = "SELECT * FROM station_events ORDER BY event_time DESC"
            cursor.execute(query)
        else:
            query = "SELECT * FROM station_events WHERE station_id = %s ORDER BY event_time DESC"
            cursor.execute(query, (station_id,))

        rows = cursor.fetchall()

        cursor.close()
        cnx.close()

        return rows

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return []

def add_event(event_text, station_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        query = "INSERT INTO station_events (event, event_time, station_id) VALUES (%s, %s, %s)"
        timestamp = datetime.datetime.now()
        data = (event_text, timestamp, station_id)

        cursor.execute(query, data)
        cnx.commit()

        cursor.close()
        cnx.close()

        return True

    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return False
