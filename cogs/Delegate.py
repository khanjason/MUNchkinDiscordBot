import discord
import time
import asyncio
from discord.ext import commands, tasks
from collections import defaultdict

class Delegate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chair=self.bot.get_cog('Chair')
        if self.chair is not None:
            self.session=self.chair.session
            self.general_speakers=self.chair.general_speakers
        else:
            self.session={}
            self.general_speakers=defaultdict(list)
        
    @commands.command(brief='Add yourself to GS list.', description='Adds your name to the general speakers list.')
    async def addGS(self,ctx):
        if self.chair is not None:
            if (self.chair.session)[ctx.guild.id]==True:
                    tmp=self.general_speakers[ctx.guild.id]
                    if ctx.author.nick!=None:
                        tmp.append(str(ctx.author.nick))
                    else:
                        tmp.append(str(ctx.author))
                    self.general_speakers[ctx.guild.id]=tmp
                    await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')
        else:
            
            if (self.session)[ctx.guild.id]==True:
                    tmp=self.general_speakers[ctx.guild.id]
                    if ctx.author.nick!=None:
                        tmp.append(str(ctx.author.nick))
                    else:
                        tmp.append(str(ctx.author))
                    
                    self.general_speakers[ctx.guild.id]=tmp
                    await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')

    @commands.command(brief='Lists preamble phrases.', description='Displays list of phrases, useful for preambulatory clauses.')
    async def preamble(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            preambs=["Acknowledging", 'Affirming', 'Alarmed', 'Anxious', 'Approving', 'Aware','Bearing in mind', 'Believing', 'Concerned', 'Confident', 'Conscious', 'Considering', 'Convinced', 'Disturbed', 'Determined', 'Emphasizing', 'Encouraged', 'Endorsing', 'Expressing', 'Guided by', 'Having ...adopted', '...approved', '...considered', '...examined further', '...received', '...reviewed', 'Keeping in mind', 'Mindful', 'Noting',
'...with approval', '...with concern', '...with deep concern', '...with grave concern', '...with regret', '...with satisfaction', 'Observing', 'Reaffirming', 'Realizing', 'Recalling', 'Recognising', 'Regretting', 'Reiterating', 'Seeking', 'Stressing', 'Welcoming']
            
            embedVar = discord.Embed(title="Preamble Phrases:", description="List of preambulatory phrases.", color=discord.Color.from_rgb(78,134,219))
            t=''
            for p in preambs:
                t=t+p+'\n'
            embedVar.add_field(name="Phrases:", value=t, inline=False)
            
            await ctx.channel.send(embed=embedVar)
    @commands.command(brief='Lists operative phrases.', description='Displays list of phrases, useful for operative clauses.')
    async def operative(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            operatives=["Accepts", 'Adopts', 'Affirms', 'Appeals', 'Appreciates', 'Approves', 'Authorises', 'Calls upon', 'Calls for', 'Concurs', 'Confirms', 'Congratulates', 'Considers', 'Declares', 'Deplores', 'Designates', 'Directs', 'Emphasizes', 'Encourages', 'Endorses', 'Expresses', 'Instructs', 'Invites', 'Proclaims', 'Reaffirms', '...its belief', 'Recognises', 'Recommends', 'Regrets', 'Repeats', 'Requests', 'Suggests', 'Supports', 'Takes note of', 'Transmits', 'Urges', 'Welcomes']
            embedVar = discord.Embed(title="Operative Phrases:", description="List of operative phrases.", color=discord.Color.from_rgb(78,134,219))
            t=''
            for o in operatives:
                t=t+o+'\n'
            embedVar.add_field(name="Phrases:", value=t, inline=False)
            
            await ctx.channel.send(embed=embedVar)
            
            
    @commands.command(brief='Tap in support.', description='Alerts that you support the current debate.')
    async def tap(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            if ctx.author.nick!=None:
                country=str(ctx.author.nick)
            else:
                country=str(ctx.author)
            embedVar = discord.Embed(title="Tap Tap!", description=country+" concurs!", color=discord.Color.from_rgb(78,134,219))
                        
            
            m= await ctx.channel.send(embed=embedVar)
    @commands.command(brief='Information about MUNchkin', description='Outputs information about MUNchkin bot.')
    async def about(self,ctx):
        
        embedVar = discord.Embed(title="About", description="MUNchkin Discord Bot", color=discord.Color.from_rgb(78,134,219))
        embedVar.add_field(name="Description", value="A discord bot for managing Model United Nations sessions (Harvard style).", inline=False)
        embedVar.add_field(name="Version", value="v1.0.0", inline=False)
        embedVar.add_field(name="Source Code", value="https://github.com/khanjason/MUNchkinDiscordBot", inline=False)
            
        m= await ctx.channel.send(embed=embedVar)
    
    @commands.command(brief='Brief rules of procedure.', description='Provides Harvard style MUN rules of procedure, summarised.')
    async def rules(self,ctx):
        embedVar = discord.Embed(title="Rules of Procedure", description="Harvard MUN ruleset.", color=discord.Color.from_rgb(78,134,219))
        embedVar.add_field(name="Debating", value="Debates contain three types of caucuses; general speaking, moderated, unmoderated.", inline=False)        
        embedVar.add_field(name="General Speaking", value="Delegates request to be added to a list of general speakers, which the chair will proceed through. Delegates give an overview of their opinion on the debate. This happens at the beginning of a session or when there are no motions to entertain.", inline=False)
        embedVar.add_field(name="Moderated Caucus", value="Moderated caucuses are timed with a maximum allowed speaking time and set topic. The chair chooses who gets to speak at each time.", inline=False)
        embedVar.add_field(name="Unmoderated Caucus", value="Unmoderated caucuses are not chaired and are used for open talk among delegates and writing resolutions.", inline=False)
        embedVar.add_field(name="Resolutions", value="Resolutions are made up of preambulatory and operative clauses, describing desired actions to be taken. Resolutions can be introduced and debated, and voted on to finalise a debate.", inline=False)
        m= await ctx.channel.send(embed=embedVar)
def setup(bot):
    bot.add_cog(Delegate(bot))
