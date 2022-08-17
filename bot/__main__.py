import logging
import signal
from discord.ext import commands
import discord
import traceback
import os
import sys
import dotenv
from . import prefix

sys.path.append(os.getcwd()+"/libs")

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.info("setup signal handler...")
signal.signal(signal.SIGINT, signal.SIG_DFL)

INITIAL_EXTENSIONS = [
    ".cogs.admin",
    ".cogs.util",
    ".cogs._math",
]


class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog, package=__package__)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        logging.info("Login on "+self.user.name)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith(prefix.get_prefix()):
            logging.info(
                f"command has called by {message.author.name}: {message.content}")

        await super().on_message(message)

    async def on_command_error(self, context, exception):

        if isinstance(exception, commands.CommandNotFound):
            return

        if isinstance(exception, commands.MissingRequiredArgument):
            await context.send(
                f"Error: `{context.command.name}` requires `{exception.param.name}`")
            return

        if isinstance(exception, commands.CommandOnCooldown):
            await context.send(
                f"Error: `{context.command.name}` is on cooldown. Try again in `{exception.retry_after}` seconds.")
            return

        await context.send(f"Error: ```{exception}```")


if __name__ == "__main__":
    environ = dotenv.dotenv_values()

    prefix.auto_set_prefix(environ["DISCORD_BOT_MODE"])
    TOKEN = environ["DISCORD_TOKEN"]

    client = MyBot(command_prefix=prefix.get_prefix())

    client.run(TOKEN)
