import os
import traceback
from dotenv import load_dotenv
import discord
from discord.ext import commands
from utils.database import init_db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def load_extensions():
    extensions = [
        'cogs.image_commands',
        'cogs.text_commands',
        'cogs.message_listener',
        'cogs.image_processing',
        'cogs.blackjack',
        'cogs.video_commands',
        'cogs.face_detection',
        'cogs.token_management'
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}')
            print(traceback.format_exc())  # This will print the full error traceback
    
    bot.remove_command('help')

async def main():
    try:
        print("Initializing database...")
        init_db()
        print("Database initialized.")
        
        print("Loading extensions...")
        await load_extensions()
        print("Extensions loaded.")
        
        print("Starting bot...")
        async with bot:
            await bot.start(TOKEN)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())  # This will print the full error traceback

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())