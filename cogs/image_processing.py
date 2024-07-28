import discord
from discord.ext import commands
from utils.image_utils import get_image_url, overlay_image


class ImageProcessing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.overlay_folder = "cum/"  # Update this path

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glaze(self, ctx):
        image_url = await get_image_url(ctx)
        if not image_url:
            await ctx.send("No image found to process.")
            return

        try:
            result_buffer = overlay_image(image_url, self.overlay_folder)
            await ctx.send(
                file=discord.File(result_buffer, filename="overlayed_image.png")
            )
        except Exception as e:
            await ctx.send(f"An error occurred while processing the image: {str(e)}")

    @glaze.error
    async def glaze_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"This command is on cooldown. Please try again in {error.retry_after:.2f} seconds."
            )


async def setup(bot):
    await bot.add_cog(ImageProcessing(bot))
