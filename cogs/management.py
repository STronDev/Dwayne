import discord
import json

from discord.ext import commands
from settings import *
from utils import dm

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Kicks a user from Server")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, reason: str = "None"):
        if member is not None:
            message=reason
            await dm(member, message)
            await ctx.guild.kick(member, reason=reason)
        else:
            await ctx.send("Specify a User to kick")

    @commands.command(brief="Bans a user from Server")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, reason: str = "None"):
        if member is not None:
            await dm(member, reason)
            await ctx.guild.ban(member, reason=reason)
        else:
            await ctx.send("Specify a User to kick")

    @commands.command(brief="Unbans a user from Server")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"Unbanned: {user.mention}")

    @commands.command(brief="Viewes Bans of a Server")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):

        guild = ctx.guild
        query = {
            "id" : guild.id,
            "name": f"{guild.name}"
        }

        x = server_settings.find_one(query)
       
        if not x is None:
            id = x["id"]
            name = x["name"]
            banner = x["banner"]
        else:
            banner = ""

        banned_users = await guild.bans()
        em=discord.Embed(title="Banned Users", description="Users that are banned in this server")

        em.set_thumbnail(url=f"{guild.icon_url}")
        for ban_entry in banned_users:
            user = ban_entry.user
            em.add_field(name=user, value="\u200b", inline=False)
        em.set_image(url=banner)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Management(client))
