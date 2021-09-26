import subprocess
from discord.ext import commands
import state


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def switchEval(self, ctx):
        state.state.enabledEval ^= 1
        await ctx.send(f"state.enabledEval = {state.state.enabledEval}")

    def reload(self, name):
        try:
            a = self.bot.reload_extension(name)
        except Exception as ex:
            a = type(ex).__name__+": "+str(ex)
        ret = str(a)
        if not ret:
            ret = "None"
        return ret

    @commands.is_owner()
    @commands.command()
    async def reloadall(self, ctx):
        await ctx.send("updating source")
        output = subprocess.check_output(["./scripts/update.sh"])
        await ctx.send(output.decode("utf-8"))

        await ctx.send("Reloading all cogs...")
        extensions = list(self.bot.extensions.keys())
        result = [
            str(cog).ljust(10) + " -> " + self.reload(cog)
            for cog in extensions
            if cog != self.qualified_name
        ]
        await ctx.send("\n".join(["```", *result, "```"]))

    async def check_cog(self, ctx):
        if ctx.author.id == "524516049752686592":
            return True
        else:
            await ctx.send("Cannot invoke the command by you")
            return False


def setup(bot):
    bot.add_cog(Admin(bot))
