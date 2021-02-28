import discord
import json
import asyncio
import random
import os
from discord import widget
from discord import user
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

os.chdir("D:\Coding\Mander")

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        a = await open_account(ctx.author)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 5)
        
        users = await get_bank()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.red())
        em.add_field(name="Wallet", value=wallet_amt)
        em.add_field(name="Bank Balance", value=bank_amt)
        await ctx.send(embed = em)

    @commands.command()
    @commands.cooldown(1 , 300, commands.BucketType.user) 
    async def beg(self, ctx):
        a = await open_account(ctx.author)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 3.0)
        
        users = await get_bank()
        earnings = random.randrange(301)
        await ctx.send(f"Some one gave you {earnings} coins!!")
        users[str(user.id)]["wallet"] += earnings

        with open("data\mainbank.json", "r+") as f:
            json.dump(users, f)

    @commands.command()
    async def withdraw(self, ctx, amount = None):
        a = await open_account(ctx.author)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 3.0)

        if amount == None:
            await ctx.send("You Idiot You cant withdraw Nothing")
            return

        bal = await update_bank(user)

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("You Dont have that much money")
            return
        if amount<0:
            await ctx.send("You cant withdraw Negative Money")
            return

        await update_bank(user, amount)
        await update_bank(user, -1 * amount, "bank")

        msg = await ctx.send("Loging Into your bank account")
        await asyncio.sleep(2)
        await msg.edit(content = "Making transaction")
        await asyncio.sleep(1)
        await msg.edit(content = "Withdraw success", delete_after = 3.0)

    @commands.command()
    async def deposit(self, ctx, amount = None):
        a = await open_account(ctx.author)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 3.0)

        if amount == None:
            await ctx.send("You Idiot You cant deposit Nothing")
            return

        bal = await update_bank(user)

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("You Dont have that much money")
            return
        elif amount<0:
            await ctx.send("You cant deposit Negative Money")
            return

        await update_bank(user, -1 * amount)
        await update_bank(user, amount, "bank")

        msg = await ctx.send("Walking to the Bank")
        await asyncio.sleep(2)
        await msg.edit(content = "Making transaction")
        await asyncio.sleep(1)
        await msg.edit(content = "Deposit success", delete_after = 3.0)

    @commands.command()
    async def send(self, ctx, member: discord.Member, amount = None):
        a = await open_account(ctx.author)
        b = await open_account(member)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 3.0)

        if b is True:
            msg = await ctx.send(f"{member.mention} dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = f"Created a Bank Account, Name = {member.display_name}", delete_after = 3.0)

        if amount == None:
            await ctx.send("You Idiot You cant send Nothing")
            return

        bal = await update_bank(user)

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("You Dont have that much money")
            return
        elif amount<0:
            await ctx.send("You cant send Negative Money")
            return

        await update_bank(user, -1 * amount, "bank")
        await update_bank(member, amount, "bank")

        msg = await ctx.send("Loging to the Bank")
        await asyncio.sleep(2)
        await msg.edit(content = "Making transaction")
        await asyncio.sleep(1)
        await msg.edit(content = "Transaction success", delete_after = 3.0)


    @commands.command()
    async def gamble(self, ctx, amount = None):
        a = await open_account(ctx.author)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 3.0)

        if amount == None:
            await ctx.send("You Idiot You cant Gamble Nothing")
            return

        bal = await update_bank(user)

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("You Dont have that much money")
            return
        elif amount<0:
            await ctx.send("You cant send Negative Money")
            return

        
        final = []
        for i in range(3):
            b = random.choice(["X", "O", "Q"])

            final.append(b)

        if final[0] == final[1] == final[2]:
            await update_bank(user, 2  * amount)
            await ctx.send("You Won")
        else:
            await update_bank(user, -1 * amount)
            await ctx.send("You Lost!")

    @commands.command()
    async def steal(self, ctx, member: discord.Member):
        a = await open_account(ctx.author)
        b = await open_account(member)
        user = ctx.author

        if a is True:
            msg = await ctx.send("You dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = "Created a Bank Account", delete_after = 3.0)

        if b is True:
            msg = await ctx.send(f"{member.mention} dont have a Bank Account")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating a Bank Account")
            await asyncio.sleep(1)
            await msg.edit(content = f"Created a Bank Account, Name = {member.display_name}", delete_after = 3.0)

        bal = await update_bank(member)

        amount = random.randrange(-300, bal[0])

        amount = int(amount)
        if bal[0]<500:
            await ctx.send("You Dont have that much money")
            return
        if amount<0:
            await update_bank(user,-1 * amount)
            await update_bank(member, amount)
            await ctx.send(f"You were caught and paid { -1 * amount} coins")
        elif amount>0:
            await update_bank(user, amount)
            await update_bank(member, -1 * amount)
            await ctx.send(f"You stole {amount} coins")
        elif amount == 0:
            await ctx.send("It's not safe and you returned with 0 coins")

    @beg.error
    async def beg_handle(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Wait 5 Minutes before sending another message", delete_after = 5.0)
            await ctx.message.delete()

async def open_account(user):
    
    users = await get_bank()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("data\mainbank.json", "r+") as f:
        json.dump(users, f)
    return True

async def get_bank():
    with open("data\mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank()

    users[str(user.id)][mode] += change

    with open("data\mainbank.json", "r+") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

def setup(client):
    client.add_cog(economy(client))