import os
import traceback
from dotenv import load_dotenv
import discord
from discord.ext import commands
from utils.database import init_db
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
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
            print(traceback.format_exc())
    
    bot.remove_command('help')

async def setup_bot():
    try:
        print("Initializing database...")
        init_db()
        print("Database initialized.")
        
        print("Loading extensions...")
        await load_extensions()
        print("Extensions loaded.")
        
        
    except Exception as e:
        print(f"An error occurred during setup: {e}")
        print(traceback.format_exc())

@bot.event
async def setup_hook():
    await setup_bot()

async def main():
    try:
        print("Starting bot...")
        await bot.start(TOKEN)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())