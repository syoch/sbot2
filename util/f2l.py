import re
import numpy
import math


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
    formula = re.sub(r"log([^\]]*)\(([^\)]*)\)",
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
    return formula
