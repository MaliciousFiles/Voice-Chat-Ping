from gevent import monkey
monkey.patch_all()
import discord
import os
from flask import Flask
from flask_compress import Compress
from gevent.pywsgi import WSGIServer
from threading import Thread

client = discord.Client()

def get_role(guild, name):
    return discord.utils.get(guild.roles, name=name)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(name="users changing voice chats", type=discord.ActivityType.listening))


@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    if after.channel:
        channel_name = after.channel.name
        if not get_role(guild, channel_name):
            await guild.create_role(name=channel_name, mentionable=True)

        role = get_role(guild, channel_name)
        await member.add_roles(role)
    if before.channel:
        await member.remove_roles(get_role(guild, before.channel.name))

app = Flask('')

@app.route('/')
def home():
    client.run(os.environ["token"])
    return "Voice Chat Ping active!"

def run():
  WSGIServer(('0.0.0.0', 8080), app).serve_forever()

compress = Compress()
compress.init_app(app)
Thread(target=run).start()

