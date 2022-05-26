import asyncio
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="!")


@bot.command(name='add_group')
async def members(ctx: discord.context):
    users = []
    for guild in bot.guilds:
        for member in guild.members:
            if member.guild.name == ctx.message.guild.name and not member.bot:
                users.append((member.name, member.discriminator, member.id))

    options = user2option(users)

    await ctx.send("What is your team name ?")
    try:
        cat_name = await bot.wait_for('message', timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.channel.send('You ran out of time to answer!')

    await ctx.channel.send(f'Your name of team is **{cat_name.content}**')

    class Choose(discord.ui.View):
        @discord.ui.select(
            placeholder="Choose your teammate(s)",
            min_values=1,
            max_values=len(options),
            options=options
        )
        async def select_callback(self, select, interaction):
            await interaction.response.send_message(
                f"{select2string(select)} are your teammates. A category and a channel will be create")

    await ctx.send("Choose your teammate(s)", view=Choose())

    # TODO : create private category and private channels
    cat = await ctx.guild.create_category(cat_name.content)
    # await guild.create_text_channel('annonces', category=cat)
    # await guild.create_text_channel('liens-importants', category=cat)
    # await guild.create_text_channel('general', category=cat)
    # await guild.create_text_channel('annonces', category=cat)
    # await guild.create_voice_channel('audio', category=cat)

    # TODO : create the role with permissions
    color = random.randint(0, 0xffffff)
    role = await ctx.guild.create_role(name=str(cat_name.content), colour=discord.Colour(color))
    # 0b11111111111111111111111111111111111111111

    # Add persons on the role
    for usr in users:
        usr_tmp = ctx.guild.get_member(usr[2])
        await usr_tmp.add_roles(role)

    # TODO : refacto the code in classes
    # TODO : add try catch everywhere
    # TODO : Docker to be run everywhere
    return users


def user2option(users):
    res = []
    for usr in users:
        res.append(discord.SelectOption(label=usr[0],
                                        description=usr[0] + '#' + usr[1]))
    return res


def select2string(select):
    res = ""
    for e in select.options:
        # print(e.label)
        res += str(e.label)
        res += ', '
    return res


@bot.event
async def on_ready():
    print("Bot ready!")


bot.run(os.getenv("TOKEN"))
