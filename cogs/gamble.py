import random

from discord.ext import commands


class gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(breif="Generates a random number between 1 and given number")
    async def roll(self, ctx, lastnum=101):
        n = random.randrange(1, lastnum)
        await ctx.send(f'The number is {n}')

    @commands.command(breif="Rolls a dice")
    async def dice(self, ctx):
        n = random.randrange(1, 7)
        await ctx.send(f'You rolled {n}')

    @commands.command(breif="Tosses a coin")
    async def coin(self, ctx):
        n = random.randint(0, 1)
        await ctx.send('Heads' if n == 1 else 'Tails')

def setup(client):
    client.add_cog(gamble(client))
