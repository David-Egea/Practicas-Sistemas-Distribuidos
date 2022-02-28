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

# TODO: Cambiar de BBDD sistemasdistribuidos2 -> sistemasdistribuidos2

#Se crea la conexión con la base de datos
database = psycopg2.connect("host=casamanzano.duckdns.org port=6000 dbname=postgres user=postgres password=Icai2022")
app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
    path = sys.path[0] + "\\users.pass"
    with open(path, 'r') as file:
            data = file.readlines()
            users=dict([i.split(':') for i in data])
    if username in users and password==users[username][:-1]: 
        # remove las character \n
        return True
    return False

@app.route('/api/v1.0/delmove', methods=['DELETE'])
@auth.login_required
def delete_move():
    """ Deletes the database entries which coincide with the given arguments. 
        - http://127.0.0.1:6878/api/v1.0/delmove?date=01/06/2019&orig=146&dest=162
    """
    if request.method == 'DELETE':
        date = request.args.get('date')
        orig = request.args.get('orig')
        dest = request.args.get('dest')
        user_type = request.args.get('user_type')
        base_orig = request.args.get('base_orig')
        base_dest = request.args.get('base_dest')
        file = request.args.get('file')

        query = "DELETE from sistemasdistribuidos2 WHERE"
        data = ()
        cur = database.cursor()
        if date is not None:
            query = "DELETE from sistemasdistribuidos2 WHERE fecha = %s"
            data = (date,)
        if orig is not None:
            query = query + " and idunplug_station = %s"
            data = data + (orig,)
        if dest is not None:
            query = query + " and idplug_station = %s"
            data = data + (dest,)
        if base_orig is not None:
            query = query + " and idunplug_base = %s"
            data = data + (base_orig,)
        if base_dest is not None:
            query = query + " and idplug_base = %s"
            data = data + (base_dest,)
        if file is not None:
            query = query + " and fichero = %s"
            data = data + (file,)
        if user_type is not None:
            query = query + " and user_type = %s"
            data = data + (user_type,)
    # Deletes the data
    cur = database.cursor()
    print(query)
    cur.execute(query,data)
  
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/api/v1.0/date', methods=['GET'])
def get_data():
	#http://127.0.0.1:6878/api/v1.0/date
    if request.method == 'GET':
        return jsonify({'date': datetime.datetime.now()})
        
@app.route('/api/v1.0/dates', methods=['GET'])
def get_dates():
    """ Returns all dates."""
    cur = database.cursor()
    cur.execute("SELECT fecha from sistemasdistribuidos2")
    response = []
    while True:
        row = cur.fetchone()
        if row is None:
            break
        elif row[0] not in response:
            response.append(row[0])
    return jsonify({'dates': response})
    
@app.route('/api/v1.0/orig_stations', methods=['GET'])
def get_all_base_orig():
    """ Returns all origin stations. """
    cur = database.cursor()
    cur.execute("SELECT idunplug_station from sistemasdistribuidos2")
    response = []
    row = cur.fetchone()
    while True:
        if row is None:
            break
        elif row[0] not in response:
            response.append(row[0])
        row = cur.fetchone()
    return jsonify({'stations': response})
    
@app.route('/api/v1.0/dest_stations', methods=['GET'])
def get_all_base_dest():
    """ Returns all destination stations. """
    cur = database.cursor()
    cur.execute("SELECT idplug_station from sistemasdistribuidos2")
    response = []
    row = cur.fetchone()
    while True:
        if row is None:
            break
        elif row[0] not in response:
            response.append(row[0])
    return jsonify({'stations': response})
    

@app.route('/api/v1.0/newmove', methods=['POST'])
@auth.login_required
def set_line():
    
    """ Creates a new move in the Database.
        
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
    date = request.json.get('date')
    age_range = request.json.get('age_range')
    user_type = request.json.get('user_type')
    id_orig = request.json.get('id_orig')
    id_dest = request.json.get('id_dest')
    id_orig_base = request.json.get('id_orig_base')
    id_dest_base = request.json.get('id_dest_base')
    travel_time = request.json.get('travel_time')
    file = '000000'

    cur = database.cursor()
    cur.execute("INSERT INTO sistemasdistribuidos2 (fecha, ageRange,user_type, idunplug_station, idplug_station, idunplug_base, idplug_base,travel_time,fichero) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(date,age_range,user_type,id_orig,id_dest,id_orig_base,id_dest_base,travel_time,file,))
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    
@app.route('/api/v1.0/moves', methods=['GET'])
def get_move_by_day():
    """ Returns all the moves in the given day. 
        Usage examples:
        - http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019
        - http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&orig=146
        - http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&orig=146&dest=162
        - http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&min=300&max=400
        - http://127.0.0.1:6878/api/v1.0/moves?date=01/06/2019&orig=146&dest=162&min=300
    """
    if request.method == 'GET':
        response = []
        date = request.args.get('date')
        orig = request.args.get('orig')
        dest = request.args.get('dest')
        min = request.args.get('min')
        max = request.args.get('max')
        cur = database.cursor()
        if date is not None:
            query = "SELECT * from sistemasdistribuidos2 where fecha = %s"
            data = (date,)
            if orig is not None:
                # /api/v1.0/moves?date=01/06/2019&orig=146
                query = query + " and idunplug_station = %s"
                data = data + (orig,)
            if dest is not None:
                # /api/v1.0/moves?date=01/06/2019&dest=162
                query = query + " and idplug_station = %s"
                data = data + (dest,)
            if min is not None:
                # /api/v1.0/moves?date=01/06/2019&min=400
                query = query + " and travel_time >= %s"
                data = data + (min,)
            if max is not None:
                # /api/v1.0/moves?date=01/06/2019&max=500
                query = query + " and travel_time <= %s"
                data = data + (max,)
            # Query execution
            cur.execute(query,data)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                elif row not in response:
                    response.append(dict(zip(["date","age_range","user_type","id_orig","id_dest","id_orig_base","id_dest_base","travel_time","file"],row)))
        # Returns the response
        return jsonify({'data': response})

if __name__ == '__main__':
    app.run(debug=True,port=6878)
    # app.run(port=6878)