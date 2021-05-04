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
                ]
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
                    obj = org___import__(name, _globals, _locals, fromlist, level)

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
                elif basename == "io" or basename=="_io":
                    obj.open = block(basename+".open()")
                    obj.open_code = block(basename+".open_code()")
                    obj.FileIO = block(basename+".FileIO()")
                elif basename == "_thread":
                    obj.exit=block("_thread.exit()")
                    obj.exit_thread=block("_thread.exit_thread()")
                elif basename== "time":
                    obj.sleep=block("time.sleep()")
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

            org___import__ = __builtins__["__import__"]
            org_range      = __builtins__["range"]
            org_open       = __builtins__["open"]
            org_globals    = __builtins__["globals"]
            org_locals     = __builtins__["locals"]
            org_input      = __builtins__["input"]
            org_exit       = __builtins__["exit"]
            org_exec       = __builtins__["exec"]

            VMbuiltins = __builtins__
            VMbuiltins["__import__"] = myImport
            VMbuiltins[     "range"] = myRange
            VMbuiltins[      "open"] = myOpen
            VMbuiltins[   "globals"] = block("globals")
            VMbuiltins[    "locals"] = block("locals")
            VMbuiltins[     "input"] = block("input()")
            VMbuiltins[      "exit"] = block("exit()")
            VMbuiltins[      "exec"] = block("exec()")

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
                    }
                )
            except Exception as ex:
                error = str(ex)

            __builtins__["__import__"] = org___import__
            __builtins__[     "range"] = org_range
            __builtins__[      "open"] = org_open
            __builtins__[   "globals"] = org_globals
            __builtins__[    "locals"] = org_locals
            __builtins__[     "input"] = org_input
            __builtins__[      "exit"] = org_exit
            __builtins__[      "exec"] = org_exec

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