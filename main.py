import pathlib
import os
import signal
import ast
import http
import threading
import math
import subprocess
import io
import numpy
import matplotlib.pyplot as plt
import discord
import re
from math import ceil
import logging
import sys
default_importCache = sys.modules

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.info("import Re")
logging.info("import discord")
logging.info("import mpl.Pyplot")
logging.info("import numpy")
logging.info("import io")
logging.info("import subprocess")
logging.info("import math")
logging.info("import Thread")
logging.info("import http")
logging.info("import os,sys,pathlib")
logging.info("import ast")

logging.info("setup signal handler...")
signal.signal(signal.SIGINT, signal.SIG_DFL)

TOKEN = "NjQ5OTQ5MzY2Nzg1ODAyMjYw.XeEOhA.KCvJ5GSSA6rs43JEG2QwQZdlr4g"


def abcfegogeg():
    global client
    C = client
    _z = len([])
    _a = _z**_z
    _b = _a+_a
    _c = _b+_a
    a = _c+_b*(_c+(_b*_b)*(_c+_b*(_c+_a)))
    b = _b*_b*(_b*_c*(_b+_c)-_a)
    c = b-_b
    __builtins__.__dict__[chr(a+_b*_c)+chr(a+_b*_b)+chr(b)+chr(a)+_b*chr(b)+chr(b-_b)](C, chr(b-_b)+chr(b+_a)+chr(b-_b*_c))(
        eval(chr(a-_a-_b*_b*_c)+chr((_b**(_b*_c)+_b**_c*_b)-_a)+chr(a-_b*(_c+_b**_c))+chr(a-_b**_c*_c-_b**_b)+chr(a-_a-_c**_b*_b)))

# --------------------
# Program utilities
# --------------------


def f2l(formula_, symbols_=["x"]):
    """
    formula_ type is str
    symbols_ type is list or tuple,str

    formula_ Example:3x x x/2 x^2
    symbols_ Example:["x","y"]
    lambda arguments have this func second argument 'symbols_'
    """
    symbols = list(symbols_)
    formula = str(formula_)
    formula = re.sub(r"\|\-?(.*)\|", r"abs(\1)", formula)
    formula = formula.replace("^", "**")
    formula = re.sub(r"log\(([^\)]*)\)", r"log(\1)", formula)
    formula = re.sub(r"log\[([^\]]*)\]\(([^\)]*)\)",
                     r"log(\2)/log(\1)", formula)
    formula = formula.replace("asin", "arcsin")
    formula = formula.replace("acos", "arccos")
    formula = formula.replace("atan", "arctan")
    formula = formula.replace("asinh", "arsinh")
    formula = formula.replace("acosh", "arccosh")
    formula = formula.replace("atanh", "arctanh")
    for s in symbols:
        formula = re.sub(rf"{s}\*\*(\d+)", rf"({s}**\1)", formula)
        while True:
            oldf = formula
            formula = re.sub(rf"(\d+){s}", rf"(\1*{s})", formula)
            formula = re.sub(rf"{s}\(", rf"{s}*(", formula)
            formula = re.sub(rf"\){s}", rf")*{s}", formula)
            formula = re.sub(rf"{s}{s}", rf"({s}*{s})", formula)
            formula = re.sub(rf"\)\(", rf")*(", formula)

            if formula == oldf:
                break
    formula = re.sub(rf"(\d)\(", rf"\1*(", formula)
    return (formula, eval(
        "lambda "+",".join(symbols)+" : "+formula,
        numpy.__dict__, math.__dict__
    ))


client = discord.Client()


# --------------------
# Discord Event Handler
# --------------------
@client.event
async def on_ready():
    logging.info("Login on "+client.user.name)
    await client.change_presence(status=discord.Status.offline)


@client.event
async def on_message(msg):
    if(msg.author == client.user):
        return
    a = (msg.content+" ").index(" ")
    content = msg.content[:a].lower()+msg.content[a:]
    if(content[0:2] != "sb"):
        return
    if(content[3] != "@"):
        return
    prefix = content.split("@")[0][2:]
    command = content.split("@")[1].split(" ")[0]
    arguments = content.split("@")[1].split(" ")[1:]
    print("command has invoked by ", msg.author,
          ",command : ", prefix, command, arguments)

    async def token_filter(content, **kwargs):
        content = content.replace(TOKEN, "<TOKEN>")
        return await msg.channel.send(content, **kwargs)
    try:
        if(prefix == 'u'):
            await util(token_filter, command, arguments)
        elif(prefix == "g"):
            await general(token_filter, command, arguments)
    except Exception as ex:
        await msg.channel.send("Errrrrrror Whhiiiileee Command execute")
        await token_filter(str(ex.args))
        raise ex


# --------------------
# Category switcher
# --------------------

# General Category
async def general(sender, cmd, arg):
    if(cmd == "help"):
        await help(sender, arg)

# Utility Category


async def util(sender, cmd, arg):
    if(cmd == "calc"):
        await calc(sender, "".join(arg))
    if(cmd == "graph"):
        await graph(sender, arg)
    if(cmd == "eval"):
        await _eval(sender, arg)


# --------------------
# Commands
# --------------------

# Help
async def help(sender, arg):
    await sender(
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
        r"| | ex. Sbu@eval py 10**2"+"\n"
        #r"\ \ ex. Sbu@eval js console.log(\"Hello world\")"+"\n"
        r""+"\n"
        r""+"\n"
        r"General help"+"\n"
        r"| help"+"\n"
        r"\ \show help"+"\n"
        "```"
    )
# Evalute command


async def _eval(sender, arg):
    laun = arg[0]
    error = ""
    stdout = ""
    src = " ".join(arg[1:])
    ret = None
    if laun == "py":
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
            else:
                obj = orgImport(name, _globals, _locals, fromlist, level)

            if name == "sys":
                obj.exit = block("sys.exit()")
            elif name == "os":
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
            elif name == "io":
                obj.open = block("io.open()")
                obj.open_code = block("io.open_code()")
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

        VMglobal = {}
        VMglobal["__builtins__"] = globals()["__builtins__"]
        orgImport = VMglobal["__builtins__"].__import__
        VMglobal["__builtins__"].__import__ = myImport

        org_modules = sys.modules
        sys.modules = default_importCache

        try:
            # check (ListComp attack)
            for node in ast.walk(ast.parse(src)):
                if type(node) == ast.ListComp:
                    iters = []
                    for generator in node.generators:
                        iters.append(generator.iter.id)

                    calls = []
                    for node2 in ast.walk(node.elt):
                        if type(node2) == ast.Call:
                            calls.append(node2)

                    for call in calls:
                        if call.func.attr != "append":
                            continue
                        if call.func.value.id not in iters:
                            continue

                        raise Exception("ListComp Attack has detected!!!")
            ret = eval(
                src,
                VMglobal,
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

        VMglobal["__builtins__"].__import__ = orgImport
        sys.modules = org_modules

        stdout = buf.getvalue()
    # elif laun=="js":
    #     src=src.replace("\"","\\\"")
    #     tmp=subprocess.check_output("js -e \"console.log((()=>{return "+src+"})())\"")\
    #          .decode().split("\n")[0:-1]
    #     outs=tmp[0:-1]
    #     ret=tmp[-1]
    #     stdout="\n".join(outs)
    else:
        error = "unknown laun"
    try:
        await sender(
            f"```{laun}\n" +
            f"lang  : {laun}\n" +
            f"source: {src}\n" +
            f"errors: {error}\n" +
            f"return: {ret}\n" +
            f"output: {stdout}\n" +
            "```"
        )
    except discord.errors.HTTPException as ex:
        await sender("Error:"+ex.text)

# Graphing Command


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
    x = numpy.linspace(s, e, ceil(1000*(e-s)))
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

# Calculate Commmand


async def calc(sender, formula):
    try:
        await sender(str(f2l(formula, symbols_="")[1]()))
    except Exception as ex:
        await sender(str(ex))

# --------------------
# Main process
# --------------------
if __name__ == "__main__":

    logging.info("Discord starting")
    abcfegogeg()
