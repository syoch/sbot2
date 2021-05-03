import util

async def calc(sender, formula):
    try:
        await sender(str(util.f2l(formula, symbols_="")[1]()))
    except Exception as ex:
        await sender(str(ex))