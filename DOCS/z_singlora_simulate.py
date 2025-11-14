#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Paths
DATA_DIR = "/home/snap/Desktop/z_SingLoRA_Project/SIM_DATA"
LOG_FILE = "/home/snap/Desktop/z_SingLoRA_Project/LOGS/simulation_log.txt"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Start log
with open(LOG_FILE, "a") as log:
    log.write(f"[{datetime.now()}] Starting SingLoRA simulation...\n")

# Generate sample images + captions
for i in range(1, 6):
    img_path = os.path.join(DATA_DIR, f"sim_image_{i:03d}.png")
    txt_path = os.path.join(DATA_DIR, f"sim_caption_{i:03d}.txt")
    
    # Create a simple colored image with text
    img = Image.new("RGB", (512, 512), color=(200, 200, 200))  # light gray background
    draw = ImageDraw.Draw(img)
    draw.text((20, 20), f"Sample Image {i}", fill=(0,0,0))
    img.save(img_path)
    
    # Create a simple caption
    with open(txt_path, "w") as f:
        f.write(f"Caption for sample image {i}")
    
    # Log each file
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.now()}] Created {img_path} and {txt_path}\n")

# Final log
with open(LOG_FILE, "a") as log:
    log.write(f"[{datetime.now()}] Simulation complete. Files saved to {DATA_DIR}\n")
