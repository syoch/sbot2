from discord.ext import commands
import state

import eval


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    async def _eval(sender, ctx, language: str, *, src):
        if not state.state.enabledEval:
            await ctx.send("eval is disabled")
            return
        stdout = ""
        ret = None
        if language == "py":
            (ret, stdout) = eval._eval(src)
        else:
            ret = "Error:  Unknown language"

        try:
            await ctx.send(
                f"```{language}\n" +
                f"lang  : {language}\n" +
                f"source: {src}\n" +
                f"errors: {error}\n" +
                f"return: {ret}\n" +
                f"output: {stdout}\n" +
                "```"
            )
        except Exception as ex:
            await ctx.send("Exception has occured!\n" +
                           str(type(ex))+":"+str(ex))


def setup(bot):
    bot.add_cog(Util(bot))
