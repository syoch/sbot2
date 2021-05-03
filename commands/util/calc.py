from util.f2l import f2l

async def calc(sender, formula):
    try:
        await sender(str(f2l(formula, symbols_="")[1]()))
    except Exception as ex:
        await sender(str(ex))