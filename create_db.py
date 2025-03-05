# This python script will create a tables in database.db file (SQLite3).
# The database will be used to store information about drones and drones types.
# Execute this script in python terminal when there is no database - python create_db.py 

import sqlite3

connection = sqlite3.connect('database.db')
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
# maybe add something to information and also add type information table

print("Successfully created tables!")

connection.close()