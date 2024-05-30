from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import board
import adafruit_dht
import threading
import subprocess

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

dht_device = adafruit_dht.DHT11(board.D14)

def read_sensor():
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            vcgencmd_output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
            controller_temp = float(vcgencmd_output.split('=')[1].split('\'')[0])

            socketio.emit('sensor_data', {'temp': temperature, 'humidity': humidity, 'controller_temp': controller_temp})
            print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%, Controller temp={2:0.1f}ºC".format(temperature, humidity, controller_temp))
        
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
        except Exception as error:
            dht_device.exit()
            raise error
        
        time.sleep(1.0)

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    threading.Thread(target=read_sensor, daemon=True).start()

    try:
        print("Starting server...")
        socketio.run(app, host='0.0.0.0', port=12344, debug=False, allow_unsafe_werkzeug=True)
    except Exception as e:
        print("An error occurred while starting the server:")
        print(e)
