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
        
    @commands.command()
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

    @commands.command()
    async def preamble(self,ctx):
        if (self.session)[ctx.guild.id]==True:
            preambs=["Acknowledging", 'Affirming', 'Alarmed', 'Anxious', 'Approving', 'Aware','Bearing in mind', 'Believing', 'Concerned', 'Confident', 'Conscious', 'Considering', 'Convinced', 'Disturbed', 'Determined', 'Emphasizing', 'Encouraged', 'Endorsing', 'Expressing', 'Guided by', 'Having ...adopted', '...approved', '...considered', '...examined further', '...received', '...reviewed', 'Keeping in mind', 'Mindful', 'Noting',
'...with approval', '...with concern', '...with deep concern', '...with grave concern', '...with regret', '...with satisfaction', 'Observing', 'Reaffirming', 'Realizing', 'Recalling', 'Recognising', 'Regretting', 'Reiterating', 'Seeking', 'Stressing', 'Welcoming']
            
            
            await ctx.channel.send('```Preambulatory phrases: '+preambs+'```')
        
def setup(bot):
    bot.add_cog(Delegate(bot))
