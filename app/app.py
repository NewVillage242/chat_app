import time

import redis
from flask import Flask, render_template, request, redirect
import os
import time

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
    cursor = connection.cursor(dictionary=True)
    return connection, cursor

def get_data():
    conn, cursor = get_db_connection()
    cursor.execute('SELECT * FROM ttable')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    messages = [{"id":row['id'], "author": row['author'], "message":row['message']} for row in rows]
    return messages

def insert_data(author, message):
    conn, cursor = get_db_connection()
    cursor.execute(f'INSERT INTO ttable (`author`, `message`) VALUES ("{author}", "{message}")')
    conn.commit()
    conn.close()

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
def show_messages():
    messages = get_data()
    return render_template('messages.html', messages=messages)

@app.route('/messages/<name>')
def chat(name):
    messages = get_data()
    return render_template('send_message.html',author=name, messages=messages) 

@app.route('/send_message')
def send_message():
    author = request.args.get('author')
    message= request.args.get('message')
    insert_data(author, message)
    return redirect(f"/messages/{author}") 