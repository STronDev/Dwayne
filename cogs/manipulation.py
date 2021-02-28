import discord
import datetime
import asyncio
import random
from PIL import Image
from io import BytesIO
from discord.ext import commands
from colorthief import ColorThief
from colormap import rgb2hex


class manipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def wanted(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        wanted = Image.open("assets/wanted.jpg")
        asset = user.avatar_url_as(size = 256)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((246, 246))
        wanted.paste(pfp, (33,147))

        wanted.save("profile.jpg")
        await ctx.send(file = discord.File("profile.jpg"))

    @commands.command()
    async def dominant(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        asset = user.avatar_url_as(size = 256)
        data = BytesIO(await asset.read())
        color_thief = ColorThief(data)
        dc = color_thief.get_color(quality=1)    
        hex = rgb2hex(dc[0], dc[1], dc[2])
        
        await ctx.send(hex)


def setup(client):
    client.add_cog(manipulation(client))