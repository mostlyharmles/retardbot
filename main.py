import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from cogs.image_commands import ImageCommands
from cogs.text_commands import TextCommands
from cogs.message_listener import MessageListener
from cogs.image_processing import ImageProcessing
from cogs.blackjack import Blackjack  # Import the Blackjack cog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def load_extensions():
    await bot.add_cog(ImageCommands(bot))
    await bot.add_cog(TextCommands(bot))
    await bot.add_cog(MessageListener(bot))
    await bot.add_cog(ImageProcessing(bot))
    await bot.add_cog(Blackjack(bot))  # Add the Blackjack cog
    await bot.load_extension('cogs.video_commands')
    await bot.load_extension('cogs.face_detection')
    bot.remove_command('help')  # Remove the default help command

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
