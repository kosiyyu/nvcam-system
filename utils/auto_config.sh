#!/bin/bash

green_color='\033[0;32m'
reset_color='\033[0m'
username=""
config_file="nvcam.conf"

if [[ -f "$config_file" ]]; then
    while IFS='=' read -r key value
    do
        key=$(echo $key | xargs)
        value=$(echo $value | xargs)

        if [[ $key == "USERNAME" ]]; then
            echo "Loaded USERNAME: $value"
            username=$value
        fi
    done < "$config_file"
else
    echo "Config config_file not found."
    exit 1
fi

echo
echo -e "${green_color}This script will scan the local network for active IPs and attempt to SSH into each one.${reset_color}"
echo

primary_ip=$(hostname -I | awk '{print $1}')
subnet=$(ip -o -f inet addr show | awk '/scope global/ {print $4}' | grep "$primary_ip")

echo "Scanning the network $subnet..."
found_ips=$(nmap -sn "$subnet" | grep "Nmap scan report for" | awk '{print $NF}' | tr -d '()')
echo

echo -e "${green_color}Found IPs:${reset_color}"
echo "$found_ips"

reachable_ips=()
unreachable_ips=()

for ip in $found_ips; do
    echo
    echo -e "Attempting SSH connection to: ${green_color}$ip${reset_color}"
    output=$(timeout 10 ssh -o BatchMode=yes -o ConnectTimeout=5 "$username@$ip" 'echo connected && exit' 2>&1)
    result=$?
    if [[ $result -eq 0 ]]; then
        echo -e "Success: Connected and responsive $ip"
        reachable_ips+=("$ip (Successful login)")
    elif [[ $output == *"Permission denied"* || $output == *"Host key verification failed"* ]]; then
        echo -e "${green_color}Reachable but access denied or host key issue: $ip${reset_color}"
        reachable_ips+=("$ip (Access denied/host key issue)")
    else
        echo -e "${reset_color}Failed to connect to $ip - $output${reset_color}"
        unreachable_ips+=("$ip")
    fi
done

echo
echo -e "${green_color}Reachable IPs:${reset_color}"
for entry in "${reachable_ips[@]}"; do
    ip_address=$(echo "$entry" | awk '{print $1}')
    echo "$ip_address"
done

echo
echo -e "${green_color}Unreachable IPs:${reset_color}"
for entry in "${unreachable_ips[@]}"; do
    ip_address=$(echo "$entry" | awk '{print $1}')
    echo "$ip_address"
done

echo
if [[ ${#reachable_ips[@]} -gt 0 ]]; then
    new_ip=$(echo "${reachable_ips[0]}" | awk '{print $1}')

    if grep -q "^IP=" "$config_file"; then
        sed -i "s/^IP=.*/IP=$new_ip/" "$config_file"
        echo -e "${green_color}IP updated in $config_file to $new_ip${reset_color}"
    else
        echo "IP=$new_ip" >> "$config_file"
        echo -e "${green_color}IP set in $config_file to $new  new_ip${reset_color}"
    fi
else
    echo "No reachable IPs were found to save."
fi