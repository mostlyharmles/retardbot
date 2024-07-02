import random
from discord.ext import commands
from config import KEYWORDS, SPECIFIC_KEYWORD_RESPONSES

class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        msg_content = message.content.lower()
        
        if any(keyword in msg_content for keyword in KEYWORDS):
            random_number = random.randint(0, 100)
            await message.channel.send(f'You are {random_number}% Retarded!')

        for keyword, response in SPECIFIC_KEYWORD_RESPONSES.items():
            if keyword in msg_content:
                if callable(response):
                    response = response()
                await message.channel.send(response)
                break
