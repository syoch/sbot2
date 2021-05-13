from discord.ext import commands
import discord


import io
import math

import numpy
import matplotlib.pyplot as plt

from util.f2l import f2l
import state


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gravdivdaoijvadoijvadph(self, ctx, *args):
        s = -10
        e = 10
        # parse args
        _formula = []
        flag = "n"  # s:check start e:check end n:none
        for arg in args:
            if flag == "s":
                s = float(arg)
                flag = "n"
            elif flag == "e":
                e = float(arg)
                flag = "n"
            elif arg == "--start":
                flag = "s"
            elif arg == "--end":
                flag = "e"
            else:
                _formula.append(arg)
        formula = "".join(_formula)
        # process
        x = numpy.linspace(s, e, math.ceil(1000*(e-s)))
        ff = f2l(formula)
        f = ff[1]
        # mpl
        plt.figure()
        plt.title("f(x)="+formula)
        plt.xlabel("x")
        plt.ylabel("y")

        plt.plot(x, f(x))

        buf = io.BytesIO(b'')
        plt.savefig(buf)
        await ctx.send(f"<@!{ctx.author.id}>"+"`"+ff[0]+"`", file=discord.File(io.BytesIO(buf.getvalue()), filename="graph.png"))

    @commands.command()
    async def cijigugeugewualc(self, ctx, *, formula):
        try:
            await ctx.send(str(f2l(formula, symbols_="")[1]()))
        except Exception as ex:
            await ctx.send(str(ex))


def setup(bot):
    bot.add_cog(Math(bot))
