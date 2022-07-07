import os
import asyncio
from pathlib import Path
import json
from math import radians
import random
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext.commands import MissingPermissions, has_permissions
import platform
import sys
import traceback
import re

import cogs._json


certification_database = cogs._json.read_json("certifications")
admins_base = cogs._json.read_json("admins")
crftSvOwners = cogs._json.read_json("certified_Owners")
crftSvMods = cogs._json.read_json("serverMods")
blacklist_database = cogs._json.read_json("blacklists")
blacklist_log_channels = cogs._json.read_json("blacklist_channels")

print("\n---------\n")

intents = discord.Intents.all()
client = discord.Client(intents=intents,owner_id=655443924948877323)
slash = SlashCommand(client, sync_commands=True)

# Lists

guild_ids = []

client.owner = 655443924948877323
client.version = 1.2
client.discordinvite = "https://discord.gg/G3u2q3bcMm"
client.sellixlink = "Comming Soon"
client.btcaddress = "bc1q9cmamygcwf8gd90zl0lml8l9sscl5l7l3ttl3v"
client.xmraddress = "42UfSQagZL4c8XFfSBqvqSj17XVvi3bjp6WatMsLW34HhX9pQJLKH4m73E3L8UBugmfxmqCyYk7QfaQ42xN4cvgi5AkMmgD"
client.ltcaddress = "ltc1qfxp8ntjlhjpnc4j0mjn80wa44fa45txdyvev80"

certificate_commands = """```/certificate
/getstarted
/about
/tmc
/donate

~~Certfified-Server-Mods~~
/blacklist

~~Certified-Server-Owners~~
/addServerMod
/removeServerMod
/setup

~~Intern-Staff~~
/addcrtf
/rmccrtf

~~Bot-Owner~~
/addadmin
/rmvadmin
```"""

lastupdate = f"""```v{client.version}: 100% Functional
TMC has now slashcommands!
```"""

client.aboutproject = """```
The reason why I started this project is because I want to protect people from money scam scenarios like I experienced. I was in such scenarios about 3 times, I was quite sad when I realized it was a money fraud, but the last time I got into such a scam, I realized that people need a sign to see if a server is a trusted server or not. So I started developing this bot and contacted friends of mine if they wanted to be the first with it so it could slowly grow. And the result was this amazing certification bot.
```"""




colors_list = {
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_NAVY': 0x2C3E50
}

option_types = {
    "SUB_COMMAND": 1,
    "SUB_COMMAND_GROUP": 2,
    "STRING": 3,
    "INTEGER": 4,
    "BOOLEAN": 5,
    "USER": 6,
    "CHANEL": 7,
    "ROLE": 8
}

error = discord.Embed(
    title=f"Error",
    description=f"🧰Invalid Permissions🧰",
    colour=colors_list["RED"]
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

already_admin = discord.Embed(
    title=":red_circle: User already an Admin",
    description="That user is already an Admin and can't be added to the database.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

not_admin = discord.Embed(
    title=":red_circle: User not an Admin",
    description="That user is not an Admin.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

already_certified = discord.Embed(
    title=":red_circle: Server Already Certified",
    description="This server has been already certified and can't be certified again.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

not1_certified = discord.Embed(
    title=":red_circle: Server isn't Certified",
    description="This server wasn't certified and can't be removed an Certification.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

already_crftowner = discord.Embed(
    title=":red_circle: User already an Certificated Server Owner",
    description="That user is already an Certificated Server Owner and can't be added to the database.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

not_crftowner = discord.Embed(
    title=":red_circle: User not Certificated Server Owner",
    description="That user is not an Certificated Server Owner.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

already_crftmod = discord.Embed(
    title=":red_circle: User already an Certificated Server Mod",
    description="That user is already an Certificated Server Mod and can't be added to the database.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

not_crftmod = discord.Embed(
    title=":red_circle: User not Certificated Server Mod",
    description="That user is not an Certificated Server Mod.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

already_blacklisted = discord.Embed(
    title=":red_circle: User already Blacklisted",
    description="That user has been already blacklisted by an certificated server Mod.",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

already_logchannel = discord.Embed(
    title=":red_circle: Channel already Logchannel",
    description="That channel is already in our database and can't be added again",
    color=colors_list['RED']
).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")







# Events

async def all_guilds_func():
    for guild in client.guilds:
        id = guild.id
        guild_ids.append(id)

@client.event
async def on_ready():
    await all_guilds_func()
    print(f"ALl Guild Id's\n{guild_ids}")

    print("\n---------\n")
    print(f"Logged in as {client.user}")
    print("\n---------\n")




@slash.slash(
    name="help",
    description="Sends Embed with all Help categories",
    guild_ids=guild_ids
)
async def _help(ctx):
    help_embed = discord.Embed(
        title="Help",
        description="Use /help for the list of Commands",
        color=colors_list["GREEN"]
    ).add_field(
        name="Certification Commands",
        value=certificate_commands,
        inline=False
    ).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    await ctx.send(embed=help_embed)





# Certification Handler

@slash.slash(name="certificate", description="Check if the Sevrer has an valid Certificate", guild_ids=guild_ids)
async def _certficate(ctx):
    certified = discord.Embed(
        title="Trusted Marketing Certification",
        description="Trusted Marketing Certification Service",
        color=colors_list["GREEN"]
    ).add_field(name="Certification Status", value=":white_check_mark: Certified", inline=False)
    certified.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")
    not_certified = discord.Embed(
        title="Trusted Marketing Certification",
        description="Trusted Marketing Certification Service",
        color=colors_list["RED"]
    ).add_field(name="Certification Status", value=":red_circle: Not Certified", inline=False)
    certified.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if str(ctx.guild.id) in certification_database['certified']:
        await ctx.send(embed=certified)
    else:
        await ctx.send(embed=not_certified)


@slash.slash(
    name="addcrtf",
    description="Add an Certification to an server",
    guild_ids=guild_ids,
)
async def _addcrtf(ctx):
    add_admin_em = discord.Embed(
        title=":white_check_mark: Created Certification",
        description="An Certification has been added to this group.",
        color=colors_list['GREEN']
    ).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")
    add_admin_em.add_field(name="Added By", value=f"{ctx.author.name}", inline=True)

    SUP124 = admins_base['admins']

    if str(ctx.author.id) in SUP124:
        if str(ctx.guild.id) in certification_database['certified']:
            await ctx.send(embed=already_certified)
        else:
            certification_database['certified'].append(str(ctx.guild.id))
            cogs._json.write_json(certification_database, "certifications")

            crftSvMods[str(ctx.guild.id)] = []
            cogs._json.write_json(crftSvMods, "serverMods")

            crftSvOwners[str(ctx.guild.id)] = []
            crftSvOwners[str(ctx.guild.id)].append(str(ctx.guild.owner_id))
            cogs._json.write_json(crftSvOwners, "certified_Owners")

            blacklist_log_channels[str(ctx.guild.id)] = []
            cogs._json.write_json(blacklist_log_channels, "blacklist_channels")

            await ctx.send(embed=add_admin_em)
    else:
        await ctx.send(embed=error)

@slash.slash(
    name="rmvcrtf",
    description="Remove an Certification to an server",
    guild_ids=guild_ids
)
async def _rmvcrtf(ctx):
    add_admin_em = discord.Embed(
        title=":red_circle: Removed Certification",
        description="An Certification has been removed from this server.",
        color=colors_list['RED']
    ).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")
    add_admin_em.add_field(name="Removed By", value=f"{ctx.author.name}", inline=True)


    if str(ctx.author.id) in admins_base['admins']:
        if str(ctx.guild.id) in certification_database['certified']:
            certification_database['certified'].remove(str(ctx.guild.id))
            cogs._json.write_json(certification_database, "certifications")

            crftSvMods.pop(str(ctx.guild.id))
            cogs._json.write_json(crftSvMods, "serverMods")

            crftSvOwners.pop(str(ctx.guild.id))
            cogs._json.write_json(crftSvOwners, "certified_Owners")

            await ctx.send(embed=add_admin_em)
        else:
            await ctx.send(embed=not1_certified)
    else:
        await ctx.send(embed=error)








# Intern Staff

@slash.slash(
    name="addadmin",
    description="Add an Certification Admin",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="user",
            description="User who should be added admin",
            option_type=option_types['USER'],
            required=True
        )
    ]
)
async def _addadmin(ctx, user:discord.Member=None):
    add_admin_em = discord.Embed(
        title=":white_check_mark: Added Certification Manager",
        description="An Certification Manager has been added to the Certification Service Team.",
        color=colors_list['GREEN']
    ).add_field(name="User", value=f"{user.mention}",inline=True)
    add_admin_em.add_field(name="Added By", value=f"{ctx.author.name}", inline=True)
    add_admin_em.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if ctx.author.id == client.owner:
        if str(user.id) in admins_base['admins']:
            await ctx.send(embed=already_admin)
        else:
            sup = admins_base['admins']
            sup.append(str(user.id))
            cogs._json.write_json(admins_base, "admins")
            await ctx.send(embed=add_admin_em)
    else:
        await ctx.send(embed=error)


@slash.slash(
    name="rmvadmin",
    description="Remove an Certification Admin",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="user",
            description="User who should be added admin",
            option_type=option_types['USER'],
            required=True
        )
    ]
)
async def _rmvadmin(ctx, user:discord.Member=None):
    add_admin_em = discord.Embed(
        title=":red_circle: Removed Certification Manager",
        description="An Certification Manager has been removed from the Certification Service Team.",
        color=colors_list['RED']
    ).add_field(name="User", value=f"{user.mention}",inline=True)
    add_admin_em.add_field(name="Removed By", value=f"{ctx.author.name}", inline=True)
    add_admin_em.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if ctx.author.id == client.owner:
        if str(user.id) in admins_base['admins']:
            sup = admins_base['admins']
            sup.remove(str(user.id))
            cogs._json.write_json(admins_base, "admins")

            await ctx.send(embed=add_admin_em)
        else:
            await ctx.send(embed=not_admin)
    else:
        ctx.send(embed=error)











# Certified Server Mods

@slash.slash(
    name="addServerMod",
    description="Add an Certificated Server Owner",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="user",
            description="User who should be added to the crft Server Mods",
            option_type=option_types['USER'],
            required=True
        )
    ]
)
async def _addServerMod(ctx, user:discord.Member=None):
    add_admin_em = discord.Embed(
        title=":white_check_mark: Added Certificated Server Mod",
        description="An Certificated Server Mod has been added to the Certificated Server Mod Database.",
        color=colors_list['GREEN']
    ).add_field(name="User", value=f"{user.mention}",inline=True)
    add_admin_em.add_field(name="Added By", value=f"{ctx.author.name}", inline=True)
    add_admin_em.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if str(ctx.author.id) in crftSvOwners[str(ctx.guild.id)] or str(ctx.author.id) in admins_base['admins']:
        if str(ctx.guild.id) in crftSvMods:
            if str(user.id) in crftSvMods[str(ctx.guild.id)]:
                await ctx.send(embed=already_crftmod)
            else:
                sup = crftSvMods[str(ctx.guild.id)]
                sup.append(str(user.id))
                cogs._json.write_json(crftSvMods, "serverMods")

                await ctx.send(embed=add_admin_em)
        else:
            await ctx.send(embed=not_crftowner)
    else:
        await ctx.send(embed=error)



@slash.slash(
    name="removeServerMod",
    description="Remove an Certificated Server Mod",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="user",
            description="User who should be removed from the crft Server Mods",
            option_type=option_types['USER'],
            required=True
        )
    ]
)
async def _removeServerMod(ctx, user:discord.Member=None):
    add_admin_em = discord.Embed(
        title=":red_circle: Removed Certificated Server Mod",
        description="An Certificated Server Mod has been removed from the Certificated Server Mod Database.",
        color=colors_list['RED']
    ).add_field(name="User", value=f"{user.mention}",inline=True)
    add_admin_em.add_field(name="Removed By", value=f"{ctx.author.name}", inline=True)
    add_admin_em.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if str(ctx.author.id) in crftSvOwners[str(ctx.guild.id)]:
        if str(ctx.guild.id) in crftSvMods:
            if not str(user.id) in crftSvMods[str(ctx.guild.id)]:
                await ctx.send(embed=not_crftmod)
            else:
                sup = crftSvMods[str(ctx.guild.id)]
                sup.remove(str(user.id))
                cogs._json.write_json(crftSvMods, "serverMods")

                await ctx.send(embed=add_admin_em)
        else:
            await ctx.send(embed=not_crftowner)
    else:
        await ctx.send(embed=error)







@slash.slash(
    name="blacklist",
    description="Blacklist someone of certified servers",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="user",
            description="User who should be globaly blacklisted",
            option_type=option_types['USER'],
            required=True
        ),
        create_option(
            name="reason",
            description="Reason why the User is being globaly blacklisted",
            option_type=option_types['STRING'],
            required=True
        )
    ]
)
async def _blacklist(ctx, user:discord.Member=None, *, reason: str=None):
    blacklistem = discord.Embed(
        title=f"Global Blacklist",
        description="An user has been blacklisted by an Moderator of an certified Server.",
        color=colors_list['RED']
    ).add_field(name="User", value=f"{user.mention}",inline=True)
    blacklistem.add_field(name="Username/Displayname", value=f"{user.display_name}", inline=True)
    blacklistem.add_field(name="UserId", value=f"{user.id}", inline=True)
    blacklistem.add_field(name="Reason", value=f"```{reason}```", inline=True)
    blacklistem.add_field(name="Server", value=f"This blacklist was completed by staff in `{ctx.guild.name}`, id: {ctx.guild.id}")
    blacklistem.set_thumbnail(url=f"{ctx.guild.icon_url}")
    blacklistem.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    executed_black = discord.Embed(
        title=":white_check_mark: Global Blacklist",
        description="Global blacklist was succesfull",
        color=colors_list['GREEN']
    ).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if str(ctx.guild.id) in crftSvMods:
        if str(user.id) in blacklist_database:
            await ctx.send(embed=already_blacklisted)
        else:

            for id1 in blacklist_log_channels:
                for channel_id in blacklist_log_channels[id1]:
                    chan = client.get_channel(int(channel_id))
                    await chan.send(embed=blacklistem)

            for x in certification_database['certified']:
                sev1 = client.get_guild(int(x))
                await sev1.ban(user=user, reason=reason)

            blacklist_database[str(user.id)] = []
            blacklist_database[str(user.id)].append(str(reason))
            cogs._json.write_json(blacklist_database, "blacklists")

            await ctx.send(embed=executed_black)
    else:
        await ctx.send(embed=error)







@slash.slash(
    name="setup",
    description="Set the channel where the global blacklists should be logged",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="channel",
            description="Channel where the Logs should be posted",
            option_type=option_types['CHANEL'],
            required=True
        )
    ]
)
async def _setup(ctx, channel:discord.TextChannel=None):
    add_admin_em = discord.Embed(
        title=":white_check_mark: Set global blacklist logchannel",
        description="An certificated server Owner or Intern Staff has set the blacklist logchannel.",
        color=colors_list['GREEN']
    ).add_field(name="Channel", value=f"{channel.mention}",inline=True)
    add_admin_em.add_field(name="Set By", value=f"{ctx.author.name}", inline=True)
    add_admin_em.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    if str(ctx.guild.id) in certification_database['certified']:
        if str(ctx.author.id) in crftSvOwners[str(ctx.guild.id)] or str(ctx.author.id) in admins_base['admins']:

            if str(channel.id) in blacklist_log_channels[str(ctx.guild.id)]:
                await ctx.send(embed=already_logchannel)
            else:
                blacklist_log_channels[str(ctx.guild.id)].append(str(channel.id))
                cogs._json.write_json(blacklist_log_channels, "blacklist_channels")

                await ctx.send(embed=add_admin_em)
        else:
            await ctx.send(embed=error)
    else:
        await ctx.send(embed=not1_certified)











# Bot **Status** cmds

@slash.slash(name="ping", description="This sends the response time of the Bot", guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(f"Pong! {client.latency * 1000}ms")


@slash.slash(name="about", description="", guild_ids=guild_ids)
async def _about(ctx):
    em11 = discord.Embed(
        title="Why this project?",
        description=client.aboutproject,
        color=colors_list["GOLD"]
    ).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    await ctx.send(embed=em11)


@slash.slash(name="getstarted", description="Get info how you can get your", guild_ids=guild_ids)
async def _getstarted(ctx):
    em11 = discord.Embed(
        title="Get Started",
        description="How do I get my Server certified and setuped?",
        color=colors_list["GOLD"]
    ).set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")
    em11.add_field(name="Step 1", value="Open an Ticket in the official server to get your server checked and certified.", inline=True)
    em11.add_field(name="Step 2", value="If you're server passed the certification test, then you should run the command `/setup` to setup the blacklist log channel.", inline=True)
    em11.add_field(name="Step 3", value="After you have set the blacklist log channel, you need to add mods which can global blacklist money fraud Scammers, use `/addServerMod` command to set an new blacklisting Mod and use `/removeServerMod` to remove an blacklisting Mod.", inline=True)
    em11.add_field(name="Finish", value="Now your server is setup and certified. The blacklisting Mods can now use the command `/blacklist` to blacklist Scammers in any certified Server, but abuse of the command can cause an revoke of the Server certification.", inline=True)
    em11.add_field(name="Communication Server", value=client.discordinvite, inline=False)
    em11.set_thumbnail(url=client.user.avatar_url)

    await ctx.send(embed=em11)


@slash.slash(name="donate", description="Donate to support TMC to stay online", guild_ids=guild_ids)
async def _donate(ctx):
    embed = discord.Embed(
        title=f'Donate',
        description='Donate to TMC 2$ to support us , that our Bot can stay online and help you guys to find trusted Servers',
        colour=colors_list["GOLD"],
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Sellix', value=f"```{client.sellixlink}```", inline=True)
    embed.add_field(name='BTC', value=f'```{client.btcaddress}```', inline=True)
    embed.add_field(name='XMR', value=f"```{client.xmraddress}```", inline=True)
    embed.add_field(name='LTC', value=f"```{client.ltcaddress}```", inline=True)
    embed.add_field(name='Developers:', value="<@655443924948877323>", inline=False)

    embed.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")
    embed.set_author(name=client.user.name, icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")

    await ctx.send(embed=embed)




@slash.slash(name="tmc", description="Trusted Marketing Certificate Statistics", guild_ids=guild_ids)
async def _tmc(ctx):
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))

    certificateaamout = 0

    for _ in certification_database['certified']:
        certificateaamout = certificateaamout + 1

    embed = discord.Embed(title=f'{client.user.name} Stats', description='\uFEFF', colour=colors_list["GOLD"],
                          timestamp=datetime.utcnow())

    embed.add_field(name='Bot Version:', value=f"```{client.version}```", inline=True)
    embed.add_field(name='Certified Servers', value=f'```{certificateaamout}```', inline=True)
    embed.add_field(name='Servers:', value=f"```{serverCount}```", inline=True)
    embed.add_field(name='Users:', value=f"```{memberCount}```", inline=True)
    embed.add_field(name='Developers:', value="<@655443924948877323>", inline=False)
    embed.add_field(name="**Last Update**", value=lastupdate, inline=False)

    embed.set_footer(text=f"TMC | {datetime.utcnow()}",icon_url="https://cdn.discordapp.com/app-icons/942121919459770408/1765517ef96be0ee58ceca0837b55a07.png?size=256")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)

    await ctx.send(embed=embed)


# SETUP CMD


client.run("OTQzMDQ4NTQ1NTEzMTExNTgz.YgtYZg.aeDCnDOz9xw2I-4x9sL5_XkdWUk")
