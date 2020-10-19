import discord
import time
import asyncio
from collections import defaultdict
from discord.ext import commands, tasks
class Chair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session={}
        self.delegate=self.bot.get_cog('Delegate')
        self.general_speakers=defaultdict(list)
        self.register = defaultdict(dict)
        
    @commands.has_role('Committee')
    @commands.command()
    async def startSession(self, ctx):
        self.session[ctx.guild.id]=True
        if self.delegate is not None:
            self.delegate.session[ctx.guild.id]=True
            self.delegate.general_speakers[ctx.guild.id]=[]
        self.general_speakers[ctx.guild.id]=[]
        self.register[ctx.guild.id]={}
        await ctx.channel.send("Session has started!")
        
    @commands.has_role('Committee')
    @commands.command()
    async def endSession(self, ctx):
        self.session[ctx.guild.id]=False
        if self.delegate is not None:
            self.delegate.session[ctx.guild.id]=False
            self.delegate.general_speakers[ctx.guild.id]=[]
        self.general_speakers[ctx.guild.id]=[]
        await ctx.channel.send("Session has ended!")
        
    @commands.has_role('Committee')  
    @commands.command()
    async def GS(self, ctx):
        if self.session[ctx.guild.id]==True:
                
                await ctx.channel.send("General Speakers List: ")
                await ctx.channel.send(self.bot.get_cog('Delegate').general_speakers[ctx.guild.id])

    @commands.has_role('Committee')
    @commands.command(pass_context=True)
    async def speak(self,ctx, *,args):
        if self.session[ctx.guild.id]==True:
                args=args.split(' ')
                u=args[0]
                t=int(args[1])
                await ctx.send(u+" has the floor!")
                def check(message):
                    return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
                try:
                    m = await self.bot.wait_for("message", check=check, timeout=(t*60-10))
                    await ctx.send("Cancelled")
                except asyncio.TimeoutError:
                    await ctx.send("10 seconds left, "+u)
                    try:
                        m = await self.bot.wait_for("message", check=check, timeout=(10))
                        await ctx.send("Cancelled")
                    except asyncio.TimeoutError:
                        await ctx.send("Time is up, "+u+'!')
                
    @commands.has_role('Committee')
    @commands.command(pass_context=True)
    async def propose(self, ctx,*,args):
        if self.session[ctx.guild.id]==True:
                args=args.split(' ')
                type=args[0]
                if type=='mod':
                        total=args[1]
                        speaking=args[2]
                        country=args[3]
                        topic=' '.join(word for word in args[4:])
                        
                        m = await ctx.channel.send(country+" proposed a "+type+' caucus on '+topic+' for '+total+' mins with '+speaking+ ' seconds speakers time.')
                        await m.add_reaction("\U0001F44D")
                        await m.add_reaction("\U0001F44E")
                else:
                        total=args[1]
                        country=args[2]
                        m = await ctx.channel.send(country+" proposed a "+type+' caucus for '+total+' mins.')
                        await m.add_reaction("\U0001F44D")
                        await m.add_reaction("\U0001F44E")
    @commands.has_role('Committee')
    @commands.command(pass_context=True)
    async def mod(self,ctx, *,args):
        if self.session[ctx.guild.id]==True:
            args=args.split(' ')
            t=int(args[0])
            await ctx.send("The Mod has started!")
            def check(message):
                return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
            try:
                m = await self.bot.wait_for("message", check=check, timeout=t*60)
                await ctx.send("mod cancelled")
            except asyncio.TimeoutError:
                await ctx.send(f"Mod is over!")
                
    @commands.has_role('Committee')
    @commands.command(pass_context=True)
    async def unmod(self,ctx, *,args):
        if self.session[ctx.guild.id]==True:
            args=args.split(' ')
            t=int(args[0])
            await ctx.send("The UnMod has started!")
            def check(message):
                return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
            try:
                m = await self.bot.wait_for("message", check=check, timeout=t*60)
                await ctx.send("Unmod cancelled")
            except asyncio.TimeoutError:
                await ctx.send(f"UnMod is over!")
    @commands.has_role('Committee')
    @commands.command(pass_context=True)
    async def register(self,ctx,*,args):
        if self.session[ctx.guild.id]==True:
            args=args.split(' ')
            member=args[0].lower()
            status= args[1]
            dic=self.register[ctx.guild.id]
            dic[member]=status
            if status=='p':
                await ctx.send(member+" is present!")
            if status=='pv':
                await ctx.send(member+" is present and voting!")
            if status=='a':
                await ctx.send(member+" is absent!")
            elif status not in ['p','pv','a']:
                await ctx.send(member+"'s status was not understood!")

                
                
            
            
            

        
        
def setup(bot):
    bot.add_cog(Chair(bot))
