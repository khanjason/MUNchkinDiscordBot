import discord
import time
import os


from discord.ext import commands,tasks


DISCORD_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the United Nations"))


@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')
    
    
@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        
    

bot.run(DISCORD_TOKEN)
