import discord

client = discord.Client()

def get_role(guild, name):
    return discord.utils.get(guild.roles, name=name)

@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    if after.channel:
        channel_name = after.channel.name
        if not get_role(guild, channel_name):
            await guild.create_role(name=channel_name, mentionable=True)

        role = get_role(guild, channel_name)
        await member.add_roles(role)
        print("giving member " + member.name + " role " + role.name)
    if before.channel:
        print("removing role " + get_role(guild, before.channel.name).name + " from member " + member.name)
        await member.remove_roles(get_role(guild, before.channel.name))

client.run('ODM0MjYzMjkxOTY5Nzk4MTY0.YH-WPA.8KjR4og2bBYJry5DxgQDmz3myOI')
