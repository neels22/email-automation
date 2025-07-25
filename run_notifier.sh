#!/bin/bash

# Go to the script directory
cd /Users/indraneelsarode/Desktop/email-automation

# Activate virtual environment
source ./myenv/bin/activate

# Run the notifier
./myenv/bin/python slack.py
