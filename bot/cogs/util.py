from discord.ext import commands
from .. import state

from libs.eval import safeeval
import libs.sorter as sorter
import re


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sort")
    # TODO(syoch): impl auto mode
    async def sort(self, ctx, *, codeblock: str):
        match = re.match(r"```([^\n]*)?\n([^(```)]*)```", codeblock)

        if match is None:
            await ctx.send("Invalid codeblock")
            return

        target = match.group(1)
        code = match.group(2)

        if target == "":
            target = "plain"

        if target not in sorter.table:
            lines = [
                "Unknown target: {}".format(target),
                "",
                "Usage:",
                "  sb@sort",
                "  ```<target>",
                "  code...",
                "  ```",
                "",
                "Available targets:",
                "```",
                "",
                *sorted([
                    f"{avail_target}"
                    for avail_target in sorter.table.keys()
                ]),
                "```",
                "",
                "if target isn't specified, SBot2 will use 'plain' sort"
            ]
            return await ctx.send("\n".join(lines))

        # Sort
        func = sorter.table[target]

        await ctx.send("\n".join([
            f"```{target}",
            func(code),
            "```"
        ]))

    @commands.command(name="eval")
    async def _eval(sender, ctx, *, codeblock: str):
        """
        Evalute python expression in safeeval
        """

        if not state.eval_enabled:
            await ctx.send("eval is disabled")
            return
        try:
            (ret, stdout) = safeeval._eval(codeblock)
            with safeeval.patcher:
                ret = str(ret)
        except Exception as ex:
            import traceback
            await ctx.reply("Exception has occured!\n" +
                            "```\n" +
                            ''.join(traceback.TracebackException.from_exception(ex).format()) +
                            "```")
            return

        # Create Content
        code = codeblock.replace("```", "'''")

        ret_len = len(ret)
        if ret_len >= 1500:
            ret = f"long object({ret_len})"
        ret = ret.replace("```", "'''")

        stdout_len = len(stdout)
        if stdout_len >= 1500:
            stdout = f"long object({stdout_len})"
        stdout = stdout.replace("```", "'''")

        lines = []

        lines.extend([
            "sources",
            "```py",
            code,
            "```",
            ""
        ])

        if ret:
            lines.extend([
                "return value",
                "```",
                ret,
                "```"
            ])

        if stdout:
            lines.extend([
                "standard output",
                "```",
                stdout,
                "```"
            ])

        await ctx.reply("\n".join(lines))

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("A invite link!\nhttps://discord.com/api/oauth2/authorize?client_id=649949366785802260&permissions=8&scope=bot")

    @commands.command()
    async def goukakuritu(self, ctx, *, argument):
        """
        合格回数, 不合格率 を引数として合格率を算出するコマンドです
        """

        match = re.match(r"^(.*[\d)]) +([(\d].*)$", argument)
        if match is None:
            await ctx.send("引数が不正です")
            return

        ok = match.group(1)
        ng = match.group(2)

        (ok, _) = safeeval(ok)
        (ng, _) = safeeval(ng)

        if not (type(ok) is int or type(ok) is float):
            await ctx.send(f"合格回数の値が不正です ({type(ok)} 型です)")
            return

        if not (type(ng) is int or type(ng) is float):
            await ctx.send(f"不合格回数の値が不正です ({type(ng)} 型です)")
            return

        if ok + ng == 0:
            await ctx.send("引数が不正です(合格回数と不合格回数の和が0です)")
            return

        await ctx.send(f"{100 * ok / (ok + ng)}% です 頑張ってください")


def setup(bot):
    bot.add_cog(Util(bot))
