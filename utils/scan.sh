#!/bin/bash

green_color='\033[0;32m'
reset_color='\033[0m'

echo
echo -e "${green_color}This script will scan the local network for active IPs.${reset_color}"
echo

# shellcheck disable=SC2207
ips=($(hostname -I))

ip=${ips[0]}
ip=$(ip addr | grep "$ip" | awk '{print $2}')

result=$(nmap -sn "$ip")

found_ips=$(echo "$result" | grep "Nmap scan report" | awk '{print $NF}' | tr -d '()')

echo "Found IPs:"
echo -e "${green_color}$found_ips${reset_color}"