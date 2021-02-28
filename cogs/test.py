from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test")
    async def test(self, ctx):
        pass


def setup(client):
    client.add_cog(Test(client))