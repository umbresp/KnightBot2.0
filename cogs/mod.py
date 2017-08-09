import discord
import datetime
import time
from ext import commands
import asyncio
from .utils import launcher
import random

info = launcher.bot()
token = info['token']
owner = info['owner']

class Mod():
    def __init__(self, bot):
        self.bot = bot
        # This should work, haven't tested it because I don't have the bot
        self.kickmsgs = ["Done. That felt good.", 
                         "No, Mr. Bond. I expect you to die.", 
                         "Let's hope he's not back in 5 minutes.",
                         "Are you sure about that?",
                         "Enough chaos."]
        
        self.kickerrs = ["Something is wrong...", 
                         "It doesn't work!", 
                         "Goodbye- wait, he's still here!", 
                         "NEED. MORE. POWWWWWWAH"]
        # Actually for kick, ban, and softban ^
        # Unban messages
        self.unbanmsgs = ["Forgiveness is key.", "I wonder how much he's grown since then?", "Ahhhh. The old memories.",
                          "Really? I thought that'd never happen!"]
        self.unbanerrs = ["Something is wrong...", "It doesn't work!"]

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

    def server_cfg(self,ctx):
        server = ctx.message.server
        info = launcher.config()
        mod_log = self.bot.get_channel(info[server.id]['mod_log'])
        return mod_log

    async def modlog(self,ctx,Type,user,moderator,time,reason=None):
        channel = self.server_cfg(ctx)
        clr = 0
        red = ['Kick','Ban','Soft-Ban']
        orange = ['Warn','Mute']
        green = ['Unban']
        if Type in red:
            clr = 0xbb3f27
        elif Type in orange:
            clr = 0xaa8f22
        elif Type in green:
            clr = 0x24b32a
        avi = ''
        if Type == 'Unban':
            avi = None
            mem = await self.bot.get_user_info(user)
            embed = discord.Embed(colour=clr,timestamp=time)
            embed.add_field(name='User',value=mem)
            embed.add_field(name='Mod',value=moderator.mention)
            embed.add_field(name='Type',value=Type)
            embed.add_field(name='Reason',value=reason)
            embed.set_author(name='Mod-Log Entry: ')
            embed.set_footer(text='ID: '+user)
            await self.bot.send_message(channel,embed=embed)
        else:
            if user.avatar_url:
                avi = user.avatar_url
            else:
                avi = user.default_avatar_url

        embed = discord.Embed(colour=clr,timestamp=time)
        embed.add_field(name='User',value=user.mention)
        embed.add_field(name='Mod',value=moderator.mention)
        embed.add_field(name='Type',value=Type)
        embed.add_field(name='Reason',value=reason)
        embed.set_author(name='Mod-Log Entry: '+user.name,icon_url=avi)
        embed.set_footer(text=('ID: '+user.id))
        await self.bot.send_message(channel,embed=embed)


    @commands.command(pass_context=True)
    @commands.check(mod)
    async def kick(self,ctx, member : discord.Member,*,reason=None):
        '''Kick someone out of the server.'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            if not discord.utils.get(member.roles, name='Mod'):
                await self.bot.kick(member)
                await self.bot.say(random.choice(self.kickmsgs))
                await self.modlog(ctx,'Kick',member,mod,time,reason)
            else:
                await self.bot.say(random.choice(self.kickerrs))

        except discord.Forbidden:
            await self.bot.say(random.choice(self.kickerrs))


    @commands.command(pass_context=True)
    @commands.check(mod)
    async def ban(self,ctx, member : discord.Member,*,reason=None):
        '''Ban someone from the server'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            if not discord.utils.get(member.roles, name='Mod'):
                await self.bot.ban(member)
                await self.bot.say(random.choice(self.kickmsgs))
                await self.modlog(ctx,'Ban',member,mod,time,reason)
            else:
                await self.bot.say(random.choice(self.kickerrs))

        except discord.Forbidden:
            await self.bot.say(random.choice(self.kickerrs))

    @commands.command(pass_context=True)
    @commands.check(mod)
    async def softban(self,ctx, member : discord.Member,*,reason=None):
        '''Kick someone out and delete their messages.'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            if not discord.utils.get(member.roles, name='Mod'):
                await self.bot.ban(member)
                await self.bot.unban(member.server,member)
                await self.bot.say(random.choice(self.kickmsgs))
                await self.modlog(ctx,'Soft-Ban',member,mod,time,reason)
            else:
                await self.bot.say(random.choice(self.kickerrs))

        except discord.Forbidden:
            await self.bot.say(random.choice(self.kickerrs))

    @commands.command(pass_context=True)
    @commands.check(mod)
    async def unban(self,ctx,member : str,*,reason=None):
        '''Unban someone using their user ID.'''
        server = ctx.message.server
        mem = discord.Object(id=member)
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            await self.bot.unban(server, mem)
            await self.bot.say(random.choice(self.unbanmsgs))
            await self.modlog(ctx,'Unban',member,mod,time,reason)
        except discord.Forbidden:
            await self.bot.say("random.choice(self.unbanmsgs)")

    @commands.command(pass_context=True)
    @commands.check(mod)
    async def mute(self,ctx,member: discord.Member,*,reason=None):
        '''Mute or Unmute someone.'''
        server = ctx.message.server
        role = discord.utils.get(server.roles, name='Muted')
        mod = ctx.message.author
        time = ctx.message.timestamp
        if not discord.utils.get(member.roles, name='Mod'):
            if not discord.utils.get(member.roles, name='Muted'):
                try:
                    await self.bot.add_roles(member,role)
                    await self.bot.say('{0.mention} is now muted.'.format(member))
                    await self.modlog(ctx,'Mute',member,mod,time,reason)
                except discord.Forbidden:
                    await self.bot.say('I dont have the perms.')
            else:
                await self.bot.remove_roles(member,role)
                await self.bot.say('{0.mention} can now speak.'.format(member))
        else:
            await self.bot.say("You can't mute mods.")

    @commands.command(pass_context=True)
    @commands.check(mod)
    async def purge(self, ctx, number: int):
        '''Delete a specified amount of messages.'''

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        async for message in self.bot.logs_from(channel, limit=number+1):
            to_delete.append(message)
        x = await self.bot.send_message(channel,'Deleting messages.')
        x = await self.bot.edit_message(x,'Deleting messages..')
        x = await self.bot.edit_message(x,'Deleting messages...')
        await self.mass_purge(to_delete)
        x = await self.bot.edit_message(x,'Deleted {} messages.'.format(len(to_delete)-1))
        await asyncio.sleep(5)
        await self.bot.delete_message(x)

    async def mass_purge(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1.5)

    @commands.command(pass_context = True,no_pm = True)
    async def shutdown(self,ctx):
        if ctx.message.author == ctx.message.server.owner or ctx.message.author.id == owner:
            await self.bot.say("Shutting down...")
            await self.bot.logout()
        else:
            await self.bot.say("Cheeky boi! Don't do that!")

    @commands.command(pass_context = True,no_pm = True)
    async def msg(self,ctx,*,msg : str):
        server = ctx.message.server
        members_messaged = 0
        '''Message everyone in the server.'''
        if ctx.message.author == ctx.message.server.owner or ctx.message.author.id == owner:
            for member in server.members:
                try:
                    await self.bot.send_message(member, msg)
                    print(member)
                except:
                    print(member, "has DM's turned off")
                members_messaged += 1 # I know this works in java, not clear with python, just want to add 1 to members_messaged each time the loop is run            
            await self.bot.say("Done. " + members_messaged + " members were DMed. (Prepare to have some angry people on your heels...)")
        else:
            await self.bot.say('Server owner only.')

    @commands.command(pass_context = True,no_pm = True)
    async def msg2(self,ctx,*,msg : str):
        server = ctx.message.server
        members_messaged = 0
        '''Message everyone in the server.'''
        if ctx.message.author == ctx.message.server.owner or ctx.message.author.id == owner:
            for member in server.members:
                if len(member.roles) < 2:
                    try:
                        await self.bot.send_message(member, msg)
                        print(member)
                    except:
                        print(member, "has DM's turned off")
                    members_messaged += 1 # I know this works in java, not clear with python, just want to add 1 to members_messaged each time the loop is run            
            await self.bot.say("Done. " + members_messaged + " members were DMed. (Prepare to have some angry people on your heels...)")
        else:
            await self.bot.say('Server owner only.')



    @commands.command(pass_context=True)
    @commands.check(mod)
    async def warn(self,ctx, member : discord.Member=None,*,reason=None):
        '''Warn someone in the server.'''
        channel = self.server_cfg(ctx)
        mod = ctx.message.author
        time = ctx.message.timestamp
        avi = ''
        if member.avatar_url:
            avi = member.avatar_url
        else:
            avi = member.default_avatar_url
        if not discord.utils.get(member.roles, name='Mod'):
            await self.bot.send_message(member,'**You have been warned by {}:** *{}*'.format(mod.name,reason))
            await self.bot.say('{} has been warned.'.format(member.mention))            
            embed = discord.Embed(colour=0xaa8f22,timestamp=time)
            embed.add_field(name='User',value=member.mention)
            embed.add_field(name='Mod',value=mod.mention)
            embed.add_field(name='Warn',value=reason)
            embed.set_author(name='User Warn: '+member.name,icon_url=avi)
            embed.set_footer(text=('ID: '+member.id))
            await self.bot.send_message(channel,embed=embed)
        else:
            await self.bot.say("You can't warn mods dummy.") # Why can't you warn mods? What's wrong with that?


    @commands.command(pass_context=True)
    @commands.check(mod)
    async def clean(self, ctx):
        '''Clean up bot messages and command calls.'''

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        async for message in self.bot.logs_from(channel, limit=100):
            if message.author.bot:               
                to_delete.append(message)
            if message.content.startswith(ctx.prefix):
                to_delete.append(message)
        await self.mass_purge(to_delete)
        x = await self.bot.send_message(channel,'Deleted {} messages.'.format(len(to_delete)-1))
        await asyncio.sleep(5)
        await self.bot.delete_message(x)
           
    @commands.command(pass_context=True)
    @commands.check(mod)
    async def role(self,ctx, member: discord.Member,*,roles=None):
        '''Give a role or a list of roles to someone.'''
        roles = roles.split(',')
        roles = [role.lower().strip() for role in roles]        
        top = ctx.message.author.top_role
        server = ctx.message.server
        channel = ctx.message.channel
        sroles = {}
        to_assign = []
        for i in server.roles:
            x = i.name.lower()
            sroles[x] = i
        for role in roles:
            for key in sroles:
                if key.startswith(role):
                    assign = sroles[key]
                    to_assign.append(assign)
                    break
                else:
                    pass
        if to_assign:
            x = await self.bot.send_message(channel,'`Assigning Roles...`')
            msg = ''
            for role in to_assign:
                if top > role:
                    if role not in member.roles:
                        await self.bot.add_roles(member, role)
                        msg += ', `Added {}`'.format(role)
                        msg = msg.strip(', ')
                        x = await self.bot.edit_message(x,msg)
                    else:
                        await self.bot.remove_roles(member, role)
                        msg += ', `Removed {}`'.format(role)
                        msg = msg.strip(', ')
                        x = await self.bot.edit_message(x,msg)
                else:
                    await self.bot.say('You cant assign roles higher than yourself.')
        else:
            await self.bot.say('Cant find any roles.')
                        
                    
        
        


def setup(bot):
    bot.add_cog(Mod(bot))
