from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial
import time

app = Flask(__name__)
socketio = SocketIO(app)

try:
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=3)  # change ACM number as found from ls /dev/tty/ACM*
except:
    ser = serial.Serial("/dev/ttyACM1", 9600, timeout=3)  # change ACM number as found from ls /dev/tty/ACM*

ser.baudrate = 9600

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data': {'per1': 20, 'per2': 40, 'case': 3}})


@socketio.on('get new value')
def get_new_value(msg):
    time.sleep(1)
    data = ser.readline()
    data2 = data.decode("UTF-8")
    position_case = data2.find('bat')

    cases = data2[position_case + 5:position_case + 6]
    position_Ah1 = data2.find('Ah1')
    position_Ah2 = data2.find('Ah2')
    if position_Ah1 < 0:
        Ah1 = 0.0
        Ah2 = 0.0
    else:
        Ah1 = float(data2[position_Ah1 + 5:position_Ah1 + 11])
        Ah2 = float(data2[position_Ah2 + 5:position_Ah2 + 11])
    emit('after connect', {'data': {'per1': 20, 'per2': 40, 'case': 3}}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
