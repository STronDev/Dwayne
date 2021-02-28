import random
import asyncio
import discord
from discord.ext import commands


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def calc(self, ctx, num1: int, num2: int):
        # TODO: Make this look better

        reaction = [
                    '\U0001f1e6',
                    '\U0001f1f8',
                    '\U0001f1f2',
                    '\U0001f1e9'
        ]

        embed=discord.Embed(title="Calculator", description="Chose one of the following Operations \n \n1)Addition (+) \n2)Subbraction (-)\n3)Multiplication (x)\n4)Division (/)", color=0x93e6fb)
        embed.set_footer(text=f"React with the emoji you want as Operator")
        message = await ctx.send(embed=embed)
        for i in reaction:
            await message.add_reaction(i)

        def check(reaction, user):
            return str(reaction) in ['\U0001f1e6', '\U0001f1f8', '\U0001f1f2', '\U0001f1e9'] and reaction.message == message and user == ctx.author

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.message.delete()
            await message.delete()
        else:

            nembed=discord.Embed(title="Calculator", color=0x93e6fb)
            nembed.set_footer(text=f"Use `.help` for more commands")

            if str(reaction.emoji) == '\U0001f1e6':
                value = num1 + num2
                await message.clear_reactions()
                nembed.add_field(name="Additon Value", value=value, inline=False)
                await message.edit(embed=nembed)
            elif str(reaction.emoji) == '\U0001f1f8':
                value = num1 - num2
                await message.clear_reactions()
                nembed.add_field(name="Subraction Value", value=value, inline=False)
                await message.edit(embed=nembed)
            elif str(reaction.emoji) == '\U0001f1f2':
                value = num1 * num2
                await message.clear_reactions()
                nembed.add_field(name="Multiplication Value", value=value, inline=False)
                await message.edit(embed=nembed)
            elif str(reaction.emoji) == '\U0001f1e9':
                value = num1/num2
                await message.clear_reactions()
                nembed.add_field(name="Division Value", value=value, inline=False)
                await message.edit(embed=nembed)

    @calc.error
    async def calc_handle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'num1':
                await ctx.send("Please mention 2 numbers for calculation")
            elif error.param.name == 'num2':
                await ctx.send("Please mention 2nd number for calculation")
            


def setup(client):
    client.add_cog(Calculator(client))
