import logging
import signal
from discord.ext import commands
import traceback
import os
import sys
import dotenv

sys.path.append(os.getcwd()+"/libs")

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.info("setup signal handler...")
signal.signal(signal.SIGINT, signal.SIG_DFL)

INITIAL_EXTENSIONS = [
    "cogs.main",
    "cogs.admin",
    "cogs.util",
    "cogs._math",
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
    dotenv.load_dotenv(verbose=True)

    prefix = "sb:t@" if os.getenv("DISCORD_BOT_MODE") == "test" else "sb@"

    client = MyBot(command_prefix=prefix)

    client.run(os.getenv("DISCORD_TOKEN"))
