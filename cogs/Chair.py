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
        self.general_speakers={}
        self.register = defaultdict(dict)
        
    @commands.has_role('Chair')
    @commands.command()
    async def startSession(self, ctx):
        self.session[ctx.guild.id]=True
        if self.delegate is not None:
            self.delegate.session[ctx.guild.id]=True
            self.delegate.general_speakers[ctx.guild.id]=[]
        else:
            t=[]
            self.general_speakers[ctx.guild.id]=t
        self.register[ctx.guild.id]={}
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect() 
        await ctx.channel.send("Session has started!")
        
    @commands.has_role('Chair')
    @commands.command()
    async def endSession(self, ctx):
        self.session[ctx.guild.id]=False
        if self.delegate is not None:
            self.delegate.session[ctx.guild.id]=False
            self.delegate.general_speakers[ctx.guild.id]=[]
        
        connected = ctx.author.voice
        if connected:
            server=ctx.message.guild.voice_client
            await server.disconnect()
        await ctx.channel.send("Session has ended!")
        
    @commands.has_role('Chair')  
    @commands.command()
    async def GS(self, ctx):
        if self.session[ctx.guild.id]==True:
                embedVar = discord.Embed(title="General Speakers List", description="General Speakers.", color=discord.Color.from_rgb(78,134,219))
                for country in self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]:
                    embedVar.add_field(name="Country:", value=country, inline=False)
        
                await ctx.channel.send(embed=embedVar)
                
    @commands.has_role('Chair')  
    @commands.command()
    async def popGS(self, ctx):
        if self.session[ctx.guild.id]==True:
                t=self.bot.get_cog('Delegate').general_speakers[ctx.guild.id][0]
                self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]=self.bot.get_cog('Delegate').general_speakers[ctx.guild.id][1:]
                self.general_speakers[ctx.guild.id]=self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]
                                
                await ctx.channel.send(str(t)+' was removed from the GS list.')
                


    @commands.has_role('Chair')
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
                    m = await self.bot.wait_for("message", check=check, timeout=(t-10))
                    await ctx.send("Cancelled")
                except asyncio.TimeoutError:
                    await ctx.send("10 seconds left, "+u)
                    try:
                        m = await self.bot.wait_for("message", check=check, timeout=(10))
                        await ctx.send("Cancelled")
                    except asyncio.TimeoutError:
                        voice_channel = ctx.voice_client
                        
                        
                        voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./../sounds/gavel.wav')))
           
                        await ctx.send("Time is up, "+u+'!')
                
    @commands.has_role('Chair')
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
                        embedVar = discord.Embed(title="Proposal", description="A motion has been proposed.", color=discord.Color.from_rgb(78,134,219))
                        
                        embedVar.add_field(name="Proposed Caucus:", value=type, inline=False)
                        embedVar.add_field(name="Topic:", value=topic, inline=False)
                        embedVar.add_field(name="Country:", value=country, inline=False)
                        embedVar.add_field(name="Speaking Time (seconds):", value=speaking, inline=False)
                        embedVar.add_field(name="Total Time (minutes):", value=total, inline=False)
                        m= await ctx.channel.send(embed=embedVar)
                        await m.add_reaction("\U0001F44D")
                        await m.add_reaction("\U0001F44E")
                else:
                        total=args[1]
                        country=args[2]
                        embedVar = discord.Embed(title="Proposal", description="A motion has been proposed.", color=discord.Color.from_rgb(78,134,219))
                        embedVar.add_field(name="Proposed Caucus:", value=type, inline=False)
                        embedVar.add_field(name="Country:", value=country, inline=False)
                        embedVar.add_field(name="Total Time (minutes):", value=total, inline=False)
                        m= await ctx.channel.send(embed=embedVar)
                        await m.add_reaction("\U0001F44D")
                        await m.add_reaction("\U0001F44E")
    @commands.has_role('Chair')
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
                voice_channel = ctx.voice_client   
                voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./../sounds/gavel.wav')))
                await ctx.send(f"Mod is over!")
                
    @commands.has_role('Chair')
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
                voice_channel = ctx.voice_client   
                voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('./../sounds/gavel.wav')))
                await ctx.send(f"UnMod is over!")
    @commands.has_role('Chair')
    @commands.command(pass_context=True)
    async def register(self,ctx,*,args):
        if self.session[ctx.guild.id]==True:
            args=args.split(' ')
            member=args[0].lower()
            status= args[1]
            dic=self.register[ctx.guild.id]
            dic[member]=status
            if status=='p':
                await ctx.send(member.title()+" is present!")
            if status=='pv':
                await ctx.send(member.title()+" is present and voting!")
            if status=='a':
                await ctx.send(member.title()+" is absent!")
            elif status not in ['p','pv','a']:
                await ctx.send(member+"'s status was not understood!")
    @commands.has_role('Chair')
    @commands.command(pass_context=True)
    async def viewRegister(self,ctx):
        if self.session[ctx.guild.id]==True:
            dic=self.register[ctx.guild.id]
            await ctx.send("Register: "+str(dic))
            
    @commands.has_role('Chair')
    @commands.command(pass_context=True)
    async def voting(self, ctx,*,args):
        if self.session[ctx.guild.id]==True:
                args=args.split(' ')
                topic=' '.join(word for word in args)
                embedVar = discord.Embed(title="Voting", description="A vote is in progress.", color=discord.Color.from_rgb(78,134,219))
                embedVar.add_field(name="Topic:", value=topic, inline=False)

                m= await ctx.channel.send(embed=embedVar)
                await m.add_reaction("\U0001F44D")
                await m.add_reaction("\U0001F44E")
                

                
                
            
            
            

        
        
def setup(bot):
    bot.add_cog(Chair(bot))
