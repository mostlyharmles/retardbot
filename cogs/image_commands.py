import os
import random
import discord
from discord.ext import commands
from PIL import Image
from config import IMAGE_DIR, MOSAIC_DIR, MOSAIC_OUTPUT

class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        await ctx.send("Creating mosaic... Please wait.")
        output_image_path = self.reassemble_image(MOSAIC_DIR, MOSAIC_OUTPUT)
        
        if output_image_path and os.path.exists(output_image_path):
            with open(output_image_path, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
            os.remove(output_image_path)
        else:
            await ctx.send("Failed to create mosaic. Please try again.")

    @commands.command(name='gumby')
    async def random_image(self, ctx):
        images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        if images:
            random_image = random.choice(images)
            image_path = os.path.join(IMAGE_DIR, random_image)
            await ctx.send(file=discord.File(image_path))
        else:
            await ctx.send("No images found in the directory.")

    def reassemble_image(self, grid_dir, output_image_path, grid_size=20):
        sections = [os.path.join(grid_dir, f) for f in os.listdir(grid_dir) if f.endswith('.png')]
        
        if len(sections) != grid_size * grid_size:
            print(f"Expected {grid_size * grid_size} sections, found {len(sections)}")
            return None

        random.shuffle(sections)
        
        first_section = Image.open(sections[0])
        cell_width, cell_height = first_section.size
        
        total_width = cell_width * grid_size
        total_height = cell_height * grid_size
        new_img = Image.new('RGB', (total_width, total_height))
        
        for i in range(grid_size):
            for j in range(grid_size):
                section = Image.open(sections[i * grid_size + j])
                new_img.paste(section, (j * cell_width, i * cell_height))
        
        new_img.save(output_image_path)
        print(f"Reassembled image saved as {output_image_path}")
        return output_image_path