from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

GPIO.setmode(GPIO.BCM)

motor_pin_1 = 17
motor_pin_2 = 27
ena_pin = 22

GPIO.setup(motor_pin_1, GPIO.OUT)
GPIO.setup(motor_pin_2, GPIO.OUT)
GPIO.setup(ena_pin, GPIO.OUT)

pwm_a = GPIO.PWM(ena_pin, 100)
pwm_a.start(0)

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
        current_position -= 1
    else:
        if current_position >= max_position:
            return
        current_position += 1
    
    GPIO.output(motor_pin_2, GPIO.HIGH if direction == 'left' else GPIO.LOW)
    GPIO.output(motor_pin_1, GPIO.LOW if direction == 'left' else GPIO.HIGH)
    pwm_a.ChangeDutyCycle(force)
    time.sleep(run_time)
    pwm_a.ChangeDutyCycle(0)
    time.sleep(break_time)

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
