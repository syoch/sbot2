from .general import general
from .util import util

async def command(sender,prefix,command,arguments):
    if(prefix == 'u'):
        await util(sender, command, arguments)
    elif(prefix == "g"):
        await general(sender, command, arguments)