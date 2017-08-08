
from ext.commands import Bot
from ext import commands
import datetime
import time
import random
import asyncio
import json
import discord
from discord.ext.commands.cooldowns import BucketType
import operator

class Levels():
	def __init__(self, bot):
		self.bot = bot

	def level(self,user,channel):
		lvls_xp = [5*(i**2)+960*i+100 for i in range(100)]
		with open('cogs/utils/levels.json') as f:
			levels = json.loads(f.read())
		xp = random.randint(15,25)
		if user.id not in levels:
			levels[user.id] = {'xp':0,'lvl':0}
		xp += levels[user.id]['xp']
		lvl = 0
		lvl_p = levels[user.id]['lvl']
		nxt = 0
		for i,num in list(enumerate(lvls_xp)):
			if xp <= num:
				lvl = i
				nxt = num
				break
		if lvl > lvl_p:
			flag = True
		else:
			flag = False

		rankdict = {}

		for key in levels.keys():
			rankdict[key] = levels[key]['xp']

		sorted_x = sorted(rankdict.items(), key=operator.itemgetter(1), reverse=True)
		rank = 0
		leng = len(sorted_x)
		for i,key in list(enumerate(sorted_x)):
			if key[0] == user.id:
				rank = i+1
				break

		levels[user.id] = {'xp':xp,'lvl':lvl,'name':str(user)}
		levels = json.dumps(levels,indent=4)
		with open('cogs/utils/levels.json','w') as f:
		    f.write(levels)
		return [lvl,xp,nxt,rank,leng,flag]

	async def on_message(self,message):
		with open('cogs/utils/t_config.json') as f:
			data = json.loads(f.read())
		server = message.server
		if data[server.id]["levels"] is True:	
		    user = message.author
		    channel = message.channel
		    if user == self.bot.user:
		        return
		    if user.bot:
		    	return
		    x = self.level(user,channel)
		    if x[5] is True:
		    	await self.bot.send_message(channel,'Well played! **{}** has just advanced to level **{}**.'.format(user.name, x[0]))

	@commands.command(pass_context=True)
	async def rank(self,ctx, user : discord.Member = None):
		server = ctx.message.server
		if not user: user = ctx.message.author
		info = self.level(user, ctx.message.channel)
		if not user.avatar_url:
			av = user.default_avatar_url
		else:
			av = user.avatar_url
		data = discord.Embed(color=0x00FFFF)
		data.set_author(name=user.name, icon_url=av)
		data.add_field(name='Rank', value='{}/{}'.format(info[3],info[4]))
		data.add_field(name='Level', value=info[0])
		data.add_field(name='XP', value='{}/{}'.format(info[1],info[2]))
		data.set_footer(text='KnightBot')
		

		await self.bot.say(embed=data)

	@commands.command(pass_context=True,aliases=['lb','leader','ld'])
	async def leaderboard(self,ctx):
		server = ctx.message.server

		with open('cogs/utils/levels.json') as f:
			levels = json.loads(f.read())
		rankdict = {}
		for key in levels.keys():
			rankdict[key] = levels[key]['xp']
		sorted_x = sorted(rankdict.items(), key=operator.itemgetter(1), reverse=True)
		usrs = []
		for i in range(10):
			usrs.append(sorted_x[i][0])
		print(usrs)
		msg = ''
		for i,usr in list(enumerate(usrs)):
			mem = levels[usr]['name']
			if i == 9:
				msg += (str(i+1)+'  '+str(mem)+'\n')
				break
			msg += (str(i+1)+'   '+str(mem)+'\n')
		print(msg)
		await self.bot.say('```py\n'+msg+'```')



def setup(bot):
    bot.add_cog(Levels(bot))
