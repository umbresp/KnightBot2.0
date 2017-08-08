import discord
from ext.commands import Bot
from ext import commands
import json
from .utils import launcher
from __main__ import send_cmd_help


info = launcher.bot()
owner = info['owner']


class Alias:

	def __init__(self, bot):
		self.bot = bot

	def mod(ctx):
		info = launcher.config()
		server = ctx.message.server
		s_owner = server.owner
		modrole = discord.utils.get(server.roles, id=info[server.id]['mod_role'])
		adminrole = discord.utils.get(server.roles, id=info[server.id]['admin_role'])
		author = ctx.message.author
		def is_owner(ctx):
		    return ctx.message.author.id == owner
		if author is s_owner:
		    return True
		if is_owner(ctx):
		    return True
		if modrole:
		    modrole = modrole.name
		if adminrole:
		    adminrole = adminrole.name
		if discord.utils.get(author.roles,name=adminrole):
		    return True
		return discord.utils.get(author.roles,name=modrole)


	async def on_message(self, message):
		with open('cogs/utils/t_config.json') as f:
			data = json.load(f)
		server = message.server
		prefix = data[server.id]['prefix']
		if message.content.startswith(prefix):
			cmd = message.content.strip(prefix)
			if cmd in data[server.id]['aliases']:		
				to_exec = prefix + data[server.id]['aliases'][cmd]
				message.content = to_exec
				await self.bot.process_commands(message)


	@commands.group(pass_context=True)
	async def alias(self, ctx):
		''' Make command aliases! '''
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@alias.command(pass_context=True)
	@commands.check(mod)
	async def add(self, ctx, alias, *, cmd):
		''' Add an alias for a command '''

		server = ctx.message.server

		with open('cogs/utils/t_config.json') as file:
			data = json.load(file)
			existing = data[server.id]['aliases']

		cmd = cmd.strip().strip(ctx.prefix)
		base = cmd.split()[0]

		if alias in self.bot.commands or alias in existing:
			await self.bot.say('You cannot add an existing command or alias!')
			return

		if base in self.bot.commands:
			data[server.id]['aliases'][alias] = cmd
			await self.bot.say('Successfully added the `{}` alias for the server.'.format(alias))
		else:
			await self.bot.say('The command you are linking to the alias does not exist.')

		with open('cogs/utils/t_config.json', 'w') as file:
			file.write(json.dumps(data, indent=4, sort_keys=True))

	@alias.command(pass_context=True, name='del')
	@commands.check(mod)
	async def _del(self, ctx, *, alias):
		"""Remove an existing alias"""
		server = ctx.message.server
		with open('cogs/utils/t_config.json') as file:
			data = json.load(file)
			existing = data[server.id]['aliases']
		try:
			del existing[alias]
		except KeyError:
			await self.bot.say('No such alias exists.')
		else:
			await self.bot.say('Alias `{}` successfully removed!'.format(alias))

		with open('cogs/utils/t_config.json', 'w') as file:
			file.write(json.dumps(data, indent=4, sort_keys=True))


	@alias.command(pass_context=True)
	async def show(self, ctx, *, alias = None):
		server = ctx.message.server
		prefix = ctx.prefix
		with open('cogs/utils/t_config.json') as file:
			data = json.load(file)
			existing = data[server.id]['aliases']
		if alias is None:
			all_aliases = ', '.join(existing.keys())
			await self.bot.say('List of server aliases:\n```bf\n{}```'.format(all_aliases))
			return
		try:
			cmd = '`{}{}`'.format(prefix, existing[alias])
		except KeyError:
			await self.bot.say('No such alias exists.')
		else:
			await self.bot.say('`{}` yields : {}'.format(alias, cmd))

	@commands.command(pass_context=True)
	async def aliases(self, ctx):
		server = ctx.message.server
		with open('cogs/utils/t_config.json') as file:
			data = json.load(file)
			existing = data[server.id]['aliases']
			all_aliases = ', '.join(existing.keys())
			await self.bot.say('List of server aliases:\n```bf\n{}```'.format(all_aliases))





def setup(bot):
    bot.add_cog(Alias(bot))