import time

import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

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
    messages=[
        {'id': 1, 'author': 'twei', 'message': "abc"},
        {'id': 2, 'author': 'anonymous1', 'message': 'hi'},
        {'id': 3, 'author': 'anonymous2', 'message': 'hello, world'},
    ]
    return render_template('messages.html', messages=messages)
