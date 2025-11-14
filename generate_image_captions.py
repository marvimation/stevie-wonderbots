import clip
import os
from PIL import Image
import torch

# Initialize the CLIP model
device = "cpu"  # Using CPU instead of CUDA for better compatibility
model, preprocess = clip.load("ViT-B/32", device)

# Set directories for images and captions
image_dir = "IMAGE_FOLDER = '/home/snap/Desktop/z_SingLoRA_Project/SIM_DATA/images'
"
caption_dir = "/home/snap/Desktop/z_SingLoRA_Project/SIM_DATA/captions/"

# Ensure the caption directory exists
os.makedirs(caption_dir, exist_ok=True)

# Function to generate captions for images
def generate_caption(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    
    # Text prompts for captioning
    text = clip.tokenize(["a photo of a person", "a photo of a landscape", "a photo of an animal"]).to(device)
    
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        
    # Find the most similar caption
    similarity = (image_features @ text_features.T).squeeze(0)
    caption = ["a photo of a person", "a photo of a landscape", "a photo of an animal"][similarity.argmax().item()]
    return caption

# Process all images in the SIM_DATA/images folder
for i, filename in enumerate(os.listdir(image_dir)):
    if filename.endswith(".png"):
        image_path = os.path.join(image_dir, filename)
        caption = generate_caption(image_path)
        caption_file = os.path.join(caption_dir, f"sim_caption_{i+1}.txt")
        
        # Save the generated caption to the captions directory
        with open(caption_file, "w") as f:
            f.write(caption)
        print(f"Generated caption for {filename}: {caption}")
