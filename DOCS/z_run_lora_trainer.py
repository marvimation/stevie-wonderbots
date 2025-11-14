import os
import time
import json

CONFIG_PATH = "/home/snap/Desktop/z_SingLoRA_Project/DOCS/z_lora_run_config.json"
LOG_PATH = "/home/snap/Desktop/z_SingLoRA_Project/DOCS/train_execute_log.txt"

def log(msg):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_PATH, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(msg)

def main():
    log("=== SingLoRA Trainer Execution Started ===")

    if not os.path.exists(CONFIG_PATH):
        log("[ERROR] Config not found.")
        return

    with open(CONFIG_PATH, "r") as f:
        cfg = json.load(f)

    log(f"Loaded project: {cfg['project_name']}")
    log(f"Using base model: {cfg['base_model']}")
    log(f"Training data: {cfg['train_data_dir']}")
    log(f"Output path: {cfg['output_dir']}")

    data_files = [f for f in os.listdir(cfg["train_data_dir"]) if f.endswith(".png")]
    if not data_files:
        log("[ERROR] No training images found.")
        return
    log(f"Found {len(data_files)} training images.")

    # --- Simulated CPU training loop ---
    for epoch in range(cfg["num_epochs"]):
        log(f"Starting epoch {epoch + 1}/{cfg['num_epochs']}...")
        time.sleep(2)
        log(f"Epoch {epoch + 1}/{cfg['num_epochs']} complete.")

    # --- Create a simulated LoRA output file ---
    output_file = os.path.join(cfg["output_dir"], "trained_model_lora.safetensors")
    with open(output_file, "w") as f:
        f.write("Simulated LoRA weights")
    log(f"LoRA output saved to: {output_file}")

    log("=== Trainer Execution Complete ===")

if __name__ == "__main__":
    main()
