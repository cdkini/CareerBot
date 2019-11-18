import discord
import os
import random

from discord.ext import commands
from secrets import credentials_dict


bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used. Use -help to see valid commands.')

@bot.command(help='Removes {num} messages from the chat')
async def clean(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

@bot.command(help='Enables {title} category')
async def enable(ctx, ext):
    await ctx.send(f'Category "{ext.title()}" enabled.')
    bot.load_extension(f'cogs.{ext}')

@bot.command(help='Disables {title} category')
async def disable(ctx, ext):
    await ctx.send(f'Category "{ext.title()}" disabled.')
    bot.unload_extension(f'cogs.{ext.lower()}')

@bot.command(help='Reenables all categories')
async def reset(ctx):
    await ctx.send(f'Reset to factory settings.')
    ext_list = [ext for ext in os.listdir('Discord-Bot/cogs')]
    for ext in ext_list:
        bot.load_extension(f'cogs.{ext[:-3]}')

for file_name in os.listdir('Discord-Bot/cogs'):
    try:
        if file_name.endswith('.py'):
            bot.load_extension(f'cogs.{file_name[:-3]}')
    except Exception as e:
        print(e)

def main():
    bot.run(credentials_dict['token'])