import discord
from discord.ext import commands, tasks
import os

CHANNEL_ID = 1257770068272484453  # Replace with your specific channel ID
COUNTER_FILE = 'counter.txt'

class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = self.read_counter()
        self.counter_task.start()

    def cog_unload(self):
        self.counter_task.cancel()

    def read_counter(self):
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, 'r') as f:
                return int(f.read().strip())
        return 0

    def write_counter(self):
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(self.count))

    @tasks.loop(seconds=1)
    async def counter_task(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            self.count += 1
            await channel.send(str(self.count))
            self.write_counter()

    @counter_task.before_loop
    async def before_counter_task(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == CHANNEL_ID and message.author != self.bot.user:
            await message.channel.send("WHAT THE FUCKING FUCK NOW I HAVE TO START OVER :angry_emoji_with_tits:")
            self.count = 0
            self.write_counter()
            self.counter_task.restart()

async def setup(bot):
    await bot.add_cog(CounterCog(bot))