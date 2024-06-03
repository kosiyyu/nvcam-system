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

force = 50
step_duration = 0.09  
idle_time = 0.1

current_step = 0
max_steps = 20

def move_motor(steps, direction):
    global current_step
    if direction == 'left':
        target_step = max(current_step - steps, -max_steps)
    else:
        target_step = min(current_step + steps, max_steps)

    while (direction == 'left' and current_step > target_step) or (direction == 'right' and current_step < target_step):
        if direction == 'left':
            motor.backward()
            current_step -= 1
        else:
            motor.forward()
            current_step += 1

        enable_pin.value = force / 100.0
        sleep(step_duration)
        enable_pin.value = 0
        sleep(idle_time)
        # print(steps, current_step)

@socketio.on('move')
def handle_move(direction):
    steps = 1  # default number of steps

    move_motor(steps, direction)
    emit('status', {'message': f'Moved {direction.capitalize()} {steps} steps'})

if __name__ == '__main__':
    try:
        print("Starting server...")
        socketio.run(app, host='0.0.0.0', port=12345, allow_unsafe_werkzeug=True)
    except Exception as e:
        print("An error occurred while starting the server:")
        print(e)
