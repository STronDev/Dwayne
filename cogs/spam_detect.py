import asyncio
from typing import Counter
from discord.ext import commands
from asyncio import sleep

class spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        counter = 0
        with open("spam_detect.txt", "r+") as f:
            for lines in f:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            f.writelines(f"{str(message.author.id)}\n")
            if counter > 5:
                await message.guild.ban(message.author, reason = "Spam")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)

def setup(client):
    client.add_cog(spam(client))