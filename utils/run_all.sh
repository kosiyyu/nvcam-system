#!/bin/bash

nohup python3 ../motor/motor.py > motor.log 2>&1 &

nohup python3 ../sensor/sensor.py > sensor.log 2>&1 &

nohup bash -i ../camera/exec.sh > camera.log 2>&1 &