import discord
from datetime import datetime

client = discord.Client()

TOKEN = config.TOKEN

global bot_channel
global timer


@client.event
async def on_ready():
    global bot_channel
    global timer
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    timer = None
    for channel in client.get_all_channels():
        if channel.name == 'filtered-tribe-log':
            bot_channel = channel
            break


@client.event
async def on_message(message):
    global bot_channel
    global timer
    if message.content.startswith('!exit') and str(message.author).__eq__("Jannik / Krümel#8630"):
        await message.channel.send("Bot exit initiated\n")
        exit(0)
    if message.channel.name == 'tribe-log':
        key = message.content.find('\n')
        data = message.content[key + 1:].split("!")
        important_keys = ["starved to death", "was destroyed", "(Crewmember) was killed", "Your Company killed",
                          "has become a settler in your Settlement", "is stealing your"]
        for entry in data:
            key = entry.find(": ")
            entry = entry[key + 2:]
            for important_key in important_keys:
                if entry.find(important_key) != -1:
                    if important_key == "(Crewmember) was killed" or important_key == "starved to death":
                        await bot_channel.send(entry)
                    else:
                        if timer is None:
                            await bot_channel.send("@here " + entry)
                            timer = datetime.now()
                        else:
                            if (datetime.now() - timer).seconds > 600:
                                await bot_channel.send("@here " + entry)
                                timer = datetime.now()
                            else:
                                await bot_channel.send(entry)
                    break


client.run(TOKEN)
