#!/bin/bash

source .config_env

SSH_KEY_PATH="$HOME/.ssh/nvcam"

# Check if the SSH key exists
if [[ ! -f "$SSH_KEY_PATH" ]]; then
    echo "Error: SSH key not found at $SSH_KEY_PATH"
    exit 1
fi

echo "Connecting to $IP as $USERNAME..."
ssh -i "$SSH_KEY_PATH" "$USERNAME@$IP"
