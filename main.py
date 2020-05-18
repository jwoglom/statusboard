#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from users import init_user, user_response, user_set_status, user_checkin, all_statuses

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/<path:names>')
def index(names):
    name_split = names.split('/')
    self_name = name_split[0]
    conn_names = ",".join(filter(None, name_split[1:]))
    return render_template('index.html', self_name=self_name, conn_names=conn_names)


@socketio.on('init')
def init_message(message):
    print('init message:', message)

    init_user(message['self_name'], message['conn_names'].split(','))
    emit('init_response', {})

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
    print('checkin message:', message)
    user_checkin(message['self_name'])

if __name__ == '__main__':
    socketio.run(app)