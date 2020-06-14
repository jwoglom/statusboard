#!/usr/bin/env python3

import os

from flask import Flask, render_template, request, make_response, send_from_directory
from flask_socketio import SocketIO, emit

from users import init_user, user_response, user_set_status, user_checkin, all_statuses
from statuses import get_statuses, get_visible_count, set_custom_statuses, get_unknown_status

# To specify custom configurations, look at config_sample.py
try:
    from config import custom_init_response, custom_statuses
except ImportError:
    print('Failed to load custom config')
    def custom_init_response(message):
        return {}
    
    custom_statuses = None

set_custom_statuses(custom_statuses)

app = Flask(__name__, static_url_path='/static')

if os.getenv('APPLICATION_ROOT'):
    app.config['APPLICATION_ROOT'] = os.getenv('APPLICATION_ROOT')

cors_origins = '*'
if os.getenv('CORS_ALLOWED_ORIGINS'):
    cors_origins = os.getenv('CORS_ALLOWED_ORIGINS').split(',')

# Log messages with Gunicorn
if not app.debug:
    import logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.info('CORS origins: %s', cors_origins)
socketio = SocketIO(app, cors_allowed_origins=cors_origins)

def parse_names(names):
    name_split = names.split('/')
    self_name = name_split[0]
    conn_names = ",".join(filter(None, name_split[1:]))
    return self_name, conn_names

@app.route('/<path:names>')
def index(names):
    self_name, conn_names = parse_names(names)
    return render_template('index.html',
        self_name=self_name,
        conn_names=conn_names,
        path='{}?{}'.format(names, request.query_string.decode()),
        statuses=get_statuses(),
        unknown_status=get_unknown_status(),
        statuses_rows=get_visible_count(),
        statuses_cols=len(conn_names.split(",")) + 1)

@app.route('/manifest.json')
def manifest():
    names = request.query_string.decode()
    self_name, _ = parse_names(names)

    r = make_response(render_template('manifest.json',
        self_title=self_name.title(),
        path=names))

    r.headers.set('Content-Type', 'text/json')
    return r

@app.route('/static/<path:path>')
def static_path(path):
    return send_from_directory('static', path)

@socketio.on('init')
def init_message(message):
    print('init message:', message)

    init_user(message['self_name'], message['conn_names'].split(','))
    emit('init_response', custom_init_response(message))

@socketio.on('update')
def update_message(message):
    print('update message:', message)
    emit('response', user_response(message['self_name']))

@socketio.on('set_status')
def set_status_message(message):
    print('set_status message:', message)
    user_set_status(message['self_name'], message['status'])
    emit('response', all_statuses(), broadcast=True)

@socketio.on('checkin')
def checkin_message(message):
    time_diff = user_checkin(message['self_name'])
    print('checkin message:', message, 'elapsed: %.2f sec' % time_diff)

if __name__ == '__main__':
    socketio.run(app)