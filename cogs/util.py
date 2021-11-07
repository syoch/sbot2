from discord.ext import commands
import state

from libs.eval import _eval as safeeval
import libs.sorter as sorter
import re


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sort")
    # TODO(syoch): impl auto mode
    async def sort(self, ctx, target: str = "normal", *, codeblock: str):
        if target not in sorter.table:
            lines = [
                "Unknown target: {}".format(target),
                "",
                "Available targets:",
                "```",
                "",
                *sorted([
                    f"{avail_target} ({sorter.table[avail_target][0]})"
                    for avail_target in sorter.table.keys()
                ]),
                "```",
                "",
                "if target isn't specified, SBot2 will use 'normal' sort"
            ]
            return await ctx.send("\n".join(lines))

        # Get raw code block
        block = codeblock
        block = block[block.find("```"):]
        match = re.match(r"```[^\n]*?\n([^(```)]*)\n```", block)

        if not match:
            return await ctx.send("Invalid codeblock.")

        block = match.group(1)

        # Sort
        (language, func) = sorter.table[target]

        await ctx.send("\n".join([
            f"```{language}",
            func(block),
            "```"
        ]))

    @commands.command(name="eval")
    async def _eval(sender, ctx, language, *, codeblock: str):
        if not state.state.enabledEval:
            await ctx.send("eval is disabled")
            return
        stdout = ""
        ret = None
        try:
            if language == "py":
                (ret, stdout) = safeeval(codeblock)
            else:
                ret = "Error:  Unknown language"

            # Create Content
            code = codeblock.replace("```", "'''")

            content = ""
            content += f"source"+"\n"
            content += f"```{language}"+"\n"
            content += f"{code}"+"\n"
            content += f"```"+"\n"
            content += f""+"\n"

            if ret:
                content += f"return value"+"\n"
                content += f"```"+"\n"
                ret_len = len(str(ret))
                if ret_len >= 1500:
                    content += f"long object({ret_len})"+"\n"
                else:
                    tmp = str(ret).replace("```", "'''")
                    content += f"{tmp}"+"\n"
                content += f"```"+"\n"
            if stdout:
                content += f"stdout"+"\n"
                content += f"```"+"\n"
                stdout_len = len(str(stdout))
                if stdout_len >= 1500:
                    content += f"long object({stdout_len})"+"\n"
                else:
                    tmp = str(stdout).replace("```", "'''")
                    content += f"{tmp}"+"\n"
                content += f"```"+"\n"

            await ctx.reply(content)
        except Exception as ex:
            import traceback
            await ctx.reply("Exception has occured!\n" +
                            "```\n" +
                            ''.join(traceback.TracebackException.from_exception(ex).format()) +
                            "```")


def setup(bot):
    bot.add_cog(Util(bot))
