import discord
from PyDictionary import PyDictionary
from discord import file 
from discord.ext import commands

class Educational(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Test", aliases=['mean', '?'])
    async def meaning(self, ctx, word):
        dic = PyDictionary()
        jsn = dic.meaning(str(word))

        try:
            meaning = jsn["Noun"]
            em = discord.Embed(title="Meaning")

            for i in range(len(meaning)):
                if i == 2:
                    break
                else:
                    em.add_field(name=meaning[i], value="\u200c", inline=False)
                
            await ctx.send(embed = em)
        except TypeError:
            await ctx.send(f"There is no meaning for {word}")

    @commands.command()
    async def rt5(self, ctx, num):
        await ctx.send(f"""```cs
let √{int(num)} be a rational then 
√5 = a/b such that a and b are co primes
b√5 = a
sq. on B.S
5b² = a²          ---------------------(1)
So that a² is divisible by 5, a is also divisible by 5
let a = 5c
5b² = (5c)²
5b² = 25c²
b² = 25c²/5
b² = 5c
So that b² is divisible by 5, a is also divisible by 5

∴ A and B have a common factor 5
  This contradicts the fact that A and B are Coprimes ∴ Our assumption is wrong

∴ √5 is Irrational

                         HP//
```""")

    @commands.command()
    async def statistics(self, ctx):
        await ctx.send("""```css
(1) The mean of the grouped data can be found by 3 methods.

Direct Method: x̅ = ∑fixi / ∑fi

Assumed mean method : x̅ = a + ∑fidi / ∑fi

(2) The mode of grouped data:

Mode = l + f1–f0 / 2f1 – f0 – f2 × h

(3) The median for a grouped data:

Median = l + (n / 2) – cf / f × h

```""")

    @commands.command()
    async def trigid(self, ctx):
        await ctx.send("""```css
▪ sin(90° – θ) = cos θ
▪ cos(90° – θ) = sin θ
▪ tan(90° – θ) = cot θ
▪ cot(90° – θ) = tan θ
▪ sec(90° – θ) = cosecθ
▪ cosec(90° – θ) = secθ
▪ sin²θ + cos²θ = 1
▪ sec²θ = 1 + tan²θ
▪ Cosec²θ = 1 + cot²θ
```""")

    @commands.command()
    async def circles(self, ctx):
        await ctx.send("""```css
▪ Circumference of the circle = 2πr
▪ Area of the circle = πr²
▪ Area of the sector of angle θ = (θ/360) × πr²
▪ Length of an arc of a sector of angle θ = (θ/360) × 2πr
        ```""")

    @commands.command()
    async def trig(self, ctx):
        f = discord.File("assets\Trig.png", filename="image.png")
        e = discord.Embed(color = discord.Color.red())
        e.set_image(url="attachment://image.png")
        await ctx.send(file=f, embed=e)

    @commands.command()
    async def lifep(self, ctx):
        with open("assets\Life Process Class 10 Science Notes.pdf", "rb") as f:
            await ctx.send(file = discord.File(f, "Life Process Class 10 Science Notes.pdf"))

    @commands.command()
    async def riseof(self, ctx):
        await ctx.send("""
```cs
1791 - Napoleonic Wars
1799 - Napoleon Gains Power
1804 - Napoleonic Code
1807 - Birth of Giuseppe Mazzini
1814-1815 - Fall of Napoleon
1821 - Greek struggle for Independence
1830 - First Upheaval in France, July
1830 - Economic Crisis in Europe
1832 - Greece gained Independence
1834 - Formation of Zollverein
1848 - Revolutions in Europe Began
1848 - Germans Voted for a Germans only national assembly in France
1848 - Conservatives began to strengthen Monarchy
1855 - Sardinia Participated with British and french in Crimean War
1858 - Cavour formed a alliance with France
1859-1870 - Unification of Italy
1859 - Sardinia-Piedmont with France defeated Austria
1860 - Sardinia-Piedmont forces marched into south Italy
1861 - Victor Emmanuel II was declared the king of United Italy
1866-1871 - Unification of Italy
1871 - Persian king William I was proclaimed emperor of Germany
1905 - Slav nationalism gathered forces in Hapsburg and Ottoman Empire
1914 - Beginning of First World war
```
        """)

    @commands.command()
    async def riseofsymbols(self, ctx):
        await ctx.send("""
```
Broken Chains                - Being Freed
Breastplate with eagle       - Symbol of German Empire
Crown of oak leaves          - Heroism
Sword                        - Readiness to fight
Olive branch around sword    - Willingness to make peace
Black, Red and Gold Tricolor - Flag of Liberal Nationalists in 1848
Rays of the rising sun       - Beginning of new era
```
        """)

def setup(client):
    client.add_cog(Educational(client))