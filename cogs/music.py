import discord
import youtube_dl
import random
import asyncio
from discord.ext import commands
from discord.voice_client import VoiceClient
from random import choice


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

queue = []

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='This command makes the bot join the voice channel')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return
        
        else:
            channel = ctx.message.author.voice.channel

        await channel.connect()

    @commands.command(name='queue', help='This command adds a song to the queue')
    async def queue_(self, ctx, url):
        global queue

        queue.append(url)
        player = await YTDLSource.from_url(str(url))
        await ctx.send(f'`{player.title}` added to queue!')

    @commands.command(name='remove', help='This command removes an item from the list')
    async def remove(self, ctx, number):
        global queue

        try:
            del(queue[int(number)])
            await ctx.send(f'Your queue is now `{queue}!`')
        
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range**')
            
    @commands.command(name='play', help='This command plays songs')
    async def play(self, ctx):
        global queue

        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0])
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))
        del(queue[0])

        while True:
            if not voice_channel.is_playing():
                player = await YTDLSource.from_url(queue[0])
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send('**Now playing:** {}'.format(player.title))
                del(queue[0])
            else:
                return

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.pause()

    @commands.command(name='resume', help='This command resumes the song!')
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.resume()

    @commands.command(name='view', help='This command shows the queue')
    async def view(self, ctx):
        await ctx.send(f'Your queue is now `{queue}!`')

    @commands.command(name='leave', help='This command stops makes the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @commands.command(name='stop', help='This command stops the song!')
    async def stop(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.stop()

def setup(client):
    client.add_cog(music(client))    