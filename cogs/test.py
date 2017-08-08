import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping():
    await bot.say('pong')


bot.run('TOKEN HERE')





with open('utils/t_config.json') as f:
	cont = f.read()


def paginate(self, sequence, num):
    count = 1
    rows = list()
    cols = list()
    for item in sequence:
        if count == num:
            cols.append(item)
            rows.append(cols)
            cols = list()
            count = 1
        else:
            cols.append(item)
            count += 1
    if count > 0:
        rows.append(cols)
    for row in rows:
    	yield ''.join(row)

for page in paginate(cont, 1900):
	print(page)

