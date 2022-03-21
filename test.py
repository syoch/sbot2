from libs import eval
import os
import socket


def test(x):
    ret, out = eval._eval(x)
    print(ret)
    print("-----")
    print(out)


test('__import__("math")')
test('__import__("math")')
