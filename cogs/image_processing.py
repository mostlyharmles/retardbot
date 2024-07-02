import discord
from discord.ext import commands
from utils.image_utils import get_image_url, overlay_image

class ImageProcessing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def glaze(self, ctx):
        image_url = await get_image_url(ctx)
        if not image_url:
            await ctx.send("No image found to process.")
            return

        try:
            result_buffer = overlay_image(image_url, "cum.png")
            await ctx.send(file=discord.File(result_buffer, filename="overlayed_image.png"))
        except Exception as e:
            await ctx.send(f"An error occurred while processing the image: {str(e)}")

async def setup(bot):
    await bot.add_cog(ImageProcessing(bot))
