# cogs/token_management.py
import discord
from discord.ext import commands
from utils.database import get_user_tokens, set_user_tokens

class TokenManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='give_tokens')
    @commands.has_permissions(administrator=True)
    async def give_tokens(self, ctx, member: discord.Member, amount: int):
        current_tokens = get_user_tokens(member.id)
        new_tokens = current_tokens + amount
        set_user_tokens(member.id, new_tokens)
        await ctx.send(f"Given {amount} tokens to {member.mention}. They now have {new_tokens} tokens.")

    @commands.command(name='remove_tokens')
    @commands.has_permissions(administrator=True)
    async def remove_tokens(self, ctx, member: discord.Member, amount: int):
        current_tokens = get_user_tokens(member.id)
        new_tokens = max(0, current_tokens - amount)
        set_user_tokens(member.id, new_tokens)
        await ctx.send(f"Removed {amount} tokens from {member.mention}. They now have {new_tokens} tokens.")

    @commands.command(name='check_tokens')
    async def check_tokens(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        tokens = get_user_tokens(member.id)
        await ctx.send(f"{member.mention} has {tokens} tokens.")

    @commands.command(name='give_all_tokens')
    @commands.has_permissions(administrator=True)
    async def give_all_tokens(self, ctx, amount: int):
        for member in ctx.guild.members:
            if not member.bot:
                current_tokens = get_user_tokens(member.id)
                new_tokens = current_tokens + amount
                set_user_tokens(member.id, new_tokens)
        await ctx.send(f"Given {amount} tokens to all members in the server.")

async def setup(bot):
    await bot.add_cog(TokenManagement(bot))