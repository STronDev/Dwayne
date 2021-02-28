import discord
import random
from discord.ext import commands

board = [
    '⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜',
    '⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜',
    '⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜',
    '⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜',
    '⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜','⬜',
    ]

spox = 0
spoy = 0
game_over = True

def game_start():
    global game_over
    global board
    
    if game_over:
        game_over = False

    brd = board

    bx = ""
    
    for x in range(len(brd)):
        if x == 19 or x == 39 or x == 59 or x == 79 or x == 99 or x == 119 or x == 139 or x == 159 or x == 179:
            bx += "\n".join(brd)
        else:
            bx += "".join(brd)
    
    return bx
