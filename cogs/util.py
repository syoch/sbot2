from discord.ext import commands
import state

import ast
import re
import io
import pathlib

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    async def _eval(sender,ctx, language:str, *,src):
        if not state.state.enabledEval:
            await ctx.send("eval is disabled")
            return
        error = ""
        stdout = ""
        ret = None
        if language == "py":
            utilConf={
                "module":[
                    "subprocess",
                    "importlib",
                    "imp",
                    "pip",
                    "socket",
                    "urllib",
                    "http",
                    "ctypes",
                    "fileinput",
                    "pathlib"
                ],
                "file":[
                    "main.py",
                    "token",
                ],
                "builtinFuncs":{
                    "__import__":"myImport",
                    "range":"myRange",
                    "open":"myOpen",
                    "globals":None,
                    "locals":None,
                    "input":None,
                    "exit":None,
                    "exec":None,
                },
                "funcs":{
                    "sys"      : ["exit"],
                    "os"       : ["system","fork","_exit","popen","abort","chdir","fchdir","getcwd","open","fdopen",],
                    "_thread"  : ["exit","exit_thread"],
                    "time"     : ["sleep"],
                    "io.open"  : ["open","open_code","FileIO"],
                    "_io.open" : ["open","open_code","FileIO"],
                }
            }
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
                if basename in utilConf["module"]:
                    raise Exception(f"Module {basename} is blocked.")
                else:
                    obj = org["__import__"](name, _globals, _locals, fromlist, level)

                if basename in utilConf["funcs"]:
                    for funcnames in utilConf["funcs"][basename]:
                        setattr(obj, funcnames, block(basename+"."+funcnames+"()"))
                return obj

            def block(name: str = ""):
                def wrap(*args):
                    raise Exception(f"{name} is blocked")
                return wrap

            def myOpen(path, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
                basename=pathlib.Path(path).name
                if basename in utilConf["file"]:
                    raise Exception("can't open "+basename+".")
                return open(path, mode,buffering,encoding,errors,newline,closefd,opener)
            
            src = re.sub(r"print\(([^\)]*)\)", r"print(\1,file=buf)", src)

            org={}
            for funcname in utilConf["builtinFuncs"]:
                org[funcname]=__builtins__[funcname]
                if utilConf["builtinFuncs"][funcname]:
                    __builtins__[funcname]=locals()[utilConf["builtinFuncs"][funcname]]
                else:
                    __builtins__[funcname]=block(funcname+"()")

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
                        "__builtins__": __builtins__
                    },
                    {
                        "buf": buf,
                    }
                )
            except Exception as ex:
                error = str(ex)

            for funcname in utilConf["builtinFuncs"]:
                __builtins__[funcname]=org[funcname]
    

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


    async def check_cog(self, ctx):
        if ctx.author.id=="524516049752686592":
            return True
        else:
            ctx.send("This command is blocked( can use by syoch only )")
            return False

def setup(bot):
    bot.add_cog(Util(bot))