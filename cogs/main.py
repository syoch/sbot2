from discord.ext import commands
import discord

import io
import math
import sys
import pathlib
import re
import ast
import logging

import numpy
import matplotlib.pyplot as plt

from util.f2l import f2l

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def oldHelp(self, ctx):
        await ctx.send(
            "```\n"
            r"Sbot v2 help"+"\n"
            r"Sb<category>@<command> <arg...>"+"\n"
            r""+"\n"
            r"Categories"+"\n"
            r"| [U]Utility"+"\n"
            r"\ [G]General"+"\n"
            r""+"\n"
            r""+"\n"
            r"Utilities help"+"\n"
            r"| calc <formula:string>"+"\n"
            r"| | Calculate formula"+"\n"
            r"| \ ex. Sbu@calc 10^(log[10](100))"+"\n"
            r"| "+"\n"
            r"| graph <formula:string>"+"\n"
            r"| | Draw a graph by formula"+"\n"
            r"| \ ex. Sbu@graph sin(x)"+"\n"
            r"| "+"\n"
            r"| eval <laun:str> <program:str>"+"\n"
            r"| | Evalute a program in arg with laun"+"\n"
            r"| | Supported Languages"+"\n"
            r"| | \ py"+"\n"
            r"\ \ ex. Sbu@eval py 10**2"+"\n"
            r""+"\n"
            r""+"\n"
            r"General help"+"\n"
            r"| help"+"\n"
            r"\ \show help"+"\n"
            "```"
        )
    
    @commands.group()
    async def util(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('This command is needed subcommand.\n'+
                           'subcommands are eval, calc and graph.')
    
    @util.command()
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
        await ctx.send("`"+ff[0]+"`", file=discord.File(io.BytesIO(buf.getvalue()), filename="graph.png"))
    
    @util.command()
    async def calc(self, ctx, *,formula):
        try:
            await ctx.send( str(f2l(formula, symbols_="")[1]()) )
        except Exception as ex:
            await ctx.send(str(ex))

    @util.command(name="eval")
    async def _eval(sender,ctx, language:str, *,src):
        error = ""
        stdout = ""
        ret = None
        if language == "py":
            buf = io.StringIO()

            def myRange(a=0, b=0, c=1):
                start = 0
                end = 0
                step = c

                if b == 0:  # argument count == 1
                    end = a
                else:
                    start = a
                    end = b
                if end > 10**10:
                    end = 100
                return range(a, b, c)

            def myImport(name, _globals=None, _locals=None, fromlist=(), level=0):
                basename = name.split(".")[0]
                if basename == "subprocess":
                    raise Exception("module subprocess is blocked")
                elif basename == "importlib":
                    raise Exception("module importlib is blocked")
                elif basename == "imp":
                    raise Exception("module imp is blocked")
                elif basename == "pip":
                    raise Exception("module pip is blocked")
                elif basename == "socket":
                    raise Exception("module socket is blocked")
                elif basename == "urllib":
                    raise Exception("module urllib is blocked")
                elif basename == "http":
                    raise Exception("module http is blocked")
                elif basename == "ctypes":
                    raise Exception("module ctypes is blocked")
                elif basename == "fileinput":
                    raise Exception("module fileinput is blocked")
                else:
                    obj = orgImport(name, _globals, _locals, fromlist, level)

                if basename == "sys":
                    obj.exit = block("sys.exit()")
                elif basename == "os":
                    obj.system = block("os.system()")
                    obj.fork = block("os.fork()")
                    obj._exit = block("os._exit()")
                    obj.popen = block("os.popen()")
                    obj.abort = block("os.abort()")
                    obj.chdir = block("os.chdir()")
                    obj.fchdir = block("os.fchdir()")
                    obj.getcwd = block("os.getcwd()")
                    obj.open = block("os.open()")
                    obj.fdopen = block("os.fdopen()")
                elif basename == "io":
                    obj.open = block("io.open()")
                    obj.open_code = block("io.open_code()")
                    obj.FileIO = block("io.FileIO()")
                return obj

            def block(name: str = ""):
                def wrap(*args):
                    raise Exception(f"{name} is blocked")
                return wrap

            def myOpen(path, modifier="r"):
                if pathlib.Path(path).name == "main.py":
                    raise Exception("can't open main.py.")
                return open(path, modifier)
            inp = lambda x="": "Input"
            src = re.sub(r"print\(([^\)]*)\)", r"print(\1,file=buf)", src)

            orgImport = __import__

            VMbuiltins = __builtins__
            VMbuiltins["__import__"] = myImport

            try:
                # check (ListComp attack)
                for node in ast.walk(ast.parse(src)):
                    if type(node) == ast.ListComp:
                        iters = []
                        for generator in node.generators:
                            if type(generator.iter) is not ast.Name:
                                continue
                            iters.append(generator.iter.id)

                        calls = []
                        for node2 in ast.walk(node.elt):
                            if type(node2) == ast.Call:
                                calls.append(node2)

                        for call in calls:
                            if type(call.func) != ast.Attribute():
                                continue
                            if call.func.attr != "append":
                                continue

                            if type(call.func.value) is not ast.Name:
                                continue
                            if call.func.value.id not in iters:
                                continue

                            raise Exception("ListComp Attack has detected!!!")
                ret = eval(
                    src,
                    {
                        "__builtins__": VMbuiltins
                    },
                    {
                        "buf": buf,
                        "input": inp,
                        "exit": block("exit()"),
                        "range": myRange,
                        "exec": block("exec()"),
                        "open": myOpen,
                        "globals": block("globals"),
                        "locals": block("locals")
                    }
                )
            except Exception as ex:
                error = str(ex)

            VMbuiltins["__import__"] = orgImport

            stdout = buf.getvalue()
        else:
            error = "Unknown laun"
        
        try:
            await ctx.send(
                f"```{language}\n" +
                f"lang  : {language}\n" +
                f"source: {src}\n" +
                f"errors: {error}\n" +
                f"return: {ret}\n" +
                f"output: {stdout}\n" +
                "```"
            )
        except Exception as ex:
            await ctx.send("Exception has occured!\n"+
                           str(type(ex))+":"+str(ex))

def setup(bot):
    bot.add_cog(Main(bot))