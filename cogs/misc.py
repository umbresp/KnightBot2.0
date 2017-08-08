import discord
from ext.commands import Bot
from ext import commands
import datetime
import time
import random
import asyncio
import json



class Misc():


    def __init__(self, bot):
        self.bot = bot
        self.ball = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                     'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                     'Very doubtful']
        self.sayerrs = ["Not so fast cheeky boi xD", "Ayy lmao it doesn't work :D",
                        "LOL fail you better delete that now before people get mad",
                        "How about I tag you instead", "That would be abusing admin perms.",
                        "Attention: You have been muted for attempting to troll people with me!"]
        # can't think of more at the moment ^
        self.selfroles = ['Subscriber','Hype']

    async def send_cmd_help(self,ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    @commands.command(pass_context=True)
    async def embedsay(self,ctx, *, message: str = None):
        '''Embed something as the bot.'''
        color = ("#%06x" % random.randint(8, 0xFFFFFF))
        color = int(color[1:],16)
        color = discord.Color(value=color)
        if message:
            msg = ctx.message
            emb = discord.Embed(color=color,description=message)
            await self.bot.delete_message(msg)
            await self.bot.say(embed=emb)
        else:
            await self.bot.say('Usage: `.embedsay [message]`')


    @commands.command()
    async def say(self,*, message: str):
        '''Say something as the bot.'''
        if '@everyone' in message:
            await self.bot.say(random.choice(self.sayerrs))
        elif '@here' in message:
            await self.bot.say(random.choice(self.sayerrs))
        elif "<@" in message:
            await self.bot.say("Say it to their face!")
        else:
            await self.bot.say(message)

            
    @commands.command()
    async def add(self,*args):
        '''Add multiple numbers.'''
        ans = 0
        try:
            for i in args:
                ans += int(i)
            await self.bot.say(ans)
        except:
            await self.bot.say('Enter numbers only.')
            

    @commands.command(pass_context=True,description='Response time is in ms.')
    async def ping(self,ctx):
        '''Check response time.'''

        msgtime = ctx.message.timestamp.now()
        await (await self.bot.ws.ping())
        now = datetime.datetime.now()
        ping = now - msgtime
        pong = discord.Embed(title='Pong! Response Time:', description=str(ping.microseconds / 1000.0) + ' ms',
                             color=0x00ffff)
        await self.bot.send_message(ctx.message.channel, embed=pong)

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------


    @commands.command(pass_context=True)
    async def virus(self,ctx,user: discord.Member=None,*,hack=None):
        """Inject a virus into someones system."""
        nome = ctx.message.author
        if not hack:
            hack = 'discord'
        else:
            hack = hack.replace(' ','-')
        channel = ctx.message.channel
        x = await self.bot.send_message(channel, '``[▓▓▓                    ] / {}-virus.exe Packing files.``'.format(hack))
        await asyncio.sleep(1.5)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓                ] - {}-virus.exe Packing files..``'.format(hack))
        await asyncio.sleep(0.3)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {}-virus.exe Packing files...``'.format(hack))
        await asyncio.sleep(1.2)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {}-virus.exe Initializing code.``'.format(hack))
        await asyncio.sleep(1)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {}-virus.exe Initializing code..``'.format(hack))
        await asyncio.sleep(1.5)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {}-virus.exe Finishing.``'.format(hack))
        await asyncio.sleep(1)
        x = await self.bot.edit_message(x,'``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {}-virus.exe Finishing..``'.format(hack))
        await asyncio.sleep(1)
        x = await self.bot.edit_message(x,'``Successfully downloaded {}-virus.exe``'.format(hack))
        await asyncio.sleep(2)
        x = await self.bot.edit_message(x,'``Injecting virus.   |``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus..  /``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus... -``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus....\``')
        await self.bot.delete_message(x)
        await self.bot.delete_message(ctx.message)
        
        if user:
            await self.bot.say('`{}-virus.exe` successfully injected into **{}**\'s system.'.format(hack,user.name))
            await self.bot.send_message(user,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
        else:
            await self.bot.say('**{}** has hacked himself ¯\_(ツ)_/¯.'.format(name.name))
            await self.bot.send_message(name,'**Alert!**\n``You may have been hacked. {}-virus.exe has been found in your system\'s operating system.\nYour data may have been compromised. Please re-install your OS immediately.``'.format(hack))
     
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------


    @commands.group(name='self',pass_context=True,invoke_without_subcommand=True)
    async def self_(self,ctx,role):
        """Selfrole commands"""
        if ctx.invoked_subcommand is None:
            user = ctx.message.author
            server = ctx.message.server
            channel = ctx.message.channel
            frole = role.lower().strip()
            roles_ = [i.lower() for i in self.selfroles]
            sroles = {}
            for i in server.roles:
                x = i.name.lower()
                for role in roles_:
                    if x == role:
                        sroles[x] = i
            for r in sroles:
                if r.startswith(frole):
                    frole = sroles[r]
                    break
            if frole is not None:            
                if frole not in user.roles:
                    await self.bot.add_roles(user,frole)
                    await self.bot.say('You now have the **{}** role.'.format(frole.name))
                else:
                    await self.bot.remove_roles(user,frole)
                    await self.bot.say('Removed the **{}** role.'.format(frole.name)) 
            else:
                await self.bot.say('I cant find that role.')

    @self_.command(pass_context=True)
    async def roles(self,ctx):
        """Current list of allowable selfroles."""
        await self.bot.say('Current list of self roles: {}'.format(', '.join(self.selfroles)))

        
    @commands.command(pass_context=True, aliases=['8ball'])
    async def ball8(self, ctx, *, msg: str):
        """Let the 8ball decide your fate."""
        answer = random.randint(0, 19)
        
        if answer < 10:
            color = 0x008000
        elif 10 <= answer < 15:
            color = 0xFFD700
        else:
            color = 0xFF0000
        em = discord.Embed(color=color)
        em.add_field(name='\u2753 Question', value=msg)
        em.add_field(name='\ud83c\udfb1 8ball', value=self.ball[answer], inline=False)
        await self.bot.send_message(ctx.message.channel, content=None, embed=em)
        await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        '''Returns the OAUTH invite linke'''
        await self.bot.say('**Invite Link:**\n<https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=470147287>'.format(self.bot.user.id))


    @commands.command(pass_context=True)
    async def afk(self,ctx,*,reason : str):
        user = ctx.message.author
        msg = ctx.message
        afk = open('cogs/utils/afk.json').read()
        afk = json.loads(afk)
        afk[user.id] = reason
        afk = json.dumps(afk)
        x = await self.bot.say('You are now afk: {}'.format(reason))
        with open('cogs/utils/afk.json', 'w') as f:
            f.write(afk)
        await asyncio.sleep(5)
        await self.bot.delete_messages([x,msg])


    async def on_message(self,message):
        user = message.author
        channel = message.channel
        afk = open('cogs/utils/afk.json').read()
        afk = json.loads(afk)
        if user.id in afk:
            del afk[user.id]
            x = await self.bot.send_message(channel, 'You are now back from being afk.')
        else:
            mentions = message.mentions
            for member in mentions:
                if member.id in afk:
                    y = await self.bot.send_message(channel, '**{}** is afk: *{}*'.format(member.name, afk[member.id]))
        afk = json.dumps(afk)
        with open('cogs/utils/afk.json','w') as f:
            f.write(afk)




    @commands.command(pass_context=True)
    async def guess(self,ctx):
        def is_me(msg):
            return msg.author != self.bot.user and m.content.isdigit()
        await self.bot.say
        guess = await client.wait_for_message(timeout=5.0, check=is_me)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

             







    
def setup(bot):
    bot.add_cog(Misc(bot))
