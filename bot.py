import discord
import time
import os


from discord.ext import commands,tasks


DISCORD_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

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
        

@bot.command(pass_content=True)
async def help(ctx):
    embedVar= discord.Embed(title="MUNchkin Help", description="List of commands for MUNchkin.", color=discord.Color.from_rgb(78,134,219))
    embedVar.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/2/2f/Flag_of_the_United_Nations.svg")
    embedVar.add_field(name="Chair Commands", value="These commands can only be used by the Chair role.", inline=False)
    embedVar.add_field(name="!startSession", value="Enables all commands for a session and invites bot to voice channel.", inline=True)
    embedVar.add_field(name="!register [delegate name] [status]", value="Status can be present (p),present and voting(pv) or absent (a)", inline=True)
    embedVar.add_field(name="!viewRegister", value="Displays all registered delegations and their statuses.", inline=True)
    embedVar.add_field(name="!GS", value="Prints out the current general speakers list.", inline=True)
    embedVar.add_field(name="!popGS", value="Remove first delegate from general speakers list. Used just after a speaker has finished.", inline=True)
    embedVar.add_field(name="!speak [delegate name] [time in seconds]", value="Yields the floor to the delegate. Starts a timer.", inline=True)
    embedVar.add_field(name="!propose mod [total time in min] [speakers time in sec] [country proposed] [topic]", value="Propose a moderated caucus.", inline=True)
    await ctx.channel.send(embed=embedVar)


    
bot.run(DISCORD_TOKEN)
