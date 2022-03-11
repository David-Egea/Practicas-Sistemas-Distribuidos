#!flask/bin/python
from flask import Flask, jsonify, request
import datetime
import json
import psycopg2
from flask_httpauth import HTTPBasicAuth
import sys

app = Flask(__name__)

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# Creates the datbase conection
database = psycopg2.connect("host=casamanzano.duckdns.org port=6000 dbname=postgres user=postgres password=Icai2022")
# Database name
TABLE = "bicimad"

@auth.verify_password
def verify_password(username, password):
    # Gets the password file path
    path = sys.path[0] + "\\users.pass"
    # Reads the users and paswords 
    with open(path, 'r') as file:
            data = file.readlines()
            users = dict([i.split(':') for i in data])
    # Returns whether the user is authorized or not 
    return True if username in users and password==users[username][:-1] else False

@app.route('/api/v1.0/date', methods=['GET'])
def get_date():
    """
    Returns the actual datetime. Usage example:
        *   http://127.0.0.1:6878/api/v1.0/date
    """
    if request.method == 'GET':
        # Returns the actual datetime in RFC 850
        return jsonify({'date': datetime.datetime.now()})
        
@app.route('/api/v1.0/dates', methods=['GET'])
def get_dates():
    """ 
    Returns all dates. Usage example:
        *   http://127.0.0.1:6878/api/v1.0/dates
    """
    # Creates database cursor
    cur = database.cursor()
    # Defines the query 
    query = f"SELECT DISTINCT fecha FROM {TABLE} ORDER BY fecha"
    # Executes the query action
    cur.execute(query)
    # Initializes response list
    response = []
    # For all the rows
    while True:
        # Gets a row from DB
        row = cur.fetchone()
        # If row is None quits
        if row is None:
            break
        # Adds the row to the response
        response.append(row[0])
    # Closes cursor
    cur.close()
    # Returns dates
    return jsonify({'dates': response})
    
@app.route('/api/v1.0/orig_stations', methods=['GET'])
def get_all_base_orig():
    """" 
    Returns all unique origin stations. Usage example:
        * http://127.0.0.1:6878/api/v1.0/orig_stations
    """
    # Creates database cursor
    cur = database.cursor()
    # Defines the query 
    query = f"SELECT DISTINCT idunplug_station FROM {TABLE} ORDER BY idunplug_station"
    # Executes the query action
    cur.execute(query)
    # Initializes response
    response = [] 
    # For all the rows
    while True:
        # Gets a row from DB
        row = cur.fetchone()
        # If row is None quits
        if row is None:
            break
        # Adds the row to the response
        response.append(row[0])
    # Closes cursor
    cur.close()
    # Returns the origin stations
    return jsonify({'origin_stations': response})
    
@app.route('/api/v1.0/dest_stations', methods=['GET'])
def get_all_base_dest():
    """ 
    Returns all unique destination stations. Usage example:
        * http://127.0.0.1:6878/api/v1.0/dest_stations
    """
    # Creates database cursor
    cur = database.cursor()
    # Defines the query 
    query = f"SELECT DISTINCT idplug_station FROM {TABLE} ORDER BY idplug_station"
    # Executes the query action
    cur.execute(query)
    # Initializes response
    response = [] 
    # For all the rows
    while True:
        # Gets a row from DB
        row = cur.fetchone()
        # If row is None quits
        if row is None:
            break
        # Adds the row to the response
        response.append(row[0])
    # Closes cursor
    cur.close()
    # Returns the destination stations
    return jsonify({'destination_stations': response})

@app.route('/api/v1.0/newmove', methods=['POST'])
@auth.login_required
def set_line():
    """ Creates a new move in the Database. Usage example:
            * http://127.0.0.1:6878/api/v1.0/newmove
        And an example of data passed:
         "data": [
            {
                "age_range": 0,
                "date": "28/02/2021",
                "file": 0,
                "id_dest": 160,
                "id_dest_base": 26,
                "id_orig": 163,
                "id_orig_base": 4,
                "travel_time": 543,
                "user_type": 2
            }
    ]
    """
    # Captures the data fields from the post request
    date = request.json.get('date')
    age_range = request.json.get('age_range')
    user_type = request.json.get('user_type')
    id_orig = request.json.get('id_orig')
    id_dest = request.json.get('id_dest')
    id_orig_base = request.json.get('id_orig_base')
    id_dest_base = request.json.get('id_dest_base')
    travel_time = request.json.get('travel_time')
    file = '000000' # File is set to 000000
    # Creates database cursor
    cur = database.cursor()
    # Defines the query 
    query = f"INSERT INTO {TABLE} (fecha,ageRange,user_type,idunplug_station,idplug_station,idunplug_base,idplug_base,travel_time,fichero) \
        VALUES ({date},{age_range},{user_type},{id_orig},{id_dest},{id_orig_base},{id_dest_base},{travel_time},{file})"
    # Executes the query action
    cur.execute(query)
    # Closes cursor
    cur.close()
    # Returns the response
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    
@app.route('/api/v1.0/moves', methods=['GET'])
def get_move_by_day():
    """ Returns all the moves in the given day. Usage examples:
        * http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019
        * http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&orig=146
        * http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&orig=146&dest=162
        * http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&min=300&max=400
        * http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&orig=146&dest=162&min=300
    """
    # Initializes response
    response = []
    # Captures the data fields from the get request
    date = request.args.get('date')
    orig = request.args.get('orig')
    dest = request.args.get('dest')
    min = request.args.get('min')
    max = request.args.get('max')
    # Creates database cursor
    cur = database.cursor()
    if date is not None:
        # Defines the initial query 
        query = f"SELECT * FROM {TABLE} WHERE fecha = '{date}'"
        if orig is not None:
            # /api/v1.0/moves?date=01/06/2019&orig=146
            query = f"{query} AND idunplug_station = {orig}"
        if dest is not None:
            # /api/v1.0/moves?date=01/06/2019&dest=162
            query = f"{query} AND idplug_station = {dest}"
        if min is not None:
            # /api/v1.0/moves?date=01/06/2019&min=400
            query = f"{query} AND travel_time >= {min}"
        if max is not None:
            # /api/v1.0/moves?date=01/06/2019&max=500
            query = f"{query} AND travel_time <= {max}"
        # Orders by date
        query = f"{query} ORDER BY fecha"
        # Executes the query action
        cur.execute(query)
        # For all the rows
        while True:
            # Gets a row from DB
            row = cur.fetchone()
            # If row is None quits
            if row is None:
                break
            # Adds the row to the response
            response.append(dict(zip(["date","age_range","user_type","id_orig","id_dest","id_orig_base","id_dest_base","travel_time","file"],row)))
    # Closes cursor
    cur.close()
    # Returns the response
    return jsonify({'data': response})

@app.route('/api/v1.0/delmove', methods=['DELETE'])
@auth.login_required
def delete_move():
    """
    Deletes the database entries which coincide with the given arguments. 
        *   http://127.0.0.1:6878/api/v1.0/delmove?date=01/06/2019&orig=146&dest=162
    """
    # Captures the data fields from the get request
    date = request.args.get('date')
    orig = request.args.get('orig')
    dest = request.args.get('dest')
    user_type = request.args.get('user_type')
    base_orig = request.args.get('base_orig')
    base_dest = request.args.get('base_dest')
    file = request.args.get('file')
    # Creates database cursor
    cur = database.cursor()
    # Orders by date
    query = f"DELETE from {TABLE} WHERE fecha = '{date}'"
    # Creates database cursor
    cur = database.cursor()
    if date is None:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'} 
    if orig is not None:
        query = f"{query} AND idunplug_station = {orig}"
    if dest is not None:
        query = f"{query}  AND idplug_station = {dest}"
    if base_orig is not None:
        query = f"{query} AND idunplug_base = {base_orig}"
    if base_dest is not None:
        query = f"{query} AND idplug_base = {base_dest}"
    if file is not None:
        query = f"{query} AND fichero = {file}"
    if user_type is not None:
        query = f"{query} AND user_type = {user_type}"
    # Executes the query action
    cur.execute(query)
    # Closes cursor
    cur.close()
    # Returns the response
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    # app.run(debug=True,port=6878)
    app.run(port=6878)