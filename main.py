import os

import discord
from dotenv import load_dotenv

client = discord.Client()

load_dotenv()

@client.event
async def on_ready():
    print("Prêt!")


@client.event
async def on_message(msg: discord.Message):
    print(msg.channel)
    if msg.content == 'test':
        await msg.channel.send('toto')


client.run(os.getenv("TOKEN"))

# if __name__ == '__main__':
#    for i, arg in enumerate(sys.argv):
#        if i == 1:
#            token = arg
