import discord
from discord.ext import commands
from settings import *
import requests

from colorthief import ColorThief
from colormap import rgb2hex
from io import BytesIO

bot_channel = 805434733714210846
talk_channel = [
    804650743105323048
]

level = []
levelnum = []

cluster = myclient

leveling = cluster["discord"]["Leveling"]

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channel:
            stats = leveling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {
                        "id": message.author.id,
                        "xp": 100
                    }

                    leveling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    leveling.update_one({
                        "id": message.author.id
                    }, {
                        "$set": {
                            "xp": xp
                        }
                    })

                    lvl = 0
                    while True:
                        if xp < ((50* (lvl**2)) + 50*(lvl - 1)):
                            break
                        lvl += 1
                    
                    xp -= ((50* ((lvl - 1)**2 )) + (50* (lvl - 1)))
                    if xp == 0:
                        await message.channel.send(f"Well done {message.author.mention}! You leveled up to **{lvl}**!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))


                                response = requests.get(message.author.avatar_url)
                                data = BytesIO(response.content)
                                color_thief = ColorThief(data)
                                dc = color_thief.get_color(quality=1)    
                                hex = rgb2hex(dc[0], dc[1], dc[2])

                                color = int(hex(int(hex.replace("#", ""), 16)), 0)

                                em = discord.Embed(description=f"{message.author.mention} you have gotten role **{level[i]}**!!!", Color=color)
                                em.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=em)

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        if user is not None:
            stats = leveling.find_one({
            "id": user.id
            })
            if stats is None:
                response = requests.get(user.avatar_url)
                data = BytesIO(response.content)
                color_thief = ColorThief(data)
                dc = color_thief.get_color(quality=1)    
                code = rgb2hex(dc[0], dc[1], dc[2])

                color = int(hex(int(code.replace("#", ""), 16)), 0)
                em = discord.Embed(description="You Havent send a message yet", color=color)
                await ctx.send(embed=em)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50* (lvl**2)) + 50*(lvl - 1)):
                        break
                    lvl += 1
                
                xp -= ((50* ((lvl - 1)**2 )) + (50* (lvl - 1)))

                boxes = int((xp/(200* ((1/2) * lvl)))* 20)
                rankings = leveling.find().sort("xp", -1)

                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                
                response = requests.get(user.avatar_url)
                data = BytesIO(response.content)
                color_thief = ColorThief(data)
                dc = color_thief.get_color(quality=1)    
                code = rgb2hex(dc[0], dc[1], dc[2])

                color = int(hex(int(code.replace("#", ""), 16)), 0)

                em = discord.Embed(title="{}'s level stats".format(user.name), color=color)
                em.add_field(name="Name", value=user.name, inline=True)
                em.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                em.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                em.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                em.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=em)
        else:
            stats = leveling.find_one({
            "id": ctx.author.id
            })

            if stats is None:
                response = requests.get(ctx.author.avatar_url)
                data = BytesIO(response.content)
                color_thief = ColorThief(data)
                dc = color_thief.get_color(quality=1)    
                code = rgb2hex(dc[0], dc[1], dc[2])

                color = int(hex(int(code.replace("#", ""), 16)), 0)
                em = discord.Embed(description="You Havent send a message yet", color=color)
                await ctx.send(embed=em)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50* (lvl**2)) + 50*(lvl - 1)):
                        break
                    lvl += 1
                
                xp -= ((50* ((lvl - 1)**2 )) + (50* (lvl - 1)))

                boxes = int((xp/(200* ((1/2) * lvl)))* 20)
                rankings = leveling.find().sort("xp", -1)

                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                
                response = requests.get(ctx.author.avatar_url)
                data = BytesIO(response.content)
                color_thief = ColorThief(data)
                dc = color_thief.get_color(quality=1)    
                code = rgb2hex(dc[0], dc[1], dc[2])

                color = int(hex(int(code.replace("#", ""), 16)), 0)

                em = discord.Embed(title="{}'s level stats".format(ctx.author.name), color=color)
                em.add_field(name="Name", value=ctx.author.name, inline=True)
                em.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                em.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                em.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                em.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.send(embed=em)
        

    @commands.command()
    async def leaderboard(self, ctx):
        rankings = leveling.find().sort("xp", -1)
        i = 1
        em = discord.Embed(title="Rankings:")
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                em.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                i += 1
            except:
                pass
            if i == 10:
                break
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(levelsys(client))