from libs.eval import safeeval
import os
import socket
import subprocess
import sys


def test(x):
    ret, out = safeeval._eval(x)
    print(ret)
    print("-----")
    print(out)


test('open(".env").read()')
test('print(__import__("sys").modules)')
test('[x for x in  [].__class__.__base__.__subclasses__() if x.__name__ == "BuiltinImporter"][0]().load_module("subprocess").run("ls", shell=True)')

print(__import__)
