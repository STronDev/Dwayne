import random
import discord
import asyncio
from discord import player
from discord import embeds

from discord.ext import commands

from rps.model import RPS
from rps.parser import RockPaperSiscorParser
from hangman.controller import HangmanGame
from snake.model import game_start

hangman_games = {}

word = "discord"
user_gusses = list()

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='RockPaperScissor', aliases=["rps"], brief="Play a Game of Rock,Paper,Scissor", usage="<rock or paper or scissor>")
    async def rockpaperscissors(self, ctx, choice: RockPaperSiscorParser = RockPaperSiscorParser(RPS.ROCK)):

        rps_m = RPS()
        bot_choice = random.choice(rps_m.get_choice())
        user_choice = choice.choice

        winning_conditions = {
            (RPS.ROCK, RPS.PAPER): False,
            (RPS.ROCK, RPS.SCISSOR): True,
            (RPS.PAPER, RPS.SCISSOR): False,
            (RPS.PAPER, RPS.ROCK): True,
            (RPS.SCISSOR, RPS.ROCK): False,
            (RPS.SCISSOR, RPS.PAPER): True,
        }

        won = None
        if bot_choice == user_choice:
            won = None
        else:
            won = winning_conditions[(user_choice, bot_choice)]

        if won is None:
            if user_choice == RPS.ROCK:
                file = discord.File("assets/Rock-Flip.gif", filename="Rock-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Tied!")
                em.set_image(url="attachment://Rock-Flip.gif")

            elif user_choice == RPS.PAPER:
                file = discord.File("assets/Paper-Flip.gif", filename="Paper-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Tied!")
                em.set_image(url="attachment://Paper-Flip.gif")

            elif user_choice == RPS.SCISSOR:
                file = discord.File("assets/Scissors-Flip.gif", filename="Scissors-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Tied!")
                em.set_image(url="attachment://Scissors-Flip.gif")

        elif won is True:
            if user_choice == RPS.ROCK:
                file = discord.File("assets/Rock-Flip.gif", filename="Rock-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Won!")
                em.set_image(url="attachment://Rock-Flip.gif")

            elif user_choice == RPS.PAPER:
                file = discord.File("assets/Paper-Flip.gif", filename="Paper-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Won!")
                em.set_image(url="attachment://Paper-Flip.gif")

            elif user_choice == RPS.SCISSOR:
                file = discord.File("assets/Scissors-Flip.gif", filename="Scissors-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Won!")
                em.set_image(url="attachment://Scissors-Flip.gif")

        elif won is False:
            if user_choice == RPS.ROCK:
                file = discord.File("assets/Rock-Flip.gif", filename="Rock-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Lost!")
                em.set_image(url="attachment://Rock-Flip.gif")

            elif user_choice == RPS.PAPER:
                file = discord.File("assets/Paper-Flip.gif", filename="Paper-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Lost!")
                em.set_image(url="attachment://Paper-Flip.gif")

            elif user_choice == RPS.SCISSOR:
                file = discord.File("assets/Scissors-Flip.gif", filename="Scissors-Flip.gif")
                em = discord.Embed(title="RockPaperScissor", description="You Lost!")
                em.set_image(url="attachment://Scissors-Flip.gif")


        message = await ctx.send(embed=em, file=file)

        await message.add_reaction("🗑️")

        def check(reaction, user):
            return str(reaction.emoji) == "🗑️" and reaction.message == message and user == ctx.author

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return
        else:
            await message.delete()
            await ctx.message.delete()

    @commands.command()
    async def hm(self, ctx, guess: str):
        player_id = ctx.author.id
        hangman_instance = HangmanGame()
        game_over, won = hangman_instance.run(player_id, guess)

        if game_over:
            game_over_message = "You did not win"
            if won:
                game_over_message = "Congrats you won!!"

            game_over_message = game_over_message + \
                " The word was %s" % hangman_instance.get_secret_word()

            await hangman_instance.reset(player_id)
            await ctx.send(game_over_message)

        else:
            await ctx.send("Progress: %s" % hangman_instance.get_progress_string())
            await ctx.send("Guess so far: %s" % hangman_instance.get_guess_string())

    @commands.command()
    async def snake(self, ctx):
        await ctx.send(game_start())

def setup(client):
    client.add_cog(Games(client))
