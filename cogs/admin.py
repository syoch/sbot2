from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_cog(self, ctx):
        if ctx.author.id=="524516049752686592":
            return True
        else:
            ctx.send("This command is blocked( can use by syoch only )")
            return False

def setup(bot):
    bot.add_cog(Admin(bot))