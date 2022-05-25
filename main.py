import asyncio
import os

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
    # await print(reply_message)

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
    await ctx.guild.create_category(cat_name.content)
    # TODO : create some channels
    # TODO : create the role
    # await ctx.guild.create_role(name="role name")
    # TODO : Add persons on the role
    # TODO : refacto the code in classes
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
