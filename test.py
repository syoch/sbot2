from libs.eval import safeeval

safeeval.set_do_logging(True)


def test(x):
    ret, out = safeeval._eval(x)
    print("-----")
    print(ret)
    print("-----")
    print(out)


test('type("",(),{"__str__":lambda s:open(".env").read()})()')
# test('iter(lambda:iter(lambda:1,0),0)')
# test('print(__import__("sys").modules)')
# test('[x for x in  [].__class__.__base__.__subclasses__() if x.__name__ == "BuiltinImporter"][0]().load_module("subprocess").run("ls", shell=True)')
