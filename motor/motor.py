from gpiozero import Motor, PWMOutputDevice
from time import sleep
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

motor = Motor(forward=17, backward=27)
enable_pin = PWMOutputDevice(pin=22, frequency=100)

force = 32
run_time = 0.09
break_time = 0.4

current_position = 0
max_position = 2

def move_motor(direction):
    global current_position
    if direction == 'left':
        if current_position <= -max_position:
            return
        motor.backward()
        current_position -= 1
    else:
        if current_position >= max_position:
            return
        motor.forward()
        current_position += 1

    enable_pin.value = force / 100.0
    sleep(run_time)
    enable_pin.value = 0
    sleep(break_time)

@socketio.on('move')
def handle_move(direction):
    move_motor(direction)
    emit('status', {'message': f'Moved {direction.capitalize()}'})

if __name__ == '__main__':
    try:
        print("Starting server...")
        socketio.run(app, host='0.0.0.0', port=12345)
    except Exception as e:
        print("An error occurred while starting the server:")
        print(e)
