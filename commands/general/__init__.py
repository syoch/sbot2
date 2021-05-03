from .help import help


async def general(sender, cmd, arg):
    if(cmd == "help"):
        await help(sender, arg)
