from discord.ext import commands
import discord

import logging

import state

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_message')
    async def good_reaction(self, message):
        if message.author.bot:
            return
        if message.content.startswith("sb@"):
            logging.info(f"command has called by {message.author.name}: {message.content}")
            
    @commands.command()
    async def oldHelp(self, ctx):
        await ctx.send(
            "```\n"
            r"Sbot v2 help"+"\n"
            r"Sb<category>@<command> <arg...>"+"\n"
            r""+"\n"
            r"Categories"+"\n"
            r"| [U]Utility"+"\n"
            r"\ [G]General"+"\n"
            r""+"\n"
            r""+"\n"
            r"Utilities help"+"\n"
            r"| calc <formula:string>"+"\n"
            r"| | Calculate formula"+"\n"
            r"| \ ex. Sbu@calc 10^(log[10](100))"+"\n"
            r"| "+"\n"
            r"| graph <formula:string>"+"\n"
            r"| | Draw a graph by formula"+"\n"
            r"| \ ex. Sbu@graph sin(x)"+"\n"
            r"| "+"\n"
            r"| eval <laun:str> <program:str>"+"\n"
            r"| | Evalute a program in arg with laun"+"\n"
            r"| | Supported Languages"+"\n"
            r"| | \ py"+"\n"
            r"\ \ ex. Sbu@eval py 10**2"+"\n"
            r""+"\n"
            r""+"\n"
            r"General help"+"\n"
            r"| help"+"\n"
            r"\ \show help"+"\n"
            "```"
        )

def setup(bot):
    bot.add_cog(Main(bot))