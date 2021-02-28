import asyncio
import discord
from discord import reaction
from discord import message
from discord import user
from discord.ext import commands
import random

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
class tictactoe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tictactoe(self, ctx, p2: discord.Member):
        global count
        global player1
        global player2
        global turn
        global gameOver

        up = '\U00002b06'
        down = '\U00002b07'
        right = '\U000027a1'
        left = '\U00002b05'
        top_left = '\U00002196'
        top_right = '\U00002197'
        down_left = '\U00002199'
        down_right = '\U00002198'
        center = '\U000023fa'

        reactions = [
            top_left,
            up,
            top_right,
            left,
            center,
            right,
            down_left,
            down,
            down_right
        ]

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:","\n",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:","\n",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = ctx.author
            player2 = p2

            # print the board
            em = discord.Embed(title="TicTacToe", description=f"{''.join(board)}")

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                em.set_footer(text=f"It is {player1.display_name}'s turn")
            elif num == 2:
                turn = player2
                em.set_footer(text=f"It is {player2.display_name}'s turn")
            msg = await ctx.send(embed=em)

            if not gameOver:
                mark = ""
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"

                for i in reactions:
                    await msg.add_reaction(i)

                def check(reaction, user):
                    return str(reaction) in [top_left,up,top_right,left,center,right,down_left,down,down_right] and reaction.message == msg and user == turn

                try:
                    print("Trying")
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                except asyncio.TimeoutError:
                    print("No reaction is reacted")
                    await ctx.message.delete()
                    await msg.delete()
                    gameOver = True 
                else:
                    print("A reaction is reacted")
                    if str(reaction.emoji) == top_left:
                        board[0] = mark
                        print(board)
                        count += 1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == up:
                        board[1] = mark
                        print(board)
                        count += 1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == top_right:
                        board[2] = mark
                        print(board)
                        count +=1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == left:
                        board[4] = mark
                        print(board)
                        count +=1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == center:
                        board[5] = mark
                        print(board)
                        count +=1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == right:
                        board[6] = mark
                        print(board)
                        count +=1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == down_left:
                        board[8] = mark
                        print(board)
                        count +=1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == down:
                        board[9] = mark
                        count += 1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
                    elif str(reaction.emoji) == down_right:
                        board[10] = mark
                        count += 1
                        nembed=discord.Embed(title="TicTacToe", description=f"{''.join(board)}", color=0x93e6fb)
                        nembed.set_footer(text=f"It is {turn.display_name}'s turn")
                        await msg.edit(embed=nembed)
                        for condition in winningConditions:
                            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                                gameOver = True
                        print(count)
                        if gameOver == True:
                            await ctx.send(mark + " wins!")
                        elif count >= 9:
                            gameOver = True
                            await ctx.send("It's a tie!")

                        # switch turn
                        if turn == player1:
                            turn = player2
                        elif turn == player2:
                            turn = player1
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    def checkWinner(self, winningConditions, mark):
        global gameOver
        for condition in winningConditions:
            if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
                gameOver = True


def setup(client):
    client.add_cog(tictactoe(client))
