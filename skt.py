from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('index.html', **values)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data': {'per1': 20, 'per2': 40, 'case': 1}})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')