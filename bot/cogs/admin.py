import subprocess
import sys
import importlib
from discord.ext import commands
from .. import state


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def switch_eval(self, ctx):
        state.eval_enabled ^= 1
        await ctx.send(f"state.enabledEval = {state.eval_enabled}")

    def reload(self, name):
        try:
            a = self.bot.reload_extension(name)
        except Exception as ex:
            a = type(ex).__name__+": "+str(ex)
        ret = str(a)
        if not ret:
            ret = "None"
        return ret

    @commands.command()
    async def reload_module(self, ctx, *, name: str):
        ret = importlib.reload(sys.modules[name])
        await ctx.send(f"reloading `{name}` -> `{ret}`")

    @commands.command()
    async def reload_all(self, ctx):
        """
        Fetch source code. And, reload All cogs
        """

        await ctx.send("Updating source")
        output = subprocess.check_output(["./scripts/update.sh"])
        await ctx.send("```"+output.decode("utf-8")+"```")

        await ctx.send("Reloading all cogs...")
        extensions = list(self.bot.extensions.keys())
        result = [
            str(cog).ljust(10) + " -> " + self.reload(cog)
            for cog in extensions
            if cog != self.qualified_name
        ]
        await ctx.send("\n".join(["```", *result, "```"]))

    @commands.command()
    async def fulleval(self, ctx, *, code):
        try:
            await ctx.send(eval(code))
        except Exception as ex:
            await ctx.send(str(ex))

    async def cog_before_invoke(self, ctx):
        if ctx.author.id != 524516049752686592:
            raise commands.CommandError(
                "You are not permitted to use this command")


def setup(bot):
    bot.add_cog(Admin(bot))
