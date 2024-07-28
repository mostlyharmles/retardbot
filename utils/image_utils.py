import discord
from PIL import Image
import requests
import io
import random
import math
import os


async def get_image_url(ctx):
    if ctx.message.reference:
        referenced_message = await ctx.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            return referenced_message.attachments[0].url
    else:
        async for message in ctx.channel.history(limit=100):
            if message.attachments:
                return message.attachments[0].url
    return None


def get_random_overlay(overlay_folder):
    overlay_files = [
        f
        for f in os.listdir(overlay_folder)
        if f.endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]
    if not overlay_files:
        raise ValueError(f"No image files found in {overlay_folder}")
    return os.path.join(overlay_folder, random.choice(overlay_files))


def overlay_image(image_url, overlay_folder, min_size_ratio=0.2):
    # Download the original image
    response = requests.get(image_url)
    original_image = Image.open(io.BytesIO(response.content)).convert("RGBA")

    # Get a random overlay image
    overlay_path = get_random_overlay(overlay_folder)
    overlay_image = Image.open(overlay_path).convert("RGBA")

    # Get dimensions
    bg_width, bg_height = original_image.size
    overlay_width, overlay_height = overlay_image.size

    # Calculate minimum size based on background image
    min_width = int(bg_width * min_size_ratio)
    min_height = int(bg_height * min_size_ratio)

    # Calculate scale to achieve minimum size
    width_scale = min_width / overlay_width
    height_scale = min_height / overlay_height
    min_scale = max(width_scale, height_scale)

    # Random scaling (min_scale to 50% of background size)
    max_scale = min(0.5, bg_width / overlay_width, bg_height / overlay_height)
    scale = random.uniform(min_scale, max_scale)

    new_width = int(overlay_width * scale)
    new_height = int(overlay_height * scale)

    overlay_image = overlay_image.resize((new_width, new_height), Image.LANCZOS)

    # Random rotation
    rotation = random.randint(0, 360)
    overlay_image = overlay_image.rotate(rotation, expand=True)

    # Random position
    max_x = bg_width - new_width
    max_y = bg_height - new_height
    random_x = random.randint(0, max(0, max_x))
    random_y = random.randint(0, max(0, max_y))

    # Create a new transparent image for rotated overlay
    rotated_overlay = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
    rotated_overlay.paste(overlay_image, (random_x, random_y), overlay_image)

    # Combine the original image with the overlay
    combined_image = Image.alpha_composite(original_image, rotated_overlay)

    # Save the resulting image to a buffer
    buffer = io.BytesIO()
    combined_image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


async def save_attachment(attachment):
    file_path = attachment.filename
    await attachment.save(file_path)
    return file_path


async def cleanup_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
