#!/bin/bash

# Read the nvcam.conf file
USERNAME=$(grep 'USERNAME' nvcam.conf | cut -d '=' -f2)
IP=$(grep 'IP' nvcam.conf | cut -d '=' -f2)

ssh $USERNAME@$IP '/home/kosiyyu/nvcam-system/utils/run_all.sh'