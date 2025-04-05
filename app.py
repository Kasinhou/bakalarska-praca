from flask import Flask, jsonify, render_template, request
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
# drones = data_manager.get_all_information()
drones_types = data_manager.get_drones()

data_manager.close_connection()

# drone reliability
@app.route('/', methods=['GET', 'POST'])
def home():
    swarmInfo = {}
    
    if request.method == 'POST':
        swarmInfo['structure'] = request.form.get('topologySelect')
        swarmInfo['dronesCount'] = request.form.get('dronesCount')
        swarmInfo['typesCount'] = request.form.get('dronesTypesCount')
        swarmInfo['connection'] = request.form.get('connectionType')
        swarmInfo['cuReliability'] = request.form.get('cuReliability')

        swarmInfo['typesInfo'] = []
        for i in range(1, int(swarmInfo['typesCount']) + 1):
            droneType = request.form.get(f'droneType{i}')
            typeCount = request.form.get(f'typeCount{i}')
            redundantCount = request.form.get(f'redundantCount{i}')

            swarmInfo['typesInfo'].append({ 'droneType': droneType, 'typeCount': typeCount, 'redundantCount': redundantCount })


        calculation = Calculation(swarmInfo)

        # collect errors from the server side
        errors = calculation.validate_data()
        if errors:
            print(errors)
            return jsonify({"success": False, "errors": errors}), 400
        calculation.calculate()
    return render_template('home.html')

@app.route('/api/drones')
def get_drones():
    drone_options = [{"name": drone[0], "reliability": drone[1], "description": drone[2]} for drone in drones_types]
    return json.dumps(drone_options)

if __name__ == '__main__':
    app.run(debug=True)
 