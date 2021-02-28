import asyncio
from operator import ge
import time
import discord
import random
import datetime
import gtts
import os
import base64
import datetime
from discord.ext import commands, tasks
from googlesearch import search
from utils import text_to_owo, speak
from datetime import datetime
from settings import *
from genderize import Genderize

Text = ""
private_key = ""
mode = ""
Result = ""

choice = ['imposter',
          'mate']


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Converts Text to OWO")
    async def owo(self, ctx, *,statement):
        await ctx.send(text_to_owo(statement))

    @commands.command(brief="Creates a invite for the server")
    @commands.guild_only()
    async def invite(self, ctx):
        link = "https://discord.com/api/oauth2/authorize?client_id=794936106415161376&permissions=301165943&scope=bot"
        await ctx.send(link)

    @commands.command(brief="Kill Some one or Your self")
    async def kill(self, ctx, member: discord.Member = None):
        if member is not None:
            em = discord.Embed(title=f"{ctx.author.name} shot {member.name}")
            em.set_image(url="https://i.gifer.com/Juxv.gif")
            await ctx.send(embed=em)
        else:
            await ctx.send("Mention a user to KILL")

    @commands.command()
    async def imposter(self, ctx, member: discord.Member):
        if member is not None:
            m = random.choice(choice)
            if m == 'imposter':
                await ctx.send(f"{member.mention} is a Imposter")
            elif m == 'mate':
                await ctx.send(f"{member.mention} is a Crewmate")

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.has_role(MODERATOR))
    async def spam(self, ctx, *, word):
        str = '123456789123456789123'

        for i in range(len(str)):
            await ctx.send(word)
        await ctx.send("20")

    @commands.command()
    async def quiz(self, ctx):
        reactions = [
            '\U0001f170',
            '\U0001f171',
            '\U0001f1e8',
            '\U0001f1e9'
        ]
        em = discord.Embed(title="Quiz", description="A) AK-47 \nB) Groza \nC) Bazuka \nD) Aug-A3")
        em.set_thumbnail(url=ctx.author.avatar_url)
        em.set_footer(text=f"Requested by {ctx.author.display_name}")
        msg = await ctx.send(embed=em)

        for i in reactions:
            await msg.add_reaction(i)

        def check(reaction, user):
            return str(reaction) in ['\U0001f170', '\U0001f171', '\U0001f1e8', '\U0001f1e9'] and reaction.message == msg and user == ctx.author

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            if str(reaction.emoji) == "\U0001f170":
                await ctx.send(":laughing:")
            elif str(reaction.emoji) == "\U0001f171":
                await ctx.send(":upside_down:")
            elif str(reaction.emoji) == "\U0001f1e8":
                await ctx.send(":disappointed:")
            elif str(reaction.emoji) == "\U0001f1e9":
                await ctx.send(":cry:")

    @commands.command(aliases=['g', 'google'])
    async def search(self, ctx, *, query):
        em = discord.Embed(title="Goodle Search", color=0x4285F4)
        em.timestamp = datetime.now()
        for i in search(query, num=5, stop=5, pause=2):

            em.add_field(name=i, value="\u200c", inline=False)
        
        await ctx.send(embed=em)

    @commands.command()
    async def gender(self, ctx, *, name: str):
        list = [f"{name}"]
        em = discord.Embed(title="Gender")
        gender = Genderize().get(list)
        result = gender[0]
        em.add_field(name="Name", value=f'{result["name"]}', inline=True)
        em.add_field(name='Gender', value=f'{result["gender"]}', inline=False)
        em.add_field(name='Probability', value=f'{result["probability"]}', inline=True)
        await ctx.send(embed=em)

    @commands.command()
    async def gayrate(self, ctx, member: discord.Member):
        if member is None:
            member = ctx.author

        prcnt = random.randrange(101)
        em = discord.Embed(title = "Gaycheck 831", description = f"{member.display_name}'s is {prcnt}% gay", color = discord.Color.blurple())
        await ctx.send(embed = em)

    @commands.command()
    async def simprate(self, ctx, member: discord.Member):
        if member is None:
            member = ctx.author
            
        prcnt = random.randrange(101)
        em = discord.Embed(title = "Simpcheck 6a5sd", description = f"{member.display_name}'s is {prcnt}% simp", color = discord.Color.purple())
        await ctx.send(embed = em)

    @commands.command()
    async def esplit(self, ctx, email):
        username, domain = email.split("@", 1)
        await ctx.send("Your Username is `{}` and your domain is `{}`".format(username, domain))
        await speak(self, ctx, text=f"{ctx.author.display_name} your Username is {username} and your domain is {domain}")

    @commands.command(usage = "value  key")
    async def encode(self, ctx, message, key):
        enc=[]
        for i in range(len(message)):
            key_c = key[i % len(key)]
            enc.append(chr((ord(message[i]) + ord(key_c)) % 256))
            
        await ctx.send(base64.urlsafe_b64encode("".join(enc).encode()).decode())
    
    @commands.command(usage = "value  key")
    async def decode(self, ctx, message, key):
        dec=[]
        message = base64.urlsafe_b64decode(message).decode()
        for i in range(len(message)):
            key_c = key[i % len(key)]
            dec.append(chr((256 + ord(message[i])- ord(key_c)) % 256))
            
        await ctx.send("".join(dec))

    @commands.command()
    async def alarm(self, ctx, hour: int = 0, min:int = 0, sec:int = 30):
        set_alarm_timer = f"{hour}:{min}:{sec}"
        alarm_loop.start(ctx, set_alarm_timer)
    
    @commands.command()
    async def speak(self, ctx, *, text):
        await speak(self, ctx, text)

        # os.remove("output.mp3")

                                                # Error Handlers

    @spam.error
    async def spam_handler(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("You dont have permisions to run this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'word':
                await ctx.send("Add a word to Spam.")
    
    @imposter.error
    async def imposter_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                await ctx.send("Mention a user to check if they are imposters.")

    @kill.error
    async def kill_handle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                await ctx.send("Mention a user to KILL.")

    @owo.error
    async def owo_handle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'statement':
                await ctx.send("Add a sentence to Convert into OWO")

@tasks.loop()
async def alarm_loop(ctx, set_alarm_timer):
    current_time = datetime.now()
    now = current_time.strftime("%H:%M:%S")
    date = current_time.strftime("%d/%m/%Y")
    if now == set_alarm_timer:
        print("Time to Wake up")
        await ctx.send(f"{ctx.author.mention}Time to Wake up")
#       winsound.PlaySound("sound.wav",winsound.SND_ASYNC


def setup(client):
    client.add_cog(Basic(client))
