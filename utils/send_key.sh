#!/bin/bash

config_file="nvcam.conf"
key_path="$HOME/.ssh/nvcam"
key_comment="nvcam"

if [[ ! -f "$config_file" ]]; then
    echo "Configuration file not found."
    exit 1
fi

source "$config_file"

if [[ ! -f "$key_path" ]]; then
    echo "Generating SSH key..."
    ssh-keygen -t rsa -b 2048 -C "$key_comment" -f "$key_path" -N ""
else
    echo "Key already exists. Skipping generation..."
fi

echo "Copying SSH public key to $IP..."
ssh-copy-id -i "${key_path}.pub" "$USERNAME@$IP"
