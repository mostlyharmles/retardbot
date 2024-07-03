import discord
from PIL import Image
import requests
import io
import os

async def get_image_url(ctx):
    if ctx.message.reference:
        referenced_message = await ctx.fetch_message(ctx.message.reference.message_id)
        if referenced_message.attachments:
            return referenced_message.attachments[0].url
    else:
        async for message in ctx.channel.history(limit=50):
            if message.attachments:
                return message.attachments[0].url
    return None

def overlay_image(image_url, overlay_path):
    # Download the original image
    response = requests.get(image_url)
    original_image = Image.open(io.BytesIO(response.content)).convert("RGBA")

    # Load the transparent GIF overlay
    overlay_image = Image.open(overlay_path).convert("RGBA")

    # Resize overlay if necessary
    overlay_image = overlay_image.resize(original_image.size, Image.LANCZOS)

    # Combine the original image with the overlay
    combined_image = Image.alpha_composite(original_image, overlay_image)

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