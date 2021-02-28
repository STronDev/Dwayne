import discord
import datetime
import pymongo
import os
import io
import csv
import random
import asyncio
import aiohttp
import logging
from bson import ObjectId
from discord.ext import commands
from dns.resolver import query
from settings import MODERATOR
from imgur_downloader import ImgurDownloader
from settings import *

data = {}
data['custom'] = []

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Status of the Server")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    async def status(self, ctx):

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

        no_vc = len(guild.voice_channels)
        no_tc = len(guild.text_channels)
        em = discord.Embed()
        em.set_author(name=self.bot.user.name)
        em.set_thumbnail(url=f"{guild.icon_url}")
        em.add_field(name="Server Name     ", value=guild.name, inline=False)
        em.add_field(name="Text Channels", value=no_tc)
        em.add_field(name="Voice Channels", value=no_vc)
        em.set_image(url=banner)
        em.set_footer(text = datetime.datetime.now())
        await ctx.send(embed=em)

    @commands.command(brief="Updates the banner of the server")
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    async def banner(self, ctx, *, link):
        if ctx.message.guild is None:
            return

        banner = {
            "id": ctx.guild.id,
            "name": f"{ctx.guild.name}",
            "banner": f"{link}",
            "added_by": f"{ctx.author.name}#{ctx.author.discriminator}"
        }

        query = {"id" : ctx.guild.id}
        
        x = server_settings.find_one(query)
        if x is None:
            if not link == "":
                save = server_settings.insert_one(banner)
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.message.guild.edit(banner=data.read())
                        ctx.send("Banner set!")
                await ctx.send("Added Server banner")
            else:
                await ctx.send("Please enter a link of a image")
        elif x is not None:
            replacement_data = {
                "id": ctx.guild.id,
                "banner": f"{link}",
                "name": f"{ctx.guild.name}",
                "added_by": f"{ctx.author.name}#{ctx.author.discriminator}"
            }
            result = server_settings.replace_one(query, replacement_data)
            async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        if resp.status != 200:
                            return await ctx.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.message.guild.edit(banner=data.read())
                        await ctx.send("Banner set!")
            await ctx.send("Updated Server banner")




#                                 ________  ________  ________  ________
#                                |\   ____\|\   __  \|\   ____\|\   ____\
#                                \ \  \___|\ \  \|\  \ \  \___|\ \  \___|_
#                                 \ \  \    \ \  \\\  \ \  \  __\ \_____  \
#                                  \ \  \____\ \  \\\  \ \  \|\  \|____|\  \
#                                   \ \_______\ \_______\ \_______\____\_\  \
#                                    \|_______|\|_______|\|_______|\_________\
#                                                                 \|_________|



    @commands.command(brief="Unloads a Catagory")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    async def unload(self, ctx, cog: str):
        global Cogs_Folder
        cog = cog.lower()

        cot = f"{Cogs_Folder}{cog}"
        try:
            self.bot.unload_extension(cot)
        except Exception as e:
            await ctx.send("Could not Unload Extension")
            return
        await ctx.send("Extension Unloaded Sucessfully")

    @commands.command(brief="Loads a Catagory")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    async def load(self, ctx, cog: str):
        global Cogs_Folder
        cog = cog.lower()

        cot = f"{Cogs_Folder}{cog}"
        try:
            self.bot.load_extension(cot)
        except Exception as e:
            await ctx.send("Could not Load Extension")
            return
        await ctx.send("Extension Loaded Sucessfully")

    @commands.command(brief="Reloads a Catagory")
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    async def reload(self, ctx, cog: str):
        global Cogs_Folder
        cog = cog.lower()
        
        cot = f"{Cogs_Folder}{cog}"
        try:
            self.bot.unload_extension(cot)
            self.bot.load_extension(cot)
        except Exception as e:
            await ctx.send("Could not Reload Extension")
            return
        await ctx.send("Extension Reloaded Sucessfully")

    @status.error
    async def status_handle(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("You dont have required permisions to run this command.")

    @banner.error
    async def status_handle(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("You dont have required permisions to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'link':
                await ctx.send("Please add a Image Link to set as a banner")

    @load.error
    async def status_handle(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("You dont have required permisions to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'cog':
                await ctx.send("Please add a name of a cog to load")
    
    @unload.error
    async def status_handle(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("You dont have required permisions to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'cog':
                await ctx.send("Please add a name of a cog to unload")

    @reload.error
    async def status_handle(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("You dont have required permisions to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'cog':
                await ctx.send("Please add a name of a cog to reload")



#                                     _______   ________   ________
#                                    |\  ___ \ |\   ___  \|\   ___ \
#                                    \ \   __/|\ \  \\ \  \ \  \_|\ \
#                                     \ \  \_|/_\ \  \\ \  \ \  \ \\ \
#                                      \ \  \_|\ \ \  \\ \  \ \  \_\\ \
#                                       \ \_______\ \__\\ \__\ \_______\
#                                        \|_______|\|__| \|__|\|_______|



def setup(client):
    client.add_cog(Admin(client))
