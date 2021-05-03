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


    async def check_cog(self, ctx):
        if ctx.author.id=="524516049752686592":
            return True
        else:
            ctx.send("This command is blocked( can use by syoch only )")
            return False

def setup(bot):
    bot.add_cog(Util(bot))