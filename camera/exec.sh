#!/bin/bash

green_color='\033[0;32m'
reset_color='\033[0m'

# shellcheck disable=SC2207
ips=($(hostname -I))

ip=${ips[0]}

echo
echo -e "Script executed on IP address: ${green_color}$ip${reset_color}"

(libcamera-vid --nopreview -t 0 --width 1280 --height 720 --codec h264 --framerate 15 --inline --listen -o "tcp://$ip:8888" >/dev/null 2>&1 &)

sleep 1

pid=$(pgrep -f "libcamera-vid --nopreview -t 0 --width 1280 --height 720 --codec h264 --framerate 15 --inline --listen -o tcp://$ip:8888")

echo
echo "Camera PID: $pid"

while true
do
    if ! pgrep -f "libcamera-vid" >/dev/null; then
        echo "Camera process is not running. Restarting..."
        (libcamera-vid --nopreview -t 0 --width 1280 --height 720 --codec h264 --framerate 15 --inline --listen -o "tcp://$ip:8888" >/dev/null 2>&1 &)
        # sleep 3
    fi
    pid=$(pgrep -f "libcamera-vid --nopreview -t 0 --width 1280 --height 720 --codec h264 --framerate 15 --inline --listen -o tcp://$ip:8888")
    echo "Camera PID: $pid"
    sleep 1
done
