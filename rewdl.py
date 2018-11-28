import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from bs4 import BeautifulSoup
import aiohttp
import re
from datetime import timedelta
import traceback
import os
from random import choice, randint
import asyncio
import platform
import colorsys
import random
import os
import time
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType

client = Bot("?")

@client.event
async def on_ready():
    print("Logged in as")
    print("Username: %s"%client.user.name)
    print("ID: %s"%client.user.id)
    print("----------")
    await client.change_presence(game=discord.Game(name='with your mom | ?help'))

client.remove_command('help')

@client.command(pass_context = True)
async def help(ctx, *, member : discord.Member  = None):
    embed = discord.Embed(title="Rewdl", description="Best BOT for your server, use it with this magical commands:", color=0xea7938)
 
    embed.add_field(name="?help", value="This command...", inline=False)
    embed.add_field(name="?invite", value="You can invite this BOT to your server!", inline=False)
    embed.add_field(name="?serverinfo", value="Informations about this server..", inline=False)
    embed.add_field(name="?userinfo", value="Informations about you or another user..", inline=False)
    embed.add_field(name="?ban", value="Ban user on your server!", inline=False)
    embed.add_field(name="?kick", value="Kick user on your server!", inline=False)
    embed.add_field(name="?mute", value="Mute user with this command!", inline=False)     
    embed.add_field(name="?unmute", value="You can unmute user with this magical command!", inline=False)
    embed.add_field(name="?warn", value="Warn user on your server!", inline=False)
    embed.add_field(name="?say", value="BOT can say your words, but you need write it!", inline=False)
    embed.add_field(name="?clear", value="Clear messages on your server", inline=False)
    embed.add_field(name="?ping", value="Did you want know your ping?", inline=False)
    embed.add_field(name="?avatar", value="Do you want see your avatar?", inline=False)
    embed.add_field(name="?face", value="Some faces from magical pages.", inline=False)
    embed.add_field(name="?meme", value="Some meme for you!", inline=False)
    embed.add_field(name="?creators", value="Do you want know who made this BOT?", inline=False)
    embed.add_field(name="?shit", value="Something wrong... 15+ pls", inline=False)
 
    await client.say(embed = embed)

@client.command(pass_context = True)
async def invite(ctx, *, member : discord.Member  = None):
    embed = discord.Embed(title="Invite", description="Invite this best BOT on your server =D", color=0xea7938)
 
    embed.add_field(name="Here is the link:", value=" https://discordapp.com/api/oauth2/authorize?client_id=509080817000251402&permissions=8&scope=bot", inline=False)
    
    await client.say(embed = embed)

@client.command(pass_context = True)
async def serverinfo(ctx):

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50:
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);
 
@client.command(pass_context = True) 
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title=" {} informations".format(user.name), description="Do you know it?", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)    
    await client.say(embed=embed)
      
@client.command(pass_context = True)
async def ban(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
        await client.ban(member)
        embed=discord.Embed(title="User banned!", description="**{0}** was banned by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed = embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6 )
        await client.say(embed=embed)   
                  	
@client.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    author = ctx.message.author
    if author.server_permissions.kick_members:
        await client.kick(user)
        await client.say("{} was kicked!".format(user.name))
    else:
        await client.say("Missing permissions.")           
                                      
@client.command(pass_context = True)
async def mute(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.add_roles(member, role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)                                                                                                          
        
@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.remove_roles(member, role)
        embed=discord.Embed(title="User Unmuted!", description="**{0}** was unmuted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await client.say(embed=embed)                                                                                                            
@client.command(pass_context = True)
async def warn(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
        embed=discord.Embed(title="User was warned!", description="**{0}** was warned by Administrator **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await client.say(embed=embed)
     else:
        embed=discord.Embed(title="Error", description="Missing permissions for this action..", color=0xff00f6)
        await client.say(embed=embed)                                                                                                                                                                                                                                                                                                                   
@client.command(pass_context = True)
async def say(ctx, *args):
    mesg = ' '.join(args)
    await client.delete_message(ctx.message)
    return await client.say(mesg) 
                            
@client.command(pass_context=True)
async def ping(ctx):
    t = await client.say('Pong!')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(t, new_content=':ping_pong: **Pong! Actual ping: {}ms**'.format(int(ms)))
        
@client.command(pass_context = True)
async def clear(ctx, number):
    mgs = []
    number = int(number) 
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)

@client.command()
async def meme():    
   import random
   
   choices = ["https://imgur.com/a/12e8A1L", "https://imgur.com/a/gTL4Edp", "https://imgur.com/a/jkf80vH", "https://imgur.com/a/4B1WEo0"]
                                       

   await client.say(random.choice(choices))

@client.command(pass_context = True)
async def avatar(ctx, member: discord.Member):
    await client.reply("{}".format(member.avatar_url))
          
@client.command()
async def shit():
	import random
	
	choices = ["ur mom gay", "ur dad lesbian", "ur sister mom gay", "ur pewdiepie dick", "bitch lasagna", "stfu", "nothing personal kid... suck my dick", "bobs or vEgAnA", "i dont like you", "T-Series was left the game...", "PewDiePie joined the game..."]
	
@client.command()
async def face():
	import random
	
	choices =["( ͡° ͜ʖ ͡°)","(⌐■_■)","¯\_(ツ)_/¯","ಠ_ಠ","ʢ◉ᴥ◉ʡ","(づ◔ ͜ʖ◔)づ","⤜(ʘ_ʘ)⤏","☞   ͜ʖ  ☞","ლ(⪧ロ⪦ლ)","ლ(⌐■ロ■ლ)","ᖗᵔωᵔᖘ","(´•  ͜ʖ •`)"]
	
	await client.say(random.choice(choices))
	
@client.command(pass_context = True)
async def creators(ctx, *, member : discord.Member  = None):
    embed = discord.Embed(title="Creators and Developers", description="Who is owner? Who is Developer? I dont know.. Now you can know it!", color=0xea7938)
 
    embed.add_field(name="Owner", value="@Terpix_#0327", inline=False)
    embed.add_field(name="Developer", value="rediikKK - You can found him on TeamSpeak3", inline=False)
    embed.add_field(name="Support", value="Nobody.. Contact Terpix_ for this rank!", inline=False)
    embed.add_field(name="Support with Script and Function", value="@lepax_#2196")
    
    await client.say(embed = embed)                     
client.run("NTA5MDgwODE3MDAwMjUxNDAy.DtnN3A.fYAvZfe14CA2NaMvp3iG2Mig1OU")
