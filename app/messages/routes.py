from flask import Blueprint
from flask import Flask, render_template, request, redirect
import redis
import json

# Prefix /messages
mess_bp = Blueprint('messages', __name__)

#redis
cache = redis.Redis(host='redis', port=6379)

# mySQL
import mysql.connector
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '192.168.0.109',  # Service name from docker-compose
    'port': '3307',
    'database': 'local',
}
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    return connection, cursor

@mess_bp.route('/api')
def get_data():
    if cache.get('chat-key'):
        messages = json.loads(cache.get('chat-key')) 
    else:
        conn, cursor = get_db_connection()
        cursor.execute('SELECT * FROM ttable')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        messages = [{"id":row['id'], "author": row['author'], "message":row['message']} for row in rows]
        cache.set('chat-key', json.dumps(messages))
    return messages

def insert_data(author, message):
    conn, cursor = get_db_connection()
    cursor.execute(f'INSERT INTO ttable (`author`, `message`) VALUES ("{author}", "{message}")')
    # update data inside redis
    if cache.get('chat-key'):
        dics = json.loads(cache.get('chat-key'))
        dics.append({'id': 100, 'author': author, 'message':message})
        cache.set('chat-key', json.dumps(dics))
    conn.commit()
    conn.close()

@mess_bp.route('/')
def show_messages():
    messages = get_data()
    return render_template('messages.html', messages=messages)

@mess_bp.route('/<name>')
def chat(name):
    messages = get_data()
    return render_template('chat_room.html',author=name, messages=messages) 

@mess_bp.route('/send_message', methods=['POST'])
def send_message():
    author = request.form['author']
    message= request.form['message']
    insert_data(author, message)
    return redirect(f"/messages/{author}") 