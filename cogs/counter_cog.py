import discord
from discord.ext import commands, tasks
import os
import json

CHANNEL_ID = 1257770068272484453  # Replace with your specific channel ID
DATA_FILE = 'counter_data.json'

class CounterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.read_data()
        self.count = self.data['count']
        self.high_score = self.data['high_score']
        self.count_save_interval = 25
        self.high_score_save_interval = 10
        self.counter_task.start()

    def cog_unload(self):
        self.counter_task.cancel()

    def read_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {'count': 0, 'high_score': 0}

    def write_data(self, save_count=True, save_high_score=True):
        data = {}
        if save_count:
            data['count'] = self.count
        if save_high_score:
            data['high_score'] = self.high_score
        
        with open(DATA_FILE, 'r+') as f:
            existing_data = json.load(f)
            existing_data.update(data)
            f.seek(0)
            json.dump(existing_data, f)
            f.truncate()

    @tasks.loop(seconds=1)
    async def counter_task(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            self.count += 1
            new_high_score = False
            if self.count > self.high_score:
                self.high_score = self.count
                new_high_score = True
            await channel.send(str(self.count))
            
            save_count = self.count % self.count_save_interval == 0
            save_high_score = new_high_score or self.count % self.high_score_save_interval == 0
            
            if save_count or save_high_score:
                self.write_data(save_count, save_high_score)

    @counter_task.before_loop
    async def before_counter_task(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == CHANNEL_ID and message.author != self.bot.user:
            await message.channel.send("WHAT THE FUCK NOW I HAVE TO START OVER! <:angry_emoji_with_tits:1169797872301117522>")
            self.count = 0
            self.write_data(save_count=True, save_high_score=False)
            self.counter_task.restart()

    @commands.command(name="counths")
    async def show_high_score(self, ctx):
        await ctx.send(f"The current high score is: {self.high_score}")

async def setup(bot):
    await bot.add_cog(CounterCog(bot))