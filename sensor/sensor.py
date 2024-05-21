import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT11(board.D14) # pin 6

while True:
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        temperature_f = temperature_c * (9 / 5) + 32
        print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity))
    
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    
    time.sleep(1.0)
