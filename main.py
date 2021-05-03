import logging
import signal
from discord.ext import commands
import traceback

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.info("setup signal handler...")
signal.signal(signal.SIGINT, signal.SIG_DFL)

# TOKEN
if 1==1:
    TOKEN = "NjQ5OTQ5MzY2Nzg1ODAyMjYw.XeEOhA.KCvJ5GSSA6rs43JEG2QwQZdlr4g"
    pass

INITIAL_EXTENSIONS=[
    "cogs.main"
]
class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        logging.info("Login on "+self.user.name)

if __name__ == "__main__":
    client = MyBot(command_prefix=('sb@'))
    client.run(TOKEN)
    