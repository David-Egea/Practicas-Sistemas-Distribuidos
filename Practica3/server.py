#!flask/bin/python
from flask import Flask, jsonify, request
import datetime
import json
import psycopg2


#Se crea la conexión con la base de datos
database = psycopg2.connect("host=casamanzano.duckdns.org port=6000 dbname=postgres user=postgres password=Icai2022")
app = Flask(__name__)

@app.route('/api/v1.0/date', methods=['GET'])
def get_data():
	#http://127.0.0.1:6878/api/v1.0/date
    if request.method == 'GET':
        return jsonify({'date': datetime.datetime.now()})
        
@app.route('/api/v1.0/dates', methods=['GET'])
def get_dates():
    """ Returns all dates."""
    cur = database.cursor()
    cur.execute("SELECT fecha from sistemasdistribuidos3")
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
    cur.execute("SELECT idunplug_station from sistemasdistribuidos3")
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
    cur.execute("SELECT idplug_station from sistemasdistribuidos3")
    response = []
    row = cur.fetchone()
    while True:
        if row is None:
            break
        elif row[0] not in response:
            response.append(row[0])
    return jsonify({'stations': response})

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
            query = "SELECT * from sistemasdistribuidos3 where fecha = %s"
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