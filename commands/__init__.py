from .general import general
from .util import util

async def command(sender,command,arguments):
    if(prefix == 'u'):
        await util(token_filter, command, arguments)
    elif(prefix == "g"):
        await general(token_filter, command, arguments)