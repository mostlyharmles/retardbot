import discord
from discord.ext import commands
from io import BytesIO


class FaceDetection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faces(self, ctx):
        if not ctx.message.reference:
            await ctx.send("Please reply to a message with an image.")
            return

        referenced_message = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )

        if not referenced_message.attachments:
            await ctx.send("The replied message doesn't contain an image.")
            return

        image_url = referenced_message.attachments[0].url

        # Use the utility function to process the image
        from utils.image_processing import process_image

        img_io = await process_image(image_url)

        await ctx.send(file=discord.File(img_io, "detected_faces.png"))


async def setup(bot):
    await bot.add_cog(FaceDetection(bot))
