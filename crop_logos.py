#!/usr/bin/env python3
"""
Crop Gemini watermark from logo images
"""
from PIL import Image
import os

def crop_watermark(input_path, output_path, crop_bottom_right=60):
    """
    Crop the bottom-right corner watermark from an image

    Args:
        input_path: Path to the input image
        output_path: Path to save the cropped image
        crop_bottom_right: Number of pixels to crop from bottom and right edges
    """
    # Open the image
    img = Image.open(input_path)
    width, height = img.size

    # Calculate new dimensions (crop bottom-right corner)
    new_width = width - crop_bottom_right
    new_height = height - crop_bottom_right

    # Crop the image
    cropped_img = img.crop((0, 0, new_width, new_height))

    # Save the cropped image
    cropped_img.save(output_path, 'PNG', quality=95)
    print(f"✅ Cropped: {os.path.basename(output_path)}")
    print(f"   Original size: {width}x{height}")
    print(f"   New size: {new_width}x{new_height}")

# Define project paths
projects = {
    'LaiTEX': '/Users/xiaobotu/Documents/ai_agent/LaiTEX/assets',
    'CAiD': '/Users/xiaobotu/Documents/ai_agent/CAiD/assets',
    'PCBai': '/Users/xiaobotu/Documents/ai_agent/PCBai/assets'
}

# Process each logo
for project_name, assets_path in projects.items():
    input_file = os.path.join(assets_path, 'logo_original.png')
    output_file = os.path.join(assets_path, 'logo.png')

    if os.path.exists(input_file):
        print(f"\n🎨 Processing {project_name} logo...")
        crop_watermark(input_file, output_file, crop_bottom_right=60)
    else:
        print(f"❌ Original logo not found for {project_name}")

print("\n✨ All logos processed successfully!")
