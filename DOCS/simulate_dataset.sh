#!/bin/bash
# ==========================
# SingLoRA Dataset Simulator
# ==========================
# Generates test data for LoRA training on CPU
# Author: snap@spectre
# Date: $(date)

PROJECT_DIR=~/Desktop/z_SingLoRA_Project
DATA_DIR="$PROJECT_DIR/DATA"
OUTPUT_DIR="$PROJECT_DIR/OUTPUT"
DOCS_DIR="$PROJECT_DIR/DOCS"
LOG_FILE="$DOCS_DIR/simulate_log.txt"

echo "[$(date)] Starting dataset simulation..." | tee -a "$LOG_FILE"

# Check directories
for dir in "$DATA_DIR" "$OUTPUT_DIR" "$DOCS_DIR"; do
  if [ ! -d "$dir" ]; then
    echo "Creating missing directory: $dir" | tee -a "$LOG_FILE"
    mkdir -p "$dir"
  fi
done

# Generate dummy text files
for i in {001..005}; do
  echo "Sample caption text for image_$i" > "$DATA_DIR/sample_caption_$i.txt"
done

# Generate placeholder images
for i in {001..005}; do
  convert -size 256x256 xc:gray "$DATA_DIR/sample_image_$i.png"
done

echo "[$(date)] Simulation complete. Files saved to $DATA_DIR" | tee -a "$LOG_FILE"
