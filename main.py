import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logging.info("import Re")
import re
logging.info("import discord")
import discord
logging.info("import mpl.Pyplot")
import matplotlib.pyplot as plt
logging.info("import numpy")
import numpy
logging.info("import io")
import io
logging.info("import subprocess")
import subprocess
logging.info("import math")
import math
logging.info("import Thread")
import threading
logging.info("import http")
import http
logging.info("import os,sys")
import os,sys




#--------------------
#Program utilities
#--------------------
def f2l(formula_,symbols_=["x"]):
    """
    formula_ type is str
    symbols_ type is list or tuple,str

    formula_ Example:3x x x/2 x^2
    symbols_ Example:["x","y"]
    lambda arguments have this func second argument 'symbols_'
    """
    symbols=list(symbols_)
    formula=str(formula_)
    formula=re.sub(r"\|\-?(.*)\|",f"abs(\1)",formula)
    formula=formula.replace("^","**")
    formula=re.sub(r"log\(([^\)]*)\)",r"log(\1)",formula)
    formula=re.sub(r"log\[([^\]]*)\]\(([^\)]*)\)",r"log(\2)/log(\1)",formula)
    formula=formula.replace("asin" ,"arcsin" )
    formula=formula.replace("acos" ,"arccos" )
    formula=formula.replace("atan" ,"arctan" )
    formula=formula.replace("asinh","arcsinh")
    formula=formula.replace("acosh","arccosh")
    formula=formula.replace("atanh","arctanh")
    
    for s in symbols:
        formula=re.sub(rf"{s}\*\*(\d+)",rf"({s}**\1)",formula)
        while True:
            oldf=formula
            formula=re.sub(rf"(\d){s}",rf"(\1*{s})",formula)
            formula=re.sub(rf"{s}\(",rf"{s}*(",formula)
            formula=re.sub(rf"\){s}",rf")*{s}",formula)
            formula=re.sub(rf"{s}{s}",rf"({s}*{s})",formula)
            formula=re.sub(rf"\)\(",rf")*(",formula)
            
            if formula==oldf:
                break
    formula=re.sub(rf"(\d)\(",rf"\1*(",formula)
    return (formula,eval(
        "lambda "+",".join(symbols)+" : "+formula,
        numpy.__dict__,math.__dict__
    ))
    




client=discord.Client()


#--------------------
#Discord Event Handler
#--------------------
@client.event
async def on_ready():
    logging.info("Login on "+client.user.name)

@client.event
async def on_message(msg):
    if(msg.author==client.user):
        return
    content=msg.content.lower()
    if(content[0:2]!="sb"):
        return
    prefix=content.split("@")[0][2:]
    command=content.split("@")[1].split(" ")[0]
    arguments=content.split("@")[1].split(" ")[1:]
    try:
        if(prefix=='u'):
            await    util(msg.channel.send,command,arguments)
        elif(prefix=="g"):
            await general(msg.channel.send,command,arguments)
    except Exception as ex:
        await msg.channel.send("Errrrrrror Durrrrring Command execute")
        await msg.channel.send(str(ex.args))
        raise ex
    



#--------------------
#Category switcher
#--------------------

#General Category
async def general(sender,cmd,arg):
    if(cmd=="help"):await help(sender,arg)

#Utility Category
async def util(sender,cmd,arg):
    if(cmd=="calc"):await calc(sender,"".join(arg))
    if(cmd=="graph"):await graph(sender,arg)
    if(cmd=="eval"):await _eval(sender,arg)



#--------------------
#Commands
#--------------------

#Help
async def help(sender,arg):
    await sender(
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
        r"| | ex. Sbu@eval py 10**2"+"\n"
        #r"\ \ ex. Sbu@eval js console.log(\"Hello world\")"+"\n"
        r""+"\n"
        r""+"\n"
        r"General help"+"\n"
        r"| help"+"\n"
        r"\ \show help"+"\n"
        "```"
    )
#Evalute command
async def _eval(sender,arg):
    laun=arg[0]
    error=""
    stdout=""
    src=" ".join(arg[1:])
    ret=None
    if laun=="py":
        buf=io.StringIO()
        inp=lambda x="":"Input"
        src=re.sub(r"print\(([^\)]*)\)",r"print(\1,file=buf)",src)
        ret=eval(src,{},{"buf":buf,"input":inp})
        stdout=buf.getvalue()
    elif laun=="js":
        src=src.replace("\"","\\\"")
        tmp=subprocess.check_output("js -e \"console.log((()=>{return "+src+"})())\"")\
             .decode().split("\n")[0:-1]
        outs=tmp[0:-1]
        ret=tmp[-1]
        stdout="\n".join(outs)
    else:
        error="unknown laun"
    try:
        await sender(
        f"```{laun}\n"+
        f"laun  :{laun}\n"+
        f"source:{src}\n"+
        f"errors:{error}\n"+
        f"return:{ret}\n"+
        f"output:{stdout}\n"+
        "```"
    )
    except discord.errors.HTTPException as ex:
        await sender("Error:"+ex.text)

#Graphing Command
async def graph(sender,args):
    s=-10
    e=10
    _formula=[]
    flag="n" # s:check start e:check end n:none
    for arg in args:
        if flag=="s":s=int(arg);flag="n"
        elif flag=="e":e=int(arg);flag="n"
        elif arg=="--start":flag="s"
        elif arg=="--end":flag="e"
        else:
            _formula.append(arg)
    formula="".join(_formula)
    x=numpy.arange(s-0.5,e+0.5)
    ff=f2l(formula)
    f=ff[1]
    plt.figure()
    plt.title("f(x)="+formula)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.plot(x,f(x))

    buf=io.BytesIO(b'')
    plt.savefig(buf)
    await sender("`"+ff[0]+"`",file=discord.File(io.BytesIO(buf.getvalue()),filename="graph.png"))

#Calculate Commmand
async def calc(sender,formula):
    try:
        await sender(str(f2l(formula,symbols_="")[1]()))
    except Exception as ex:
        await sender(str(ex))

#--------------------
#Main process
#--------------------
if __name__ == "__main__":
    logging.info("Discord starting")
    client.run("NjQ5OTQ5MzY2Nzg1ODAyMjYw.XgWeyQ.mG3XI3l5ryHuc4NoUQaa0hw7GX4")
