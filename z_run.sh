#!/bin/bash
cd /home/snap/Desktop/z_turtle_ai
nohup python3 z_turtle_ai.py > /dev/null 2>&1 &
echo "z_turtle_ai STARTED (PID: $!)"
