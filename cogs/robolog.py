import discord
from ext import commands
import datetime
from .utils import launcher
from __main__ import send_cmd_help
from .utils.paginator import Pages

info=launcher.bot()
owner = info['owner']

class Robolog:
	def __init__(self, bot):	
		self.bot = bot

	def getday(self):
		day = None
		day = datetime.datetime.now()
		day = day.strftime("%d/%m/%Y")
		return day

	def mod(ctx):
		info = launcher.config()
		server = ctx.message.server
		modrole = discord.utils.get(server.roles, id=info[server.id]['admin_role'])
		def is_owner(ctx):
			return ctx.message.author.id == owner
		if is_owner(ctx):
			return True
		if modrole:
			modrole = modrole.name
		author = ctx.message.author
		return discord.utils.get(author.roles,name=modrole)


	@commands.group(pass_context=True)
	@commands.check(mod)
	async def log(self, ctx):
		"""Robotics Log Commands"""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@log.command(pass_context=True)
	async def entry(self, ctx, *, entry : str):
		"""Create a log entry"""
		date = self.getday()
		msg = open('cogs/utils/robolog.txt').read()
		with open('cogs/utils/robolog.txt','a') as log:
			if date not in msg:
				log.write('\n+ '+date+'\n- '+entry+'\n')
			else:
				log.write('- '+entry+'\n')

		await self.bot.say('Added `{}` to the log'.format(entry))

	@log.command(pass_context=True)
	async def show(self, ctx):
		"""Show the current log"""
		msg = open('cogs/utils/robolog.txt').read()
		log = '```diff\n'+'!---===[ Change Log ]===---!'+(''.join(msg))+'```'
		await self.bot.say(log)

	@log.command(name='del',pass_context=True, aliases=['delete','d'])
	async def del_(self, ctx, index: int = None):
		'''Delete a log entry from the back, or by index (reversed)'''
		log = []
		with open('cogs/utils/robolog.txt') as f:
			for line in f:
				log.append(line)
		if index is None:
			x = log.pop()
			await self.bot.say('Successfully removed `{}` from the log'.format(x[1:].strip()))
			
		else:
			await self.bot.say('Successfully removed `{}` from the log'.format(log[len(log) - index][1:].strip()))
			del log[len(log) - index]
			ahel

		log = ''.join(log)

		with open('cogs/utils/robolog.txt', 'w') as f:
			f.write(log)

	


def setup(bot):
    bot.add_cog(Robolog(bot))



