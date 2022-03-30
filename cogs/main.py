from discord.ext import commands
import logging
from .. import prefix


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_message')
    async def good_reaction(self, message):
        if message.author.bot:
            return
        if message.content.startswith(prefix.get_prefix()):
            logging.info(
                f"command has called by {message.author.name}: {message.content}")


def setup(bot):
    bot.add_cog(Main(bot))
