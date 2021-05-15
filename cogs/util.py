from discord.ext import commands
import state

import eval


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    async def _eval(sender, ctx, *, aaa: str):
        if not state.state.enabledEval:
            await ctx.send("eval is disabled")
            return
        # Get Codeblock
        codeblock_start = aaa.index("```")+3
        codeblock_end = aaa.rindex("```")
        codeblock = aaa[codeblock_start:codeblock_end]

        # Get language
        language_end = codeblock.index("\n")
        language = codeblock[0:language_end]
        codeblock = codeblock[language_end:]

        stdout = ""
        ret = None
        if language == "py":
            (ret, stdout) = eval._eval(codeblock)
        else:
            ret = "Error:  Unknown language"

        try:
            content = ""
            content += f"source"+"\n"
            content += f"```{language}"+"\n"
            content += f"{codeblock}"+"\n"
            content += f"```"+"\n"
            content += f""+"\n"

            if ret:
                content += f"return value"+"\n"
                content += f"```"+"\n"
                content += f"{ret}"+"\n"
                content += f"```"+"\n"

            if stdout:
                content += f"stdout"+"\n"
                content += f"```"+"\n"
                content += f"{stdout}"+"\n"
                content += f"```"+"\n"

            await ctx.send(content)
        except Exception as ex:
            await ctx.send("Exception has occured!\n" +
                           str(type(ex))+":"+str(ex))


def setup(bot):
    bot.add_cog(Util(bot))
