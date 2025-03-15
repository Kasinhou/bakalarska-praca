import sqlite3

DB_PATH = 'database.db'

def get_data():
    with sqlite3.connect(DB_PATH) as connection:
        print("Successfully connected!")
        cursor = connection.cursor()
        
        cursor.execute(
            '''SELECT d.name, d.reliability, d.description, t.type_name, t.description, di.size, di.weight, di.max_speed, max_altitude 
            FROM drones d 
            JOIN drone_types dt ON d.id = dt.drone_id 
            JOIN types t ON dt.type_id = t.id
            JOIN drone_information di ON d.id = di.drone_id'''
        )

        results = cursor.fetchall()

    return results