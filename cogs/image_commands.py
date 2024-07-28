import os
import random
import discord
from discord.ext import commands
from PIL import Image
from config import IMAGE_DIR


class ImageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gumby")
    async def random_image(self, ctx):
        images = [
            f
            for f in os.listdir(IMAGE_DIR)
            if f.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
        ]
        if images:
            random_image = random.choice(images)
            image_path = os.path.join(IMAGE_DIR, random_image)
            await ctx.send(file=discord.File(image_path))
        else:
            await ctx.send("No images found in the directory.")


async def setup(bot):
    await bot.add_cog(ImageCommands(bot))
