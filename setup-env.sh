#!/bin/bash
# Bash script to create .env file from template
# Run this script: ./setup-env.sh

if [ -f ".env" ]; then
    echo ".env file already exists. Skipping creation."
    echo "If you want to recreate it, delete .env first and run this script again."
else
    if [ -f "env.template" ]; then
        cp env.template .env
        echo ".env file created successfully from env.template!"
        echo "You can now edit .env to customize your configuration."
    else
        echo "Error: env.template file not found!"
        exit 1
    fi
fi

