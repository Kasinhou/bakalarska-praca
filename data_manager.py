import sqlite3
from data_classes import Type, Drone, DroneInformation

DB_PATH = 'database.db'

def get_data():
    with sqlite3.connect(DB_PATH) as connection:
        print("Successfully connected!")
        cursor = connection.cursor()
        
        cursor.execute(
            '''SELECT d.name, d.reliability, d.description, t.type_name, t.description, di.size, di.weight, di.max_speed, max_altitude 
            FROM drones d 
            LEFT JOIN drone_types dt ON d.id = dt.drone_id 
            LEFT JOIN types t ON dt.type_id = t.id
            LEFT JOIN drone_information di ON d.id = di.drone_id'''
        )   

        results = cursor.fetchall()

        drones = []
        for row in results:
            name, reliability, description, type_name, type_description, size, weight, max_speed, max_altitude = row
            drone_type = Type(type_name, type_description)
            drone_information = DroneInformation(size, weight, max_speed, max_altitude)
            drone = Drone(name, reliability, drone_type, drone_information, description)
            drones.append(drone)

    return drones