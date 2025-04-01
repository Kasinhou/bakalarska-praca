from flask import Flask, render_template, request, redirect, url_for
from db_operations import DatabaseOperation
from data_manager import DataManager
from reliability import Calculation
import json

# url_for for dynamically changing redirect, also able to sent by arguments

app = Flask(__name__)

# uncomment when you want to create database and insert test data 
# (especially if this is your first time running this project)
# otherwise leave it commented
# db_operations = DatabaseOperation()
# db_operations.create_database()
# db_operations.insert_data()
# db_operations.close_connection()

data_manager = DataManager()
drones = data_manager.get_all_information()
drones_types = data_manager.get_drones()

data_manager.close_connection()

# drone reliability
@app.route('/', methods=['GET', 'POST'])
def home():
    structureSelected = None
    dronesCount = None
    dronesTypesCount = None
    redundantCount = None
    connectionType = None
    cuReliability = None
    if request.method == 'POST':
        structureSelected = request.form.get('topologySelect')
        dronesCount = request.form.get('dronesCount')
        dronesTypesCount = request.form.get('dronesTypesCount')
        redundantCount = request.form.get('redundantCount')
        connectionType = request.form.get('connectionType')
        cuReliability = request.form.get('cuReliability')
        # print(f"""Topology: {structureSelected}, drones: {dronesCount}= {dronesTypesCount}, 
        #       {redundantCount}, connection {connectionType}: {cuReliability}.""")
        calculation = Calculation(structureSelected, dronesCount, dronesTypesCount, connectionType, redundantCount, cuReliability)
    return render_template('home.html')

@app.route('/api/drones')
def get_drones():
    drone_options = [{"name": drone[0], "reliability": drone[1], "description": drone[2]} for drone in drones_types]
    return json.dumps(drone_options)

if __name__ == '__main__':
    app.run(debug=True)
 