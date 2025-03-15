# This python script will create a tables in database.db file (SQLite3).
# The database will be used to store information about drones and drones types.
# It is executed right at the start of the application.
# Otherwise, you can execute this script in python terminal when there is no database - python create_db.py (consider later pushing database to git)

import sqlite3

DB_PATH = 'database.db'

def create_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    print("Successfully connected!")

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL UNIQUE,
            description TEXT
        )'''
    )

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS drones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            reliability FLOAT NOT NULL,
            description TEXT
        )'''
    )

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS drone_types (
            drone_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            PRIMARY KEY (drone_id, type_id),
            FOREIGN KEY (drone_id) REFERENCES drones(id) ON DELETE CASCADE,
            FOREIGN KEY (type_id) REFERENCES types(id) ON DELETE CASCADE
        )'''
    )

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS drone_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drone_id INTEGER NOT NULL,
            size FLOAT, -- cm
            weight FLOAT, -- kg
            max_speed FLOAT, --m/s
            max_altitude INTEGER, --m
            FOREIGN KEY (drone_id) REFERENCES drones(id) ON DELETE CASCADE
        )'''
    )

    connection.commit()
    print("Successfully created tables!")
    connection.close()

# this data is only for test purposes, it might not contain correct information
# I have to test my app wih some data so this is hardcoded
# In the future it can be fetch from somewhere but now it is not available
def insert_data():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    print("Successfully connected!")

    # data which will be inserted
    types = [
        ("Quadcopter", "Four-rotor drone with good stability"),
        ("Hexacopter", "Six-rotor drone for more power"),
        ("Fixed-Wing", "Airplane-like drone for long-range"),
        ("VTOL", "Hybrid drone with vertical takeoff"),
        ("Racing Drone", "Small and agile drone for speed racing"),
    ]

    drones = [
        ("Phantom 4", 0.95, "Popular consumer drone."),
        ("Mavic Air 2", 0.93, "Compact and powerful drone"),
        ("Inspire 2", 0.98, "Professional drone for filmmakers"),
        ("Parrot Anafi", 0.90, "Lightweight drone"),
        ("Autel EVO II", 0.92, "Drone with long battery life"),
        ("DJI FPV", 0.88, "Fast racing drone"),
        ("Matrice 300 RTK", 0.97, "Drone for inspections"),
        ("Skydio 2", 0.94, "Self-flying drone"),
        ("WingtraOne", 0.96, "Mapping drone"),
        ("eBee X", 0.91, "Surveying drone"),
    ]

    drone_type_mapping = {
        "Phantom 4": "Quadcopter",
        "Mavic Air 2": "Quadcopter",
        "Inspire 2": "Quadcopter",
        "Parrot Anafi": "Quadcopter",
        "Autel EVO II": "Quadcopter",
        "DJI FPV": "Racing Drone",
        "Matrice 300 RTK": "Hexacopter",
        "Skydio 2": "Quadcopter",
        "WingtraOne": "Fixed-Wing",
        "eBee X": "Fixed-Wing",
    }

    drone_information = {
        "Phantom 4": (35.0, 1.38, 20.0, 6000),
        "Mavic Air 2": (18.3, 0.57, 19.0, 5000),
        "Inspire 2": (60.0, 4.25, 26.0, 5000),
        "Parrot Anafi": (24.4, 0.32, 15.0, 4500),
        "Autel EVO II": (40.0, 1.19, 20.0, 5000),
        "DJI FPV": (25.5, 0.79, 39.0, 6000),
        "Matrice 300 RTK": (81.0, 6.3, 23.0, 7000),
        "Skydio 2": (22.9, 0.775, 16.0, 4000),
        "WingtraOne": (125.0, 3.7, 16.0, 5000),
        "eBee X": (116.0, 1.6, 19.0, 4500),
    }

    # inserting data
    for type_name, type_description in types:
        cursor.execute(
            '''INSERT OR IGNORE INTO types (type_name, description) 
            VALUES (?, ?)''', (type_name, type_description)
            )

    for drone_name, drone_reliability, drone_description in drones:
        cursor.execute(
            '''INSERT OR IGNORE INTO drones (name, reliability, description) 
            VALUES (?, ?, ?)''', (drone_name, drone_reliability, drone_description)
            )

    for drone_name, type_name in drone_type_mapping.items():
        cursor.execute(
            '''SELECT id FROM drones 
            WHERE name = ?''', (drone_name,)
            )
        drone_id = cursor.fetchone()

        cursor.execute(
            '''SELECT id FROM types 
            WHERE type_name = ?''', (type_name,)
            )
        type_id = cursor.fetchone()

        if drone_id and type_id:
            cursor.execute(
                '''INSERT OR IGNORE INTO drone_types (drone_id, type_id) 
                VALUES (?, ?)''', (drone_id[0], type_id[0])
                )

    for drone_name, (size, weight, speed, altitude) in drone_information.items():
        cursor.execute(
            '''SELECT id FROM drones 
            WHERE name = ?''', (drone_name,)
            )
        drone_id = cursor.fetchone()

        if drone_id:
            cursor.execute(
                '''INSERT OR IGNORE INTO drone_information (drone_id, size, weight, max_speed, max_altitude) 
                VALUES (?, ?, ?, ?, ?)''', (drone_id[0], size, weight, speed, altitude)
            )

    connection.commit()
    print("Successfully inserted data!")
    connection.close()

# uncomment this only when you know what are you doing
# def delete_data():
#     connection = sqlite3.connect(DB_PATH)
#     cursor = connection.cursor()
#     print("Successfully connected!")

#     db_tables = ["drone_information", "drone_types", "drones", "types"]
    
#     for table in db_tables:
#         cursor.execute(f"DELETE FROM {table};")
#     connection.commit()

#     cursor.execute('VACUUM')
#     connection.commit()

#     print("Successfully cleared database!")

#     connection.close()