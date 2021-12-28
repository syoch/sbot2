from discord.ext import commands
import discord


import io
import math

import numpy
import sympy
import sympy.tensor
import matplotlib.pyplot as plt

from libs.expr_conv import f2l as converter
import state
from libs.eval import _eval as safeeval


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def graph(self, ctx, *args):
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
        # mpl
        plt.figure()
        plt.title("f(x)="+formula)
        plt.xlabel("x")
        plt.ylabel("y")

        funcs = math.__dict__
        funcs.update(numpy.__dict__)
        funcs.update(x=x)
        y = safeeval(converter(formula), funcs)[0]
        if type(y) == str:  # blocked or syntax?
            await ctx.reply(str(y))
            return

        plt.plot(x, y)

        buf = io.BytesIO(b'')
        plt.savefig(buf)
        await ctx.reply(file=discord.File(io.BytesIO(buf.getvalue()), filename="graph.png"))

    @commands.command()
    async def calc(self, ctx, *, formula):
        try:
            funcs = math.__dict__
            funcs.update(numpy.__dict__)
            await ctx.reply(
                "`" +
                str(safeeval(converter(formula), funcs)
                    [0]).replace("`", "'") +
                "`"
            )
        except Exception as ex:
            await ctx.send(str(ex))

    @commands.command()
    async def eval_sym(self, ctx, *, formula):
        try:
            funcs = math.__dict__
            funcs.update(sympy.__dict__)
            await ctx.reply(
                "`" +
                str(safeeval(formula, funcs)
                    [0]).replace("`", "'") +
                "`"
            )
        except Exception as ex:
            await ctx.send(str(ex))


def setup(bot):
    bot.add_cog(Math(bot))
