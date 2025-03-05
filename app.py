from flask import Flask, render_template, request, redirect, url_for

# url_for for dynamically changing redirect, also able to sent by arguments

app = Flask(__name__)

# drone reliability
@app.route('/', methods=['GET', 'POST'])
def home():
    topologySelect = None
    dronesCount = None
    dronesTypesCount = None
    droneType1 = None
    typeCount1 = None
    # redundancy = None
    redundantCount = None
    connectionType = None
    cuReliability = None
    if request.method == 'POST':
        topologySelect = request.form.get('topologySelect')
        dronesCount = request.form.get('dronesCount')
        dronesTypesCount = request.form.get('dronesTypesCount')
        droneType1 = request.form.get('droneType1')
        typeCount1 = request.form.get('typeCount1')
        # redundancy = True if request.form.get('redundancy') else False
        redundantCount = request.form.get('redundantCount')
        connectionType = request.form.get('connectionType')
        cuReliability = request.form.get('cuReliability')
        print("HEEREE")
        print(f"""Topology: {topologySelect}, drones: {dronesCount}= {dronesTypesCount}: {droneType1} - {typeCount1}, 
              {redundantCount}, connection {connectionType}: {cuReliability}.""")
    return render_template('home.html', topologySelect=topologySelect, dronesCount=dronesCount, 
                           dronesTypesCount=dronesTypesCount, droneType1=droneType1, typeCount1=typeCount1, 
                           redundantCount=redundantCount, connectionType=connectionType, cuReliability=cuReliability)

if __name__ == '__main__':
    app.run(debug=True)
 