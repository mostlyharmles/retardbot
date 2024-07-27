# cogs/token_management.py
import discord
from discord.ext import commands
from utils.database import get_user_tokens, set_user_tokens
from datetime import datetime, timedelta
import asyncio

class TokenManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poor_role_id = None  # Set this to your "poor" role ID
        self.bot.loop.create_task(self.schedule_daily_tokens())

    @commands.Cog.listener()
    async def on_ready(self):
        # Set the poor_role_id here. Replace YOUR_POOR_ROLE_ID with the actual role ID.
        self.poor_role_id = 1266812216729014494

    async def update_poor_role(self, guild, member, is_poor):
        if self.poor_role_id is None:
            return

        poor_role = guild.get_role(self.poor_role_id)
        if poor_role is None:
            return

        if is_poor and poor_role not in member.roles:
            await member.add_roles(poor_role)
        elif not is_poor and poor_role in member.roles:
            await member.remove_roles(poor_role)

    async def schedule_daily_tokens(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
            wait_seconds = (midnight - now).total_seconds()
            await asyncio.sleep(wait_seconds)
            await self.give_daily_tokens()

    @commands.command(name='give_tokens')
    @commands.has_permissions(administrator=True)
    async def give_tokens(self, ctx, member: discord.Member, amount: int):
        current_tokens = get_user_tokens(member.id)
        new_tokens = current_tokens + amount
        is_poor = set_user_tokens(member.id, new_tokens)
        await self.update_poor_role(ctx.guild, member, is_poor)
        await ctx.send(f"Given {amount} tokens to {member.mention}. They now have {new_tokens} tokens.")

    @commands.command(name='remove_tokens')
    @commands.has_permissions(administrator=True)
    async def remove_tokens(self, ctx, member: discord.Member, amount: int):
        current_tokens = get_user_tokens(member.id)
        new_tokens = max(0, current_tokens - amount)
        is_poor = set_user_tokens(member.id, new_tokens)
        await self.update_poor_role(ctx.guild, member, is_poor)
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
        try:
            affected_users = 0
            poor_role = ctx.guild.get_role(self.poor_role_id)

            for member in ctx.guild.members:
                if not member.bot:
                    current_tokens = get_user_tokens(member.id)
                    new_tokens = current_tokens + amount
                    set_user_tokens(member.id, new_tokens)
                    affected_users += 1

                    if poor_role and poor_role in member.roles:
                        try:
                            await member.remove_roles(poor_role)
                        except discord.Forbidden:
                            pass  # Skip members we can't modify roles for

            await ctx.send(f"Given {amount} tokens to all users and removed the poor role. {affected_users} users affected.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='reset')
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx):
        try:
            from utils.database import reset_all_user_tokens
            count = reset_all_user_tokens()
            
            poor_role = ctx.guild.get_role(self.poor_role_id)
            if poor_role:
                for member in ctx.guild.members:
                    if not member.bot and poor_role not in member.roles:
                        try:
                            await member.add_roles(poor_role)
                        except discord.Forbidden:
                            pass  # Skip members we can't assign roles to
            
            await ctx.send(f"All users Gumby tokens have been reset to 0 and assigned the poor role. {count} users affected.")
        except Exception as e:
            await ctx.send(f"An error occurred while resetting tokens: {str(e)}")

    async def give_daily_tokens(self, amount: int = 100):
        try:
            affected_users = 0
            for guild in self.bot.guilds:
                for member in guild.members:
                    if not member.bot:
                        current_tokens = get_user_tokens(member.id)
                        new_tokens = current_tokens + amount
                        set_user_tokens(member.id, new_tokens)
                        affected_users += 1

                        if self.poor_role_id:
                            poor_role = guild.get_role(self.poor_role_id)
                            if poor_role and poor_role in member.roles:
                                try:
                                    await member.remove_roles(poor_role)
                                except discord.Forbidden:
                                    pass  # Skip members we can't modify roles for

            print(f"Given {amount} welfare gumby tokens to all users. {affected_users} users affected.")
        except Exception as e:
            print(f"An error occurred while giving daily tokens: {str(e)}")

    @commands.command(name='next_welfare')
    async def next_welfare(self, ctx):
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0,) + timedelta(days=1)
        time_left = midnight - now
        await ctx.send(f"Next welfare delivery in: {time_left}")

async def setup(bot):
    await bot.add_cog(TokenManagement(bot))