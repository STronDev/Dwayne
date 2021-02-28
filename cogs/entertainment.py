import colormap
import mal
import discord

from discord.ext import commands
from mal import *
from mal import anime
from mal import manga
import requests

from colorthief import ColorThief
from colormap import rgb2hex
from io import BytesIO


class entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["a"], brief="Searches for a Anime")
    async def anime(self, ctx, *, anime):
        search = AnimeSearch(anime)
        search_id = search.results[0].mal_id
        ani = Anime(mal_id=search_id)
        ani_title = ani.title
        ani_image = ani.image_url
        ani_sys = ani.synopsis
        ani_score = ani.score
        ani_url = ani.url
        ani_type = ani.type
        ani_epi = ani.episodes
        ani_status = ani.status
        ani_genres = ani.genres
        rank = ani.rank

        embed = discord.Embed(title=ani_title, url=ani_url, description=ani_sys)
        embed.set_thumbnail(url=ani_image)
        embed.add_field(name=":military_medal: Rank", value=rank, inline=True)
        embed.add_field(name=":trophy: Score", value=ani_score, inline=False)
        embed.add_field(name=":dividers:Type", value=ani_type, inline=True)
        embed.add_field(name=":minidisc: Episodes", value=ani_epi, inline=False)
        embed.add_field(name=":hourglass_flowing_sand: Status", value=ani_status, inline=True)
        genres = ", ".join(ani_genres)
        embed.add_field(name=":arrow_right: Genres", value=ani_genres, inline=False)

    @commands.command(brief="Searches for a Manga")
    async def manga(self, ctx, *, man):
        search = MangaSearch(man)
        search_id = search.results[0].mal_id
        manga = Manga(mal_id=search_id)
        title = manga.title
        image = manga.image_url
        sys = manga.synopsis
        score = manga.score
        url = manga.url
        type = manga.type
        chapters = manga.chapters
        status = manga.status
        genres = manga.genres
        rank = manga.rank

        embed = discord.Embed(title=title, url=url, description=sys)
        embed.set_thumbnail(url=image)
        embed.add_field(name=":military_medal: Rank", value=rank, inline=True)
        embed.add_field(name=":trophy: Score", value=score, inline=True)
        embed.add_field(name=":dividers:Type", value=type, inline=False)
        embed.add_field(name=":minidisc: Chapters", value=chapters, inline=True)
        embed.add_field(name=":hourglass_flowing_sand: Status", value=status, inline=False)
        embed.add_field(name=":arrow_right: Genre", value=genres, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def bored(self, ctx):
        url = "http://www.boredapi.com/api/activity/"
        response = requests.get(url)
        results = response.json()

        em = discord.Embed(title="Are You Bored??")
        em.add_field(name=f"```{results['activity']}```", value='\u200c', inline=False)
        em.set_author(name=ctx.author, url=ctx.author.avatar_url)
        await ctx.send(embed = em)

    @anime.error
    async def anime_handle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'anime':
                await ctx.send("Please mention a Anime")
    
    @manga.error
    async def manga_handle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'manga':
                await ctx.send("Please mention a Manga")


def setup(client):
    client.add_cog(entertainment(client))
