import json, os, time

CONFIG_PATH = "/home/snap/Desktop/z_SingLoRA_Project/DOCS/z_lora_run_config.json"

print(f"[INFO] Loading config from: {CONFIG_PATH}")
with open(CONFIG_PATH, "r") as f:
    cfg = json.load(f)

print("[INFO] Checking data folder...")
if not os.path.exists(cfg["train_data_dir"]):
    print("[ERROR] Missing dataset directory!")
    exit(1)

images = [f for f in os.listdir(cfg["train_data_dir"]) if f.endswith(".png")]
texts = [f for f in os.listdir(cfg["train_data_dir"]) if f.endswith(".txt")]

print(f"[INFO] Found {len(images)} images and {len(texts)} caption files.")

if len(images) == 0 or len(texts) == 0:
    print("[ERROR] Dataset incomplete.")
    exit(1)

print("[INFO] Verifying output folder...")
os.makedirs(cfg["output_dir"], exist_ok=True)

log_path = os.path.join(cfg["log_dir"], "validate_log.txt")
with open(log_path, "a") as log:
    log.write(f"[{time.ctime()}] Validation completed. {len(images)} images, {len(texts)} captions.\n")

print("[SUCCESS] Config and dataset validation complete.")
