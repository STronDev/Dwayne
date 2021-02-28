import random
import json
import gtts
import discord

from settings import *
from discord.ext import commands


async def speak(self, ctx, text):
    output = gtts.gTTS(text=text, lang="en", slow=False)
    output.save("output.mp3")
    
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio("output.mp3")
    #if not voice_client.is_playing():
    voice_client.play(audio_source, after=None)

# DM

async def dm(member, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)

# OWO

vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']


def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)


def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    return text
