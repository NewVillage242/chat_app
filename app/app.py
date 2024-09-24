import time

import redis
from flask import Flask, render_template, request, redirect
from messages.routes import mess_bp
from messages.events import socketio_message_handlers
import os
import time
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.register_blueprint(mess_bp, url_prefix='/messages')
cache = redis.Redis(host='redis', port=6379)
socketio = SocketIO(app)

@app.route('/')
def hello():
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
    count = get_hit_count()
    greeting = 'Hello World, this is the {} times refreshed.'.format(count)
    return render_template('homepage.html', content=greeting) 

socketio_message_handlers(socketio=socketio)

if __name__ == '__main__':
    socketio.run(app)