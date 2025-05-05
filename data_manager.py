import sqlite3
from data_classes import Type, Drone, DroneInformation

DB_PATH = 'database.db'

# this class get the infromation from the database
class DataManager:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def get_all_information(self):
        self.cursor.execute(
            '''SELECT d.name, d.reliability, d.description, t.type_name, t.description, di.size, di.weight, di.max_speed, max_altitude 
            FROM drones d 
            LEFT JOIN drone_types dt ON d.id = dt.drone_id 
            LEFT JOIN types t ON dt.type_id = t.id
            LEFT JOIN drone_information di ON d.id = di.drone_id'''
        )   

        results = self.cursor.fetchall()

        drones = []
        for row in results:
            name, reliability, description, type_name, type_description, size, weight, max_speed, max_altitude = row
            drone_type = Type(type_name, type_description)
            drone_information = DroneInformation(size, weight, max_speed, max_altitude)
            drone = Drone(name, reliability, drone_type, drone_information, description)
            drones.append(drone)

        return drones
    
    # retrieve all drones
    def get_drones(self):
        self.cursor.execute(
            '''SELECT d.name, d.reliability, d.description
            FROM drones d'''
        )

        results = self.cursor.fetchall()
        return results
    
    # retrieve reliability of drone by given name
    def get_reliability_by_name(self, name):
        self.cursor.execute(
            '''SELECT d.reliability FROM drones d
            WHERE d.name = ?
            ''', (name,)
        )
        reliability = self.cursor.fetchone()
        return reliability[0] if reliability else None
    
    def close_connection(self):
        self.connection.close()