import time

import redis
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# mySQL
import mysql.connector
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'mysql',  # Service name from docker-compose
    'database': 'local',
}
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection
    
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM ttable')  # Replace 'your_table_name' with your actual table name
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    messages = [{"id":row['id'], "author": row['author'], "message":row['message']} for row in rows]
    return messages

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    greeting = 'Hello World, this is the {} times refreshed.'.format(count)
    return render_template('homepage.html', content=greeting) 

@app.route('/messages')
def hello_app():
    
    messages = get_data()
    return render_template('messages.html', messages=messages)
