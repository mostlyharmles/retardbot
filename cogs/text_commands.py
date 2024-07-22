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

    @commands.command()
    async def source(self, ctx):
        await ctx.send('https://github.com/mostlyharmles/retardbot')

    @commands.command()
    async def commands(self, ctx):
        await ctx.send('!ascii, !source, !gumby, !glaze, !gifitize, !blackjack(!bj) !whitejack(!wj), !faces, !commands')