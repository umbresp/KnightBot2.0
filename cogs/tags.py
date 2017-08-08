import discord
from ext import commands
import json
import difflib
from .utils import launcher



class Tags():
	def __init__(self, bot):
		self.bot = bot

	


	async def make_tag(self, tag, content, user):
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		if tag in data:
			await self.bot.say('This tag-name already exists.')
		elif tag not in data:
			data[tag] = [content,user.id]
			print(data)
			data = json.dumps(data,indent=2)
			with open('cogs/utils/tags.json', 'w') as f:
				f.write(data)
			await self.bot.say('Successfuly created tag.')

	async def edit_tag(self,ctx, tag, content, user):
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		info = launcher.config()
		server = ctx.message.server
		modrole = discord.utils.get(server.roles, id=info[server.id]['mod_role'])
		admin_role = discord.utils.get(user.roles, id=info[server.id]['admin_role'])

		if tag not in data:
			possible_matches = difflib.get_close_matches(tag, tuple(data.keys()))
			if not possible_matches:
				await self.bot.say('**Tag not found.**')
			else:
				possible_matches = ['`'+i+'`' for i in possible_matches]
				await self.bot.say(('Tag not found. Did you mean: ' + ', '.join(possible_matches)).strip(', '))

		if data[tag][1] == user.id or discord.utils.get(user.roles, name=admin_role):
			data[tag] = [content,user.id]
			data = json.dumps(data, indent=2)
			with open('cogs/utils/tags.json', 'w') as f:
				f.write(data)
			await self.bot.say('Successfully edited the tag')
		else:
			await self.bot.say('You are not the owner of this tag.')


	@commands.group(pass_context=True, invoke_without_command=True)
	async def tag(self, ctx, *,name : str):
		"""Tag related commands, store text"""
		if ctx.invoked_subcommand is None:
			data = open('cogs/utils/tags.json').read()
			data = json.loads(data)
			try: 
				d = data[name][0]
				await self.bot.say(d)
			except:
				possible_matches = difflib.get_close_matches(name, tuple(data.keys()))
				if not possible_matches:
					await self.bot.say('**Tag not found.**')
				else:
					possible_matches = ['`'+i+'`' for i in possible_matches]
					await self.bot.say(('Tag not found. Did you mean: ' + ', '.join(possible_matches)).strip(', '))


	@tag.command(pass_context=True, aliases=['create'])
	async def make(self, ctx, tag: str, *, content: str):
		user = ctx.message.author
		await self.make_tag(tag,content,user)

	@tag.command(name='del',pass_context=True, aliases=['d', 'delete'])
	async def _del(self, ctx, name : str):
		info = launcher.config()
		server = ctx.message.server
		user = ctx.message.author
		modrole = discord.utils.get(user.roles, id=info[server.id]['mod_role'])
		admin_role = discord.utils.get(user.roles, id=info[server.id]['admin_role'])
		flag = None
		if modrole or admin_role:
			flag = True

		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		if user.id == data[name][1] or flag:
			del data[name]
			await self.bot.say('Tag deleted.')
		else:
			await self.bot.say('You cannot delete a tag you do not own.')
		data = json.dumps(data, indent=2)
		with open('cogs/utils/tags.json', 'w') as f:
			f.write(data)

	@tag.command(pass_context=True)
	async def edit(self, ctx, tag: str, *, content):
		user = ctx.message.author
		await self.edit_tag(ctx,tag,content,user)

	@commands.command(pass_context=True)
	async def tags(self,ctx):
		"""Shows all the tags"""
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		data = ', '.join(data.keys())
		data = data.strip(', ')
		print(data)
		data = '```brainfuck\n'+data+'```'
		print(data)
		await self.bot.say('**List of current tags:**\n'+data)






def setup(bot):
	bot.add_cog(Tags(bot))
