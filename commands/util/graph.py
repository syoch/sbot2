import numpy
import util
import io
import matplotlib.pyplot as plt
import math
from util.f2l import f2l
import discord

async def graph(sender, args):
    s = -10
    e = 10
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
    x = numpy.linspace(s, e, math.ceil(1000*(e-s)))
    ff = f2l(formula)
    f = ff[1]
    plt.figure()
    plt.title("f(x)="+formula)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.plot(x, f(x))

    buf = io.BytesIO(b'')
    plt.savefig(buf)
    await sender("`"+ff[0]+"`", file=discord.File(io.BytesIO(buf.getvalue()), filename="graph.png"))