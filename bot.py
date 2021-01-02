import discord
import time
import os
import pymongo
from pymongo import MongoClient

from discord.ext import commands,tasks

from discord.ext.commands import CommandNotFound


DISCORD_TOKEN = os.getenv('BOT_TOKEN')
CONNECTION_URL= os.getenv('CONNECTION_URL')
cluster= MongoClient(CONNECTION_URL)
db=cluster["Database1"]
prefixTable=db["Prefix"]

async def getPrefix(bot,message):
    if isinstance(message.channel, discord.channel.DMChannel):
            pref='!'
            return pref
    if prefixTable.find({"_id":message.guild.id}).count() > 0:
        preftag=prefixTable.find_one({"_id":message.guild.id})
        pref=preftag.get("prefix")
    else:
        pref='!'
    return pref

bot = commands.Bot(command_prefix=getPrefix)
bot.remove_command('help')

@bot.command()
async def prefix(ctx,*,args):
    if isinstance(ctx.channel, discord.channel.DMChannel):
            embedVar = discord.Embed(title="Error", description="Not in a server.", color=discord.Color.from_rgb(78,134,219))

            await ctx.send(embed=embedVar)
    else:
        args=args.split(' ')
        p=args[0]
        if prefixTable.find({"_id":ctx.guild.id}).count() > 0:
            prefixTable.update_one({"_id":ctx.guild.id},{"$set":{"prefix":p}})
        else:
            prefTag={"_id":ctx.guild.id,"prefix":p}
            prefixTable.insert_one(prefTag)        

        embedVar= discord.Embed(title="Prefix", description="Prefix has been changed to "+p, color=discord.Color.from_rgb(78,134,219))
        await ctx.channel.send(embed=embedVar)    


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
    print(getPrefix(ctx))
    p=command_prefix
    print(p)
    embedVar= discord.Embed(title="MUNchkin Help", description="List of commands for MUNchkin.", color=discord.Color.from_rgb(78,134,219))
    embedVar.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/UN_flag.png/1024px-UN_flag.png")
    embedVar.add_field(name="Chair Commands", value="These commands can only be used by the Chair role.", inline=False)
    embedVar.add_field(name="!startSession", value="Enables all commands for a session and invites bot to voice channel.", inline=True)
    embedVar.add_field(name="!register [delegate] [status]", value="Status can be present (p),present and voting(pv) or absent (a)", inline=True)
    embedVar.add_field(name="!viewRegister", value="Displays all registered delegations and their statuses.", inline=True)
    embedVar.add_field(name="!GS", value="Prints out the current general speakers list.", inline=True)
    embedVar.add_field(name="!popGS", value="Remove first delegate from general speakers list. Used just after a speaker has finished.", inline=True)
    embedVar.add_field(name="!speak [delegate] [time (s)]", value="Yields the floor to the delegate. Starts a timer.", inline=True)
    embedVar.add_field(name="!propose mod [total time(min)] [speaker time(s)] [country] [topic]", value="Propose a moderated caucus.", inline=True)
    embedVar.add_field(name="!mod [total time(min)]", value="Starts a timer for Mod. Sending the word 'cancel' will cancel it.", inline=True)
    embedVar.add_field(name="!unmod [total time(min)]", value="Starts a timer for Unmod. Sending the word 'cancel' will cancel it.", inline=True)
    embedVar.add_field(name="!voting [topic]", value="Starts a non-caucus vote. Useful for final vote or amendments.", inline=True)
    embedVar.add_field(name="!endSession", value="Disables session commands and disconnects bot from voice channel. Clears GS list.", inline=True)
    embedVar.add_field(name="!chair [@member]", value="Gives chair role to another member.", inline=True)
    embedVar.add_field(name="Delegate Commands", value="These commands can be used by anyone.", inline=False)
    embedVar.add_field(name="!addGS", value="Adds your name to the general speakers list.", inline=True)
    embedVar.add_field(name="!tap", value="Alerts that you support the current debate.", inline=True)
    embedVar.add_field(name="!preamble", value="Displays list of phrases, useful for preambulatory clauses.", inline=True)
    embedVar.add_field(name="!operative", value="Displays list of phrases, useful for operative clauses.", inline=True)
    embedVar.add_field(name="!about", value="Provides information about MUNchkin.", inline=True)
    embedVar.add_field(name="!rules", value="Provides simplified ruleset for Harvard style MUN.", inline=True)
    embedVar.add_field(name="Support MUNchkin", value="Useful links for using MUNchkin.", inline=False)
    embedVar.add_field(name="Invite", value="[Add me!](https://discord.com/oauth2/authorize?client_id=767330479757197323&permissions=0&scope=bot)", inline=True)
    embedVar.add_field(name="Support Server", value='[Join!](https://discord.gg/94ShKfuqrk)', inline=True)
    embedVar.add_field(name="Vote", value='[Rate me!](https://top.gg/bot/767330479757197323/vote)', inline=True)
    embedVar.add_field(name="Source Code", value='[View!](https://github.com/khanjason/MUNchkinDiscordBot)', inline=True)
    await ctx.channel.send(embed=embedVar)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embedVar= discord.Embed(title="Error", description="Invalid command. Please change prefix with command 'prefix' to avoid clashing.", color=discord.Color.from_rgb(78,134,219))
        await ctx.channel.send(embed=embedVar)
    return
    
bot.run(DISCORD_TOKEN)
