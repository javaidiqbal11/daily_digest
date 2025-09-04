import os
import cv2
import numpy as np
from hashlib import md5

# Input and output directories
input_folder = "Normal"
output_folder = "Normalized"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Set to store hashes of unique images
unique_hashes = set()
count = 0

# >>> You can change this value to control how many images to process
max_images = 50   # e.g., process only first 50 images. Set None for all.

def normalize_image(img, size=(128, 128)):
    """Convert to grayscale, resize, and normalize pixel values."""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # convert to grayscale
    img = cv2.resize(img, size)                   # resize
    img = img.astype("float32") / 255.0           # normalize [0,1]
    return img

def image_to_hash(img):
    """Generate a hash for the image (based on pixel values)."""
    return md5(img.tobytes()).hexdigest()

# Get all files in the folder
all_files = os.listdir(input_folder)

# If max_images is set, restrict the number of files
if max_images is not None:
    all_files = all_files[:max_images]

# Loop through selected images
for filename in all_files:
    filepath = os.path.join(input_folder, filename)

    # Read image
    img = cv2.imread(filepath)
    if img is None:
        continue  # skip unreadable files

    # Normalize
    norm_img = normalize_image(img)

    # Hash
    img_hash = image_to_hash(norm_img)

    # Save only if unique
    if img_hash not in unique_hashes:
        unique_hashes.add(img_hash)
        count += 1
        save_path = os.path.join(output_folder, f"unique_{count}.png")
        cv2.imwrite(save_path, (norm_img * 255).astype("uint8"))

print(f"✅ Normalization done! {count} unique images saved in '{output_folder}'")

