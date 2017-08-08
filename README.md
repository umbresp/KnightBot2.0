# KnightBot 2.0

#### *Moderation, Fun, Utility, and much more to come!*

<img src='https://img.shields.io/badge/build-passing-brightgreen.svg'> [<img src="https://img.shields.io/badge/discord-py-orange.svg">](https://github.com/Rapptz/discord.py) [<img src='https://img.shields.io/badge/python-3.5-brightgreen.svg'>](https://python.org)

[<img src="https://discordapp.com/api/guilds/299358597803147264/widget.png?style=banner2">](https://discord.gg/cqgY2XZ) 

For those of you who don't know the sad, sad story of KnightBot, he was a rogue Knight who stumbled onto Discord just as verix was getting ready to make a bot with discord.py. However, KnightBot was scrapped in favor of SpikeBot, the cute little cactus from the rival game which would soon result in Clash Royale's demise. Now he's back... and he's looking for revenge!
#### TL; DR: nothing important. Keep reading.

If you want the bot, you can either invite the official version at https://bot.discord.io/kbot or clone your own instance.
If you want to clone your own instance, read on.

## For Pros: (Short version)
Clone this repository. Make sure you have python 3.5.x and pip installed. Install BeautifulSoup4, discord.py, requests, and PythonGists with pip. Go into \cogs\utils\t_config.json, and change the value of token to your bot's token and the value of opened to 1. Now run bot.py. 

## For Noobs: (Long version)
Install Python. KnightBot needs the latest 3.5.x. Try to avoid 3.6 for the time being. You can get python at https://python.org
**Important note:** When installing, make sure to check the "Add to %PATH%" option. It will make your life so much easier. Trust me.

Clone this repository. If you need help with that, check this out: https://help.github.com/articles/cloning-a-repository/

Once that's done, run command prompt as administrator (you can see this option by right clicking the start button) and run the following commands:
```
pip install requests
pip install PythonGists
pip install discord.py
pip install BeautifulSoup4
```
Now, close the command prompt window. Head on over to the cogs folder, go into the utils folder, in the file t_config.json, and change the value of "token" to your bot's token. How do you get a bot token, you ask? Go to https://discordapp.com/developers/applications/me, click "New App", name it whatever you want your bot's name to be and change the avatar if you like, click "Create Bot User" and save your changes. Then, click "show token". Copy that value and put it in t_config.json. **Make sure the token is in quotes.**
Never, ever give somebody else your bot's token. If they get it, they are essentially the bot and can do anything with it.
Once that's all done, open bot.py.

## Commands
The default set of modules includes:
* Moderation commands
* Fun/Misc commands
* Utility commands
* Tagging of text
* Tournament submission system
* Clash Royale Stats commands
* Brawl Stars Stats commands

## Support Me
I'd really appreciate if you joined the server above. It's not a support server, but I love to hang out and chill there. Most of the time, if you need help, just tag me @Victini#7460 and if I'm not sleeping, I'll help you. Also, check out verix's SpikeBot: https://github.com/verixx/SpikeBot
