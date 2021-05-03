import pathlib
import io
import re
import ast
import discord

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
            elif basename == "ctypes":
                raise Exception("module ctypes is blocked")
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