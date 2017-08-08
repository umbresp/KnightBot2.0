import discord
from ext.commands import Bot
from ext import commands
import datetime
import time
import random
from PythonGists import PythonGists
import json
from .utils import launcher
from __main__ import send_cmd_help


info = launcher.bot()
owner = info['owner']


class Info():


    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context = True, description = 'See the date and time a user joined the server',no_pm=True)
    async def joined(self,ctx, member : discord.Member = None):
        """Says when a member joined."""
        if member is None:
            member = ctx.message.author
        server = member.server
        date = str(member.joined_at)[:10]
        time = str(member.joined_at)[11:16]
        msg = '{0.mention} joined at {1}'.format(member,date)
        emb = discord.Embed(color=0x00ffff)
        emb.add_field(name='Date',value=date,inline=True)
        emb.add_field(name='Time',value=time,inline=True)
        await self.bot.send_message(server, embed=emb)
        
    @commands.command(pass_context=True,aliases=['s','serverinfo','si'])
    async def server(self, ctx):
        '''See information about the server.'''
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle or
                      m.status == discord.Status.dnd])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, icon_url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)
            print(data.to_dict())

        try:
            await self.bot.say(embed=data)
            print('test')
            
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

        
    @commands.command(pass_context=True,aliases=['ui','user'],description='See user-info of someone.')
    async def userinfo(self,ctx, user: discord.Member = None):
        '''See information about a user or yourself.'''
        server = ctx.message.server
        if user:
            pass
        else:
            user = ctx.message.author
        avi = user.avatar_url
        if avi:
            pass
        else:
            avi = user.default_avatar_url
        roles = sorted([x.name for x in user.roles if x.name != "@everyone"])
        if roles:
            roles = ', '.join(roles)
        else:
            roles = 'None'
        time = ctx.message.timestamp
        desc = '{0} is {1} right now.'.format(user.name,user.status)
        member_number = sorted(server.members,key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(colour=0x00fffff,description = desc,timestamp=time)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Member No.',value=str(member_number),inline = True)
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Roles', value=roles, inline=True)
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url='http://site-449644.mozfiles.com/files/449644/logo-1.png')
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True,aliases=['av','dp'])
    async def avatar(self,ctx, user: discord.Member = None):
        '''Returns ones avatar URL'''
        if user:
            pass
        else:
            user = ctx.message.author
        avi = user.avatar_url
        if avi:
            pass
        else:
            avi = user.default_avatar_url
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)

        em = discord.Embed(color=colour)
        em.set_image(url=avi)
        await self.bot.say(embed=em)

    def owner_only():
        return commands.check(lambda ctx: ctx.message.author == ctx.message.server.owner)

    def is_owner():
        return commands.check(lambda ctx: ctx.message.author.id == owner)

    @commands.command(pass_context=True)
    async def info(self, ctx, *, arg : str = None):
        with open('cogs/utils/t_config.json') as f:
            data = json.loads(f.read())
        if arg is None:
            uptime = (datetime.datetime.now() - self.bot.uptime)
            hours, rem = divmod(int(uptime.total_seconds()), 3600)
            minutes, seconds = divmod(rem, 60)
            days, hours = divmod(hours, 24)
            if days:
                time_ = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
            else:
                time_ = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
            servers = len(self.bot.servers)
            version = data['bot']['version']
            library = 'discord.py'
            creator = await self.bot.get_user_info(owner)
            users = 0
            for server in self.bot.servers:
                users += len(server.members)
            invite = '[bot.discord.io/kbot](https://bot.discord.io/kbot)'
            discord_ = '[discord.io/brawlstars](https://discord.gg/c9NUu2W)'
            github = '[verixx/spikebot](https://github.com/verixx/spikebot)'
            time = ctx.message.timestamp
            emb = discord.Embed(colour=0x00FFFF)
            emb.set_author(name='KnightBot', icon_url=self.bot.user.avatar_url)
            emb.add_field(name='Version',value=version)
            emb.add_field(name='Library',value=library)
            emb.add_field(name='Creator',value=creator)
            emb.add_field(name='Servers',value=servers)
            emb.add_field(name='Users',value=users)
            emb.add_field(name='Invite',value=invite)
            emb.add_field(name='Github',value=github)
            emb.add_field(name='Discord',value=discord_)
            emb.add_field(name='Uptime',value=time_)
            emb.set_footer(text="ID: {} | Powered by KnightBot (legacy)".format(self.bot.user.id))
            emb.set_thumbnail(url=self.bot.user.avatar_url)
            await self.bot.say(embed=emb)
        elif ctx.message.author.id == data['bot']['owner']:
            try:          
                v = arg.split('=')
                if v[0].lower().strip() == 'version':
                    version = v[1].strip()
                    data['bot']['version'] = str(version)
                    await self.bot.say('Set bot version to `{}`'.format(version))
                    with open('cogs/utils/t_config.json', "w") as f:
                        f.write(json.dumps(data, indent=4, sort_keys=True))
            except:
                await self.bot.say('Incorrect command passed.')



    @commands.group(pass_context=True)
    @is_owner()
    async def backup(self,ctx):
        """Backup raw data for storage"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @backup.command(pass_context=True)
    async def tags(self,ctx):
        tags = open('cogs/utils/tags.json').read()
        url = PythonGists.Gist(description='All current tags', content=str(tags), name='tags.txt')
        em = discord.Embed(description="[raw tags data]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)

    @backup.command(pass_context=True)
    async def config(self,ctx):
        cfg = open('cogs/utils/t_config.json').read()
        url = PythonGists.Gist(description='Raw Config Data', content=str(cfg), name='config.txt')
        em = discord.Embed(description="[raw config data]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)

    @backup.command(pass_context=True)
    async def levels(self,ctx):
        cfg = open('cogs/utils/levels.json').read()
        url = PythonGists.Gist(description='Player Level Data', content=str(cfg), name='levels.txt')
        em = discord.Embed(description="[Player Level Data]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)

    @backup.command(pass_context=True)
    async def decks(self,ctx):
        cfg = open('cogs/utils/decks.json').read()
        url = PythonGists.Gist(description='Player Decks', content=str(cfg), name='decks.txt')
        em = discord.Embed(description="[Deck configs]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)

    @backup.command(pass_context=True)
    async def registrations(self,ctx):
        cfg = open('cogs/utils/registrations.txt').read()
        url = PythonGists.Gist(description='Server Event Registrations', content=str(cfg), name='registrations.txt')
        em = discord.Embed(description="[Server Event Registrations]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)

    @backup.command(pass_context=True)
    async def stats(self,ctx):
        cfg = open('cogs/utils/stats.json').read()
        url = PythonGists.Gist(description='Stats data', content=str(cfg), name='stats.json')
        em = discord.Embed(description="[Stats Backup]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)






def setup(bot):
    bot.add_cog(Info(bot))