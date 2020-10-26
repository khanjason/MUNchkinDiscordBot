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
                    tmp.append(str(ctx.author.nick))
                    self.general_speakers[ctx.guild.id]=tmp
                    await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')
        else:
            
            if (self.session)[ctx.guild.id]==True:
                    tmp=self.general_speakers[ctx.guild.id]
                    tmp.append(str(ctx.author.nick))
                    self.general_speakers[ctx.guild.id]=tmp
                    await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')

    @commands.command(brief='Lists preamble phrases.', description='Displays list of phrases, useful for preambulatory clauses.')
    async def preamble(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            preambs=["Acknowledging", 'Affirming', 'Alarmed', 'Anxious', 'Approving', 'Aware','Bearing in mind', 'Believing', 'Concerned', 'Confident', 'Conscious', 'Considering', 'Convinced', 'Disturbed', 'Determined', 'Emphasizing', 'Encouraged', 'Endorsing', 'Expressing', 'Guided by', 'Having ...adopted', '...approved', '...considered', '...examined further', '...received', '...reviewed', 'Keeping in mind', 'Mindful', 'Noting',
'...with approval', '...with concern', '...with deep concern', '...with grave concern', '...with regret', '...with satisfaction', 'Observing', 'Reaffirming', 'Realizing', 'Recalling', 'Recognising', 'Regretting', 'Reiterating', 'Seeking', 'Stressing', 'Welcoming']
            
            
            await ctx.channel.send('```Preambulatory phrases: '+str(preambs)+'```')
    @commands.command(brief='Lists operative phrases.', description='Displays list of phrases, useful for operative clauses.')
    async def operative(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            operatives=["Accepts", 'Adopts', 'Affirms', 'Appeals', 'Appreciates', 'Approves', 'Authorises', 'Calls upon', 'Calls for', 'Concurs', 'Confirms', 'Congratulates', 'Considers', 'Declares', 'Deplores', 'Designates', 'Directs', 'Emphasizes', 'Encourages', 'Endorses', 'Expresses', 'Instructs', 'Invites', 'Proclaims', 'Reaffirms', '...its belief', 'Recognises', 'Recommends', 'Regrets', 'Repeats', 'Requests', 'Suggests', 'Supports', 'Takes note of', 'Transmits', 'Urges', 'Welcomes']

            
            await ctx.channel.send('```operative phrases: '+str(operatives)+'```')
    @commands.command(brief='Tap in support.', description='Alerts that you support the current debate.')
    async def tap(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            country=str(ctx.author.nick)
            embedVar = discord.Embed(title="Tap Tap!", description=country+" concurs!", color=discord.Color.from_rgb(78,134,219))
                        
            
            m= await ctx.channel.send(embed=embedVar)

        
def setup(bot):
    bot.add_cog(Delegate(bot))
