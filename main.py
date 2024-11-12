import os

import discord
from discord.ext import commands

import parser

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.command()
async def mzhdouze(ctx):
    await ctx.send("LOCALHOST !!!!!!!")


@bot.command()
async def monrole(ctx):
    roles = ctx.author.roles
    roles = [role.name for role in roles]
    await ctx.send(f'tu es {roles}')


@bot.command()
async def today(ctx, group: str):
    await ctx.send(parser.today(group))


@bot.command()
async def daily(ctx, group: str, date: str):
    await ctx.send(parser.daily(group, date))


bot.run(DISCORD_TOKEN)
