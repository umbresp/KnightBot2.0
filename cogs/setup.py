import discord
from ext import commands
import json
import string
from .utils import launcher
import asyncio
from __main__ import send_cmd_help
info = launcher.bot()
owner = info['owner']

class Setup():
	def __init__(self,bot):
		self.bot = bot

	
	def owner_only(ctx):

		def is_owner(ctx):
			return ctx.message.author.id == owner

		if is_owner(ctx):
			return True

		return ctx.message.author == ctx.message.server.owner

	@commands.group(pass_context=True)
	@commands.check(owner_only)
	async def config(self,ctx):
		"""Configure the bot for your server."""
		if ctx.invoked_subcommand is None:
			await send_cmd_help(ctx)

	@config.command(pass_context=True)
	async def set(self,ctx):
		'''Interactive config setup'''
		server = ctx.message.server
		user = ctx.message.author
		channel = ctx.message.channel
		msg = []
		config = json.loads(open('cogs/utils/t_config.json').read())



		x = await self.bot.say('*Welcome to the interactive bot setup system!*\n\n**Bot prefix:**')
		prefix = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not prefix:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else: 
			x = await self.bot.edit_message(x,'*Bot prefix set to:* `{}`'.format(prefix.content))
		try:
			await self.bot.delete_message(prefix)
			await asyncio.sleep(2)
		except:
			pass



		x = await self.bot.edit_message(x,'**Mod role:**')
		mod_role_m = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not mod_role_m:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else:
			mod_role = discord.utils.get(server.roles, name=mod_role_m.content)
			if mod_role is None:
				x = await self.bot.edit_message(x, 'Could not find the mod role.')
			else:
				x = await self.bot.edit_message(x,'*Moderator role set to:* {}'.format(mod_role.mention))
		try:
			await self.bot.delete_message(mod_role_m)
			await asyncio.sleep(2)
		except:
			pass


		x = await self.bot.edit_message(x,'**Admin role:**')
		admin_role_m = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not admin_role_m:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else:
			admin_role = discord.utils.get(server.roles,name=admin_role_m.content)
			if admin_role is None:
				x = await self.bot.edit_message(x, 'Could not find the admin role.')
			else:
				x = await self.bot.edit_message(x,'*Administrator role set to:* {}'.format(admin_role.mention))
		try:
			await self.bot.delete_message(admin_role_m)
			await asyncio.sleep(2)
		except:
			pass


		x = await self.bot.edit_message(x,'**Admin Channel:**')
		admin_chat = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not admin_chat:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else:
			if admin_chat.content.startswith('<#'):
				x = await self.bot.edit_message(x,'*Administrative channel set to:* {}'.format(admin_chat.content))
			else:
				x = await self.bot.edit_message(x,'Incorrect format of channel passed. Must be a channel mention.')
		try:
			await self.bot.delete_message(admin_chat)
			await asyncio.sleep(2)
		except:
			pass



		x = await self.bot.edit_message(x,'**Announcement channel:**')
		a_channel = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not a_channel:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else:
			if a_channel.content.startswith('<#'):
				x = await self.bot.edit_message(x,'*Announcements channel set to:* {}'.format(a_channel.content))
			else:
				x = await self.bot.edit_message(x,'Incorrect format of channel passed. Must be a channel mention.')
		try:
			await self.bot.delete_message(a_channel)
			await asyncio.sleep(2)
		except:
			pass



		x = await self.bot.edit_message(x,'**Tournament channel:**')
		t_channel = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not t_channel:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else:
			if t_channel.content.startswith('<#'):
				x = await self.bot.edit_message(x,'*Tournament channel set to:* {}'.format(t_channel.content))
			else:
				x = await self.bot.edit_message(x,'Incorrect format of channel passed. Must be a channel mention.')
		try:
			await self.bot.delete_message(t_channel)
			await asyncio.sleep(2)
		except:
			pass


		x = await self.bot.edit_message(x,'**Mod-logs channel:**')
		m_channel = await self.bot.wait_for_message(timeout=30,author=user,channel=channel)
		if not m_channel:
			x = await self.bot.edit_message(x,'*Configuration Canceled*')
			return
		else:
			if m_channel.content.startswith('<#'):
				x = await self.bot.edit_message(x,'*Moderation-Logging channel set to:* {}'.format(m_channel.content))
			else:
				x = await self.bot.edit_message(x,'Incorrect format of channel passed. Must be a channel mention.')
		try:
			await self.bot.delete_message(m_channel)
			await asyncio.sleep(2)
		except:
			pass
		

		config[server.id]["prefix"] = prefix.content.strip()
		config[server.id]["mod_role"] = mod_role.id
		config[server.id]["admin_role"] = admin_role.id
		config[server.id]["admin_chat"] = admin_chat.content.strip(string.punctuation)
		config[server.id]["announcements"] = a_channel.content.strip(string.punctuation)
		config[server.id]["tournaments"] = t_channel.content.strip(string.punctuation)
		config[server.id]["mod_log"] = m_channel.content.strip(string.punctuation)
		config[server.id]["!name"] = server.name

		

		config = json.dumps(config, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(config)
		x = await self.bot.say('**Configuration Complete.**')

	@config.command(pass_context=True)
	async def show(self,ctx,arg = None):
		'''Show basic server configuration'''
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())

		config = data[server.id]

		if arg is None:
			prefix = config['prefix']

			mod_role = discord.utils.get(server.roles, id=config['mod_role'])
			if mod_role:
				mod_role = mod_role.mention
			admin_role = discord.utils.get(server.roles, id=config['admin_role'])
			if admin_role:
				admin_role = admin_role.mention

			admin_chat = self.bot.get_channel(config['admin_chat'])
			if admin_chat:
				admin_chat = admin_chat.mention

			announcements = self.bot.get_channel(config['announcements'])
			if announcements:
				announcements = announcements.mention

			if self.bot.get_channel(config['tournaments']):
				tournaments = self.bot.get_channel(config['tournaments'])
				tournaments = tournaments.mention
			else:
				tournaments = None

			if self.bot.get_channel(config['mod_log']):
				mod_log = self.bot.get_channel(config['mod_log'])
				mod_log = mod_log.mention
			else:
				mod_log = None

			em = discord.Embed(color=0x00FFFFF)
			em.set_author(name='Server Configuration', icon_url=server.icon_url)
			em.set_thumbnail(url=server.icon_url)
			em.add_field(name='Mod Role',value=mod_role)
			em.add_field(name='Admin Role',value=admin_role)
			em.add_field(name='Admin Channel',value=admin_chat)
			em.add_field(name='Announcements',value=announcements)
			em.add_field(name='Tournaments',value=tournaments)
			em.add_field(name='Mod-Logs', value=mod_log)
			em.set_footer(text='ID: '+server.id+' | Prefix: '+prefix)

			await self.bot.say(embed=em)
			
		elif arg == 'raw':
			config = json.dumps(config, indent=4, sort_keys=True)
			await self.bot.say('**Raw json data for your server:**')
			for page in self.paginate(config, 1900):
				await self.bot.say('```json\n{}```'.format(page))
		else:
			pass

	@config.command(pass_context=True)
	async def prefix(self,ctx,*, prefix : str):
		'''Change server prefix'''
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())

		data[server.id]['prefix'] = prefix

		data = json.dumps(data, indent=4, sort_keys=True)


		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)


		await self.bot.say('Changed server prefix to: `{}`'.format(prefix))

	@config.command(pass_context=True)
	async def mod(self,ctx,*, mod : str):
		'''Change the mod_role'''
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		role = discord.utils.get(server.roles, name=mod)

		data[server.id]['mod_role'] = role.id

		data = json.dumps(data, indent=4, sort_keys=True)


		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)

		await self.bot.say('Changed modrole to: `{}`'.format(role.name))

	@config.command(pass_context=True)
	async def admin(self,ctx,*, admin : str):
		"""Change the admin_role"""
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		role = discord.utils.get(server.roles, name=admin)

		data[server.id]['admin_role'] = role.id

		data = json.dumps(data, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)

		await self.bot.say('Changed admin_role to: `{}`'.format(role.name))

	@config.command(pass_context=True)
	async def autorole(self,ctx,*, role : str):
		"""Change the join role"""
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		role = discord.utils.get(server.roles, name=role)

		data[server.id]['autorole'] = role.id

		data = json.dumps(data, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)

		await self.bot.say('Changed autorole to: `{}`'.format(role.name))



	@config.command(pass_context=True)
	async def welcome(self,ctx,channel : discord.Channel,*, msg : str = None):
		"""Change the welcome message and destination"""
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())

		data[server.id]['welcome']['channel'] = channel.id

		if msg:
			data[server.id]['welcome']['msg'] = msg
			await self.bot.say('Welcome message set to `{}` in {}'.format(msg, channel.mention))
		else:
			data[server.id]['welcome']['msg'] = 'Welcome {0.mention} to {1.name}!'
			await self.bot.say('Welcome message set to `{}` in {}'.format('Welcome {0.mention} to {1.name}!', channel.mention))

		data = json.dumps(data, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)



	@config.command(pass_context=True)
	async def leave(self,ctx,channel : discord.Channel,*, msg : str = None):
		"""Change the leave message and destination"""
		server = ctx.message.server

		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())

		data[server.id]['leave']['channel'] = channel.id

		if msg:
			data[server.id]['leave']['msg'] = msg
			await self.bot.say('Leave message set to `{}` in {}'.format(msg, channel.mention))
		else:
			data[server.id]['leave']['msg'] = '{0.name} has just left the server.'
			await self.bot.say('Leave message set to `{}` in {}'.format('{0.name} has just left the server.', channel.mention))

		data = json.dumps(data, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', 'w') as f:
			f.write(data)


	@config.command(pass_context=True)
	async def disable(self, ctx, function):
		'''Disable features.'''
		server = ctx.message.server
		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		if function == 'levels':
			data[server.id]['levels'] = False
			await self.bot.say('Disabled levels for this server.')
		if function == 'welcome':
			data[server.id]['welcome']['status'] = False
			await self.bot.say('Disabled the welcome message.')
		if function == 'leave':
			data[server.id]['leave']['status'] = False
			await self.bot.say('Disabled the leave message.')

		data = json.dumps(data, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', "w") as f:
			f.write(data)


	@config.command(pass_context=True)
	async def enable(self, ctx, function):
		'''Enable features.'''
		server = ctx.message.server
		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		if function == 'levels':
			data[server.id]['levels'] = True
			await self.bot.say('Enabled levels for this server.')
		if function == 'welcome':
			data[server.id]['welcome']['status'] = True
			await self.bot.say('Enabled the welcome message.')
		if function == 'leave':
			data[server.id]['leave']['status'] = True
			await self.bot.say('Enabled the leave message.')


		data = json.dumps(data, indent=4, sort_keys=True)

		with open('cogs/utils/t_config.json', "w") as f:
			f.write(data)

	async def on_message(self,message):
		server = message.server
		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		if server.id not in data:
			data[server.id] = {}
			role = discord.utils.get(server.roles, name='Mod')
			if role:
				data[server.id]["mod_role"] = role.id
			else:
				data[server.id]["mod_role"] = None
			role = discord.utils.get(server.roles, name='Admin')
			if role:
				data[server.id]["admin_role"] = role.id
			else:
				data[server.id]["admin_role"] = None
			data[server.id]["admin_chat"] = None
			data[server.id]["prefix"] = '!'
			data[server.id]["announcements"] = None
			data[server.id]["tournaments"] = None
			data[server.id]["mod_log"] = None
			data[server.id]["!name"] = server.name
			data[server.id]["levels"] = False
			data[server.id]["autorole"] = None
			data[server.id]["selfroles"] = []
			data[server.id]["aliases"] = {}
			data[server.id]["welcome"] = {

			"msg":'Welcome {0.mention} to {1.name}!',
			"channel":"default",
			"status": True

			}

			data[server.id]["leave"] = {

			"msg": '{0.name} has just left the server.',
			"channel":"default",
			"status": False

			}

			data = json.dumps(data, indent=4, sort_keys=True)

			with open('cogs/utils/t_config.json', "w") as f:
				f.write(data)

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



def setup(bot):
	bot.add_cog(Setup(bot))

