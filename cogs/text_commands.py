from discord.ext import commands
from config import GUMBY_ASCII

class TextCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ascii')
    async def gumby(self, ctx):
        await ctx.send(f'```{GUMBY_ASCII}```')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello!')