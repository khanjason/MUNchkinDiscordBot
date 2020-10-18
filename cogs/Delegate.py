import discord
import time
import asyncio
from discord.ext import commands, tasks

class Delegate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chair=self.bot.get_cog('Chair')
        if self.chair is not None:
            self.session=self.chair.session
            self.general_speakers=self.chair.general_speakers
        else:
            self.session={}
            self.general_speakers={}
        
    @commands.command()
    async def addGS(self,ctx):
        if self.chair is not None:
            if (self.chair.session)[ctx.guild.id]==True:
                    (self.general_speakers[ctx.guild.id]).append(str(ctx.author.nick))
                    await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')
        else:
            
            if (self.session)[ctx.guild.id]==True:
                    self.general_speakers[ctx.guild.id].append(str(ctx.author.nick))
                    await ctx.channel.send(ctx.author.mention+' has been added to the General Speakers List!')

    
        
        
def setup(bot):
    bot.add_cog(Delegate(bot))
