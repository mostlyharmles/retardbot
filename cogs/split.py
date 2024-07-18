from PIL import Image
import os

# Load the image
image_path = "/mnt/data/5.png"
image = Image.open(image_path)

# Get the dimensions of each card (assuming 3x3 grid)
card_width = image.width // 3
card_height = image.height // 3

# Create a directory to save individual cards
output_dir = "/mnt/data/playing_cards"
os.makedirs(output_dir, exist_ok=True)

# Loop to save each card as an individual image
card_count = 1
for row in range(3):
    for col in range(3):
        left = col * card_width
        top = row * card_height
        right = left + card_width
        bottom = top + card_height
        
        card = image.crop((left, top, right, bottom))
        card.save(f"{output_dir}/card_{card_count}.png")
        card_count += 1

output_dir