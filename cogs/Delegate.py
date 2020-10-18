import discord
import time
import asyncio
from discord.ext import commands, tasks

class Delegate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chair=self.bot.get_cog('Chair')
        if chair is not None:
            self.session=chair.session
            self.general_speakers=chair.general_speakers
        else:
            self.session=False
            self.general_speakers=[]
        
    @commands.command()
    async def addGS(self,ctx):
        if self.chair.session==True:
                self.general_speakers.append(str(ctx.author.nick))
                await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')



    
        
        
def setup(bot):
    bot.add_cog(Delegate(bot))
