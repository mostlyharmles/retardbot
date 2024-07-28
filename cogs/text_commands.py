import discord
from discord.ext import commands
from config import GUMBY_ASCII


class TextCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ascii")
    async def gumby(self, ctx):
        await ctx.send(f"```{GUMBY_ASCII}```")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

    @commands.command()
    async def source(self, ctx):
        await ctx.send("https://github.com/mostlyharmles/retardbot")

    @commands.command()
    async def commands(self, ctx):
        embed = discord.Embed(
            title="RetardBot Commands",
            description="Here are all the available commands:",
            color=discord.Color.purple(),  # You can change this color
        )

        # General Commands
        general_commands = "• !hello\n• !source\n• !gumby\n• !ascii"
        embed.add_field(name="General", value=general_commands, inline=False)

        # Image and Video Commands
        media_commands = "• !glaze\n• !faces\n• !gifitize"
        embed.add_field(name="Image & Video", value=media_commands, inline=False)

        # Game Commands
        game_commands = "• !blackjack (aliases: !bj, !whitejack, !wj)"
        embed.add_field(name="Games", value=game_commands, inline=False)

        # Token Management
        token_commands = "• !check_tokens\n• !next_welfare"
        embed.add_field(name="Token System", value=token_commands, inline=False)

        # Admin Commands
        admin_commands = (
            "• !give_tokens\n• !remove_tokens\n• !give_all_tokens\n• !reset"
        )
        embed.add_field(name="Admin Only", value=admin_commands, inline=False)

        # Set footer
        embed.set_footer(text="im retarded")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TextCommands(bot))
