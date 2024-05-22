#!/bin/bash

green_color='\033[0;32m'
reset_color='\033[0m'
username=""
env_file=".config_env"

if [[ -f "$env_file" ]]; then
    while IFS='=' read -r key value
    do
        # Remove spaces
        key=$(echo $key | xargs)
        value=$(echo $value | xargs)

        if [[ $key == "USERNAME" ]]; then
            echo "Loaded USERNAME: $value"
            username=$value
        fi
    done < "$env_file"
else
    echo "Env file not found."
    exit 1
fi

echo
echo -e "${green_color}This script will scan the local network for active IPs and attempt to SSH into each one.${reset_color}"
echo

# Get local machine IP
primary_ip=$(hostname -I | awk '{print $1}')

# Get network subnet
subnet=$(ip -o -f inet addr show | awk '/scope global/ {print $4}' | grep "$primary_ip")

echo "Scanning the network $subnet..."
found_ips=$(nmap -sn "$subnet" | grep "Nmap scan report for" | awk '{print $NF}' | tr -d '()')
echo

echo -e "${green_color}Found IPs:${reset_color}"
echo "$found_ips"

# Attempt to SSH into each found IP
reachable_ips=()
unreachable_ips=()
for ip in $found_ips; do
    echo
    echo -e "Attempting SSH connection to: ${green_color}$ip${reset_color}"
    # Using SSH with BatchMode to avoid interactive prompts
    output=$(ssh -o BatchMode=yes -o ConnectTimeout=5 "$username@$ip" 2>&1)
    result=$?
    if [[ $result -eq 0 ]]; then
        echo -e "${green_color}Success: Connected to $ip${reset_color}"
        reachable_ips+=("$ip (Successful login)")
    elif [[ $output == *"Permission denied"* ]]; then
        echo -e "${green_color}Reachable but access denied: $ip${reset_color}"
        reachable_ips+=("$ip (Access denied)")
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

    if grep -q "^IP=" "$env_file"; then
        sed -i "s/^IP=.*/IP=$new_ip/" "$env_file"
        echo -e "${green_color}IP updated in $env_file to $new_ip${reset_color}"
    else
        echo "IP=$new_ip" >> "$env_file"
        echo -e "${green_color}IP set in $env_file to $new_ip${reset_color}"
    fi
else
    echo "No reachable IPs were found to save."
fi
