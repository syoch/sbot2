import commands
import logging
import signal
from discord.ext import commands

class MyBot(commands.Bot):

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        logging.info("Login on "+self.user.name)

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.info("setup signal handler...")
signal.signal(signal.SIGINT, signal.SIG_DFL)

TOKEN = "NjQ5OTQ5MzY2Nzg1ODAyMjYw.XeEOhA.KCvJ5GSSA6rs43JEG2QwQZdlr4g"




client = discord.Client()



@client.event
async def on_message(msg):
    if(msg.author == client.user):
        return
    a = (msg.content+" ").index(" ")
    content = msg.content[:a].lower()+msg.content[a:]
    if(content[0:2] != "sb"):
        return
    if(content[3] != "@"):
        return
    prefix = content.split("@")[0][2:]
    command = content.split("@")[1].split(" ")[0]
    arguments = content.split("@")[1].split(" ")[1:]
    print("command has invoked by ", msg.author,
          ",command : ", prefix, command, arguments)

    async def token_filter(content, **kwargs):
        content = content.replace(TOKEN, "<TOKEN>")
        return await msg.channel.send(content, **kwargs)
    try:
        await commands.command(token_filter,prefix,command,arguments)
    except Exception as ex:
        await msg.channel.send("Errrrrrror Whhiiiileee Command execute")
        await token_filter(str(ex.args))
        raise ex



# --------------------
# Main process
# --------------------
if __name__ == "__main__":
    client = MyBot(command_prefix='sb@')
    C = client
    _z = len([])
    _a = _z**_z
    _b = _a+_a
    _c = _b+_a
    a = _c+_b*(_c+(_b*_b)*(_c+_b*(_c+_a)))
    b = _b*_b*(_b*_c*(_b+_c)-_a)
    c = b-_b
    __builtins__.__dict__[chr(a+_b*_c)+chr(a+_b*_b)+chr(b)+chr(a)+_b*chr(b)+chr(b-_b)](C, chr(b-_b)+chr(b+_a)+chr(b-_b*_c))(eval(chr(a-_a-_b*_b*_c)+chr((_b**(_b*_c)+_b**_c*_b)-_a)+chr(a-_b*(_c+_b**_c))+chr(a-_b**_c*_c-_b**_b)+chr(a-_a-_c**_b*_b)))