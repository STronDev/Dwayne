import random

import aiohttp
from discord.ext import commands
import discord

import praw
from settings_files._global import Redit_ID, Redit_Secret, Redit_Subredits


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        if Redit_ID and Redit_Secret:
            self.reddit = praw.Reddit(client_id=Redit_ID, client_secret=Redit_Secret,
                                      user_agent="Discord Bot:%s:1.0" % Redit_ID)

    @commands.command(brief="Random Reddit meme")
    async def meme(self, ctx):
        async with ctx.channel.typing():
            if not self.reddit:
                await ctx.send("The API is Down")
            else:
                subnum = random.randint(0, 2)
                subreddit = Redit_Subredits[subnum]
                memes = self.reddit.subreddit(subreddit).hot()

                pick = random.randint(1, 10)
                for i in range(0, pick):
                    submit = next(x for x in memes if not x.stickied)

                em = discord.Embed(title=submit.title)
                em.set_image(url=submit.url)
                await ctx.send(embed=em)

    @commands.command(brief="Random picture of a meow")
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow")
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="http://random.cat/")

                    await ctx.send(embed=embed)

    @commands.command(brief="Random picture of a woof")
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof")
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="http://random.dog/")

                    await ctx.send(embed=embed)

    @commands.command(brief="Random picture of a floofy")
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof")
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="https://randomfox.ca/")

                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
