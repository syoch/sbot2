from libs.eval import safeeval
import os
import socket


def test(x):
    ret, out = safeeval._eval(x)
    print(ret)
    print("-----")
    print(out)


test('__import__("subprocess").getcwd()')
test('__import__("math")')
