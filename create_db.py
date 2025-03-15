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