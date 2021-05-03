from . import calc
from . import graph
from . import _eval

async def util(sender, cmd, arg):
    if(cmd == "calc"):
        await calc.calc(sender, "".join(arg))
    if(cmd == "graph"):
        await graph.graph(sender, arg)
    if(cmd == "eval"):
        await _eval._eval(sender, arg)