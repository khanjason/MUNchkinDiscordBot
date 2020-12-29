import discord
import time
import asyncio
import pymongo
from pymongo import MongoClient
from discord import FFmpegPCMAudio
from collections import defaultdict
from discord.ext import commands, tasks
from discord.utils import get
from youtube_dl import YoutubeDL, utils
import pymongo
import os
from pymongo import MongoClient
class Chair(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session={}
        self.mongo_url=os.getenv('CONNECTION_URL')
        self.cluster= MongoClient(self.mongo_url)
        self.db=self.cluster["Database1"]
        self.sessionTable=self.db["Session"]
        self.registerTable=self.db["Register"]
        self.delegate=self.bot.get_cog('Delegate')
        self.general_speakers={}
        self.player={}
        self.register = defaultdict(dict)
        
    @commands.has_role('Chair')
    @commands.command(brief='Starts a session.', description='Enables all commands for a session and invites bot to voice channel.')
    async def startSession(self, ctx):
        
        if self.sessionTable.find({"_id":ctx.guild.id}).count() > 0:
            #update
            self.sessionTable.find({"_id":ctx.guild.id})
            self.sessionTable.update_one({"_id":ctx.guild.id},{"$set":{"session":True}})
            
        else:
            #create
            sessionTag={"_id":ctx.guild.id,"session":True}
            self.sessionTable.insert_one(sessionTag)
        if self.registerTable.find({"_id":ctx.guild.id}).count() == 0:
            registerTag={"_id":ctx.guild.id,"register":{}}
            self.registerTable.insert_one(registerTag)
            
            
        
        t=[]
        self.general_speakers[ctx.guild.id]=t
        #self.register[ctx.guild.id]={}
        connected = ctx.author.voice
        if connected:
            voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
            if voice_client and voice_client.is_connected():
                embedVar = discord.Embed(title="Error", description="Bot is already in VC. Please disconnect bot from VC and try again.", color=discord.Color.from_rgb(78,134,219))
                await ctx.channel.send(embed=embedVar)
                
            else:
                await connected.channel.connect() 
                await ctx.channel.send("Session has started!")
        else:
            embedVar = discord.Embed(title="Error", description="Please join a voice channel.", color=discord.Color.from_rgb(78,134,219))
            await ctx.send(embed=embedVar)
    @startSession.error
    async def startSession_error(c,ctx, error):
        if isinstance(error, commands.MissingRole):
            embedVar = discord.Embed(title="Error", description="The 'Chair' role is required to run this command.", color=discord.Color.from_rgb(78,134,219))
            await ctx.send(embed=embedVar)
    @commands.has_role('Chair')
    @commands.command(brief='Ends the current Session.', description='Disables session commands and disconnects bot from voice channel.\n Clears GS list.')
    async def endSession(self, ctx):
        if self.sessionTable.find({"_id":ctx.guild.id}).count() > 0:
            #update
            self.sessionTable.find({"_id":ctx.guild.id})
            self.sessionTable.update_one({"_id":ctx.guild.id},{"$set":{"session":False}})
            self.registerTable.find({"_id":ctx.guild.id})
            self.registerTable.update_one({"_id":ctx.guild.id},{"$set":{"register":{}}})
        else:
            #create
            
            await ctx.channel.send("There is no session in progress.")
        
       
        
        connected = ctx.author.voice
        if connected:
            server=ctx.message.guild.voice_client
            await server.disconnect()
        
        await ctx.channel.send("Session has ended!")
    @commands.has_role('Chair')  
    @commands.command(brief='View the general speakers list.', description='Prints out the current general speakers list.')
    async def GS(self, ctx):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
                
                '''
                embedVar = discord.Embed(title="General Speakers List", description="General Speakers.", color=discord.Color.from_rgb(78,134,219))
                t=''
                if self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]==[]:
                    embedVar = discord.Embed(title="General Speakers List", description="This list is empty.", color=discord.Color.from_rgb(78,134,219))
                    await ctx.channel.send(embed=embedVar)
                else:
                    for country in self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]:
                        t=t+country+'\n'
                    embedVar.add_field(name="Countries:", value=t, inline=False)
            
                    await ctx.channel.send(embed=embedVar)'''
                    
    @commands.has_role('Chair')  
    @commands.command(brief='Removes first delegate from general speakers list.', description='Remove first delegate from general speakers list.\n Used just after a speaker has finished.')
    async def popGS(self, ctx):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
        
                if self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]==[]:
                    embedVar = discord.Embed(title="Error", description="List is empty.", color=discord.Color.from_rgb(78,134,219))
                    await ctx.channel.send(embed=embedVar)                    
                else:
                    t=self.bot.get_cog('Delegate').general_speakers[ctx.guild.id][0]
                    self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]=self.bot.get_cog('Delegate').general_speakers[ctx.guild.id][1:]
                    self.general_speakers[ctx.guild.id]=self.bot.get_cog('Delegate').general_speakers[ctx.guild.id]
                                    
                    await ctx.channel.send(str(t)+' was removed from the GS list.')
                


    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Yields the floor to a delegate.', description='Needs [delegate name] [time in seconds] and starts a timer.')
    async def speak(self,ctx, *,args):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
                args=args.split(' ')
                u=str(args[0])
                try:
                    t=int(args[1])
                except ValueError:
                            embedVar = discord.Embed(title="Error", description="Time must be a number.", color=discord.Color.from_rgb(78,134,219))
                            m= await ctx.channel.send(embed=embedVar)
                            return
                except IndexError:
                            embedVar = discord.Embed(title="Error", description="Not enough arguments. Please provide Delegate and Time.", color=discord.Color.from_rgb(78,134,219))
                            m= await ctx.channel.send(embed=embedVar)
                            return
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
                        await ctx.send("Time is up, "+u+'!')
                                        
    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Proposes a caucus.', description='requires [type].\n If type is mod, structure is !propose mod [total time in min] [speakers time in sec] [country proposed] [topic].\n If other type, requires [type] [total time in min] [country proposed].')
    async def propose(self, ctx,*,args):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
                args=args.split(' ')
                type=args[0]
                if type=='mod':
                        try:
                            total=int(args[1])
                            speaking=int(args[2])
                        except ValueError:
                            embedVar = discord.Embed(title="Error", description="Time must be a number.", color=discord.Color.from_rgb(78,134,219))
                            m= await ctx.channel.send(embed=embedVar)
                        country=args[3]
                        topic=' '.join(word for word in args[4:])
                        embedVar = discord.Embed(title="Proposal", description="A motion has been proposed.", color=discord.Color.from_rgb(78,134,219))
                        
                        embedVar.add_field(name="Proposed Caucus:", value=type, inline=False)
                        embedVar.add_field(name="Topic:", value=topic, inline=False)
                        embedVar.add_field(name="Country:", value=country, inline=False)
                        embedVar.add_field(name="Speaking Time (seconds):", value=int(speaking), inline=False)
                        embedVar.add_field(name="Total Time (minutes):", value=int(total), inline=False)
                        m= await ctx.channel.send(embed=embedVar)
                        await m.add_reaction("\U0001F44D")
                        await m.add_reaction("\U0001F44E")
                        await m.add_reaction('\N{CROSS MARK}')
                else:
                        try:
                            total=int(args[1])
                        except ValueError:
                            embedVar = discord.Embed(title="Error", description="Time must be a number.", color=discord.Color.from_rgb(78,134,219))
                            m= await ctx.channel.send(embed=embedVar)
                        country=args[2]
                        embedVar = discord.Embed(title="Proposal", description="A motion has been proposed.", color=discord.Color.from_rgb(78,134,219))
                        embedVar.add_field(name="Proposed Caucus:", value=type, inline=False)
                        embedVar.add_field(name="Country:", value=country, inline=False)
                        embedVar.add_field(name="Total Time (minutes):", value=int(total), inline=False)
                        m= await ctx.channel.send(embed=embedVar)
                        await m.add_reaction("\U0001F44D")
                        await m.add_reaction("\U0001F44E")
                        await m.add_reaction('\N{CROSS MARK}')
    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Starts a moderated caucus.', description='Requires !mod [total time in min].\n Starts a timer.')
    async def mod(self,ctx, *,args):
        url='https://www.youtube.com/watch?v=SK3g6f5jsRA'
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
            args=args.split(' ')
            try:
                t=int(args[0])
            except ValueError:
                            embedVar = discord.Embed(title="Error", description="Time must be a number.", color=discord.Color.from_rgb(78,134,219))
                            m= await ctx.channel.send(embed=embedVar)
                            return
            await ctx.send("The Mod has started!")
            def check(message):
                return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
            try:
                m = await self.bot.wait_for("message", check=check, timeout=t*60)
                await ctx.send("mod cancelled")
            except asyncio.TimeoutError:
                await ctx.send(f"Mod is over!")
                
                voice_client=ctx.guild.voice_client
                YDL_OPTIONS = {
        'format': 'bestaudio',
        "force-ipv4":True,
        'dump-pages':True,
        'source_address':'0.0.0.0',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            
        }],
        'outtmpl': 'song.%(ext)s',
    }
                try:
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        ydl.download([url])
                    voice_client.play(FFmpegPCMAudio("song.mp3"))
                    voice_client.is_playing()
                except  utils.DownloadError:
                    embedVar = discord.Embed(title="Error", description="YoutubeDL failed to download Gavel Sound Effect.", color=discord.Color.from_rgb(78,134,219))
                    m= await ctx.channel.send(embed=embedVar)
                
                
                
    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Starts a unmoderated caucus.', description='Requires !unmod [total time in min].\n Starts a timer.')
    async def unmod(self,ctx, *,args):
        url='https://www.youtube.com/watch?v=SK3g6f5jsRA'
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
            args=args.split(' ')
            try:
                t=int(args[0])
            except ValueError:
                            embedVar = discord.Embed(title="Error", description="Time must be a number.", color=discord.Color.from_rgb(78,134,219))
                            m= await ctx.channel.send(embed=embedVar)
                            return
            await ctx.send("The UnMod has started!")
            def check(message):
                return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
            try:
                m = await self.bot.wait_for("message", check=check, timeout=t*60)
                await ctx.send("Unmod cancelled")
            except asyncio.TimeoutError:
                await ctx.send(f"UnMod is over!")
                voice_client=ctx.guild.voice_client
                YDL_OPTIONS = {
        'format': 'bestaudio',
        "force-ipv4":True,
        'dump-pages':True,
        'source_address':'0.0.0.0',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            
        }],
        'outtmpl': 'song.%(ext)s',
    }
                try:
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        ydl.download([url])
                    voice_client.play(FFmpegPCMAudio("song.mp3"))
                    voice_client.is_playing()

                except  utils.DownloadError:
                    embedVar = discord.Embed(title="Error", description="YoutubeDL failed to download Gavel Sound Effect.", color=discord.Color.from_rgb(78,134,219))
                    m= await ctx.channel.send(embed=embedVar)
    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Register a delegate.', description='Requires !register [delegate name] [status].\n Status can be present (p),present and voting(pv) or absent (a)')
    async def register(self,ctx,*,args):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
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
                embedVar = discord.Embed(title="Error", description="Not a valid registration status. Use p, pv or a.", color=discord.Color.from_rgb(78,134,219))
                m= await ctx.channel.send(embed=embedVar)
    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='View the register.', description='Displays all registered delegations and their statuses.')
    async def viewRegister(self,ctx):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
            dic=self.register[ctx.guild.id]
            embedVar = discord.Embed(title="Register", description="All registered delegates.", color=discord.Color.from_rgb(78,134,219))
            for k,v in dic.items():
                t=''
                if v=='p':
                    t='Present'
                if v=='pv':
                    t='Present and Voting'
                if v=='a':
                    t='Absent'
                embedVar.add_field(name=k, value=t, inline=False)

            await ctx.channel.send(embed=embedVar)
            
            
            
    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Start a vote.', description='Starts a non-caucus vote. Useful for final vote or amendments.\n Requires !voting [topic]')
    async def voting(self, ctx,*,args):
        sesstag = self.sessionTable.find_one({"_id":ctx.guild.id})
        sess=sesstag.get("session")
        if sess==True:
                args=args.split(' ')
                topic=' '.join(word for word in args)
                embedVar = discord.Embed(title="Voting", description="A vote is in progress.", color=discord.Color.from_rgb(78,134,219))
                embedVar.add_field(name="Topic:", value=topic, inline=False)

                m= await ctx.channel.send(embed=embedVar)
                await m.add_reaction("\U0001F44D")
                await m.add_reaction("\U0001F44E")
                await m.add_reaction('\N{CROSS MARK}')
                
                

    @commands.has_role('Chair')
    @commands.command(pass_context=True,brief='Give Chair role.', description='Gives chair role to another member.\n Requires !chair [@member]')
    async def chair(self, ctx,user: discord.Member):
        
        member = user
        role = get(ctx.message.guild.roles, name="Chair")
        await member.add_roles(role)
        embedVar = discord.Embed(title="Chair Role", description="Role was given to "+str(member), color=discord.Color.from_rgb(78,134,219))
    

        m= await ctx.channel.send(embed=embedVar)
        
            
            

    
        
def setup(bot):
    bot.add_cog(Chair(bot))
