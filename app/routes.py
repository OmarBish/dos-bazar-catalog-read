from flask import redirect,request,jsonify
import os
import requests
import sqlite3


# local imports
from app import app

#TODO: redirct all unwanted routes to root dir
# index route, redirect to api dcumentation url
@app.route('/')
def index():
    return redirect('https://bazar2.docs.apiary.io')

@app.route('/master-notification',methods=['POST'])
def massterNotification():
    # variables
    data = request.get_json()
    res = None
    status = None

    # connect to db
    sqlite_query = data['sqlite_query']
    conn = sqlite3.connect('bazar.db')
    cursor = conn.cursor()
    
    # operation
    if sqlite_query.startswith('INSERT') :
        print(sqlite_query)
        cursor.execute(sqlite_query)
        records = cursor.fetchall()
        conn.commit()
        status = 201
    elif sqlite_query.startswith('UPDATE'):
        cursor.execute(sqlite_query)
        conn.commit()
        status = 201
    # close connection and send data
    cursor.close()
    conn.close()
    return jsonify() , status


# index route, redirect to api dcumentation url
@app.route('/query',methods=['POST'])
def query():
    # variables
    data = request.get_json()
    res = None
    status = None

    # connect to db
    sqlite_query = data['sqlite_query']
    conn = sqlite3.connect('bazar.db')
    cursor = conn.cursor()
    
    # operation
    if sqlite_query.startswith('INSERT') :
        master_res = requests.post("https://dos-bazar-catalog-master.herokuapp.com" + "/query" ,json=data)
        res = master_res.json()
        status = master_res.status_code
    elif sqlite_query.startswith('SELECT'):
        cursor.execute(sqlite_query)
        records = cursor.fetchall()
        res = []
        for row in records:
            res.append({'id':row[0],'title':row[1],'amount':row[2]})
        status = 200
    elif sqlite_query.startswith('UPDATE'):
        master_res = requests.post("https://dos-bazar-catalog-master.herokuapp.com" + "/query" ,json=data)
        res = master_res.json()
        status = master_res.status_code
    else:
        res={
            'message':'unsupported operation'
        }
        status = 405
        
    # close connection and send data
    cursor.close()
    conn.close()
    return jsonify(res) , status


    

