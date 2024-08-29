from flask import Blueprint
from flask import Flask, render_template, request, redirect

# Prefix /messages
mess_bp = Blueprint('messages', __name__)

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

@mess_bp.route('/')
def show_messages():
    messages = get_data()
    return render_template('messages.html', messages=messages)

@mess_bp.route('/<name>')
def chat(name):
    messages = get_data()
    return render_template('send_message.html',author=name, messages=messages) 

@mess_bp.route('/send_message', methods=['POST'])
def send_message():
    author = request.form['author']
    message= request.form['message']
    insert_data(author, message)
    return redirect(f"/messages/{author}") 