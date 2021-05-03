#!/usr/bin/env python3
import discord

client = discord.Client()

log_file = open("vcping_log", "w+")


def get_role(guild, name):
    return discord.utils.get(guild.roles, name=name)


@client.event
async def on_ready():
    log_file.write("connected as " + client.user)


@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    if after.channel:
        channel_name = after.channel.name
        if not get_role(guild, channel_name):
            await guild.create_role(name=channel_name, mentionable=True)

        role = get_role(guild, channel_name)
        await member.add_roles(role)
        log_file.write("giving member " + member.name + " role " + role.name)
    if before.channel:
        log_file.write("removing role "
                       + get_role(guild, before.channel.name).name
                       + " from member " + member.name)
        await member.remove_roles(get_role(guild, before.channel.name))

with open("token", "r") as token_file:
    log_file.write("starting as " + client.user)
    client.run(token_file.read())
    token_file.close()
    log_file.close()
