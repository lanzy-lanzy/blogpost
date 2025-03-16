from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    # Create a new image with a blue background
    img = Image.new('RGB', (size, size), '#4A90E2')
    draw = ImageDraw.Draw(img)
    
    # Add a simple "B" text
    try:
        # Try to load a system font
        font = ImageFont.truetype("arial.ttf", size=size//2)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the text
    text = "B"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the image
    img.save(output_path)

# Generate both icons
create_icon(192, 'static/icons/icon-192x192.png')
create_icon(512, 'static/icons/icon-512x512.png')