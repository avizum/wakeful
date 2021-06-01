import discord, os, datetime, json, asyncio, aiohttp, pwd, asyncpg
from discord.ext import commands, tasks
from colorama import Fore
from discord.flags import Intents
from utils.configs import color
from utils.checks import is_blacklisted, is_mod

async def get_prefix(bot, message):
    await bot.wait_until_ready()
    if message.guild is None:
        return "!"
    else:
        try:
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return prefix["prefix"]
        except:
            await bot.db.execute("INSERT INTO prefixes(guild, prefix) VALUES($1, $2)", message.guild.id, 'w,')
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return prefix["prefix"]

with open('config.json') as f:
    conf = json.load(f)

devprefix = conf["DEVPREFIX"] # the prefix for the development version

if pwd.getpwuid(os.getuid())[0] == "pi":
    bot = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
else:
    bot = commands.AutoShardedBot(command_prefix=devprefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
bot.remove_command("help")

bot.uptime = datetime.datetime.utcnow()
token = conf["TOKEN"]
devtoken = conf["DEVTOKEN"]
bot.github = "https://github.com/pvffyn/wakeful" # the github the bot is hosted on
bot.suggestions = conf["SUGGESTIONS"] # this will be used as a webhook for suggestions
bot.greenTick="✓"
bot.redTick="x"
bot.error="!"
bot.cmdsSinceRestart = 0
bot.message_cache = {}
bot.afks = {}
bot.session = aiohttp.ClientSession()
bot.status = None
bot.guild = int(conf["GUILD"]) # your bots support server
bot.mod_role = int(conf["MODROLE"]) # moderator role on your bots support server
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

@tasks.loop(seconds=10)
async def presence():
    await asyncio.sleep(2)
    if bot.status == None:
        await bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(bot.guilds)} guilds & {len(bot.users)} users"))
    else:
        pass

@bot.event
async def on_message(msg):
    if pwd.getpwuid(os.getuid())[0] == "pi":
        prefix = await get_prefix(bot, msg)
    else:
        prefix = devprefix

    if msg.author.bot:
        return

    if await is_blacklisted(bot, msg.author):
        return

    elif msg.content.startswith(prefix):
        command = msg.content.split(prefix)
        command = command[1]
        res = await bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
        try:
            commands = res["commands"]
        except:
            success = False
        else:
            success = True
        if success:
            commands = commands.split(",")
            if command in commands and command != "":
                em=discord.Embed(description=f"this command has been disabled by the server administrators", color=color())
                await msg.channel.send(embed=em)
                return
            else:
                pass
        else:
            pass
        await bot.process_commands(msg)

    elif pwd.getpwuid(os.getuid())[0] == "pi":
        if msg.content.startswith(prefix):
            await bot.process_commands(msg)
        elif msg.content == f"<@!{bot.user.id}>" or msg.content == f"<@{bot.user.id}>":
            if msg.guild:
                em=discord.Embed(description=f"the prefix for `{msg.guild.name}` is `{prefix}`", color=color())
                await msg.channel.send(embed=em)
            else:
                em=discord.Embed(description=f"the prefix for dms is `{prefix}`", color=color())
                await msg.channel.send(embed=em)

    elif msg.content == f"<@!{bot.user.id}>" or msg.content == f"<@{bot.user.id}>":
        if is_mod(bot, msg.author):
            em=discord.Embed(description=f"my prefix is `{devprefix}`", color=color())
            await msg.channel.send(embed=em)

    elif msg.content.startswith(devprefix):
        if is_mod(bot, msg.author):
            await bot.process_commands(msg)

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{Fore.GREEN}cogs.{filename[:-3]} has been succesfully loaded{Fore.RESET}")
        except Exception as exc:
            print(f"{Fore.RED}An error occured while loading cogs.{filename[:-3]}{Fore.RESET}")
            raise exc

bot.load_extension("jishaku")
presence.start()
bot.db=bot.loop.run_until_complete(asyncpg.create_pool(host="localhost", port="5432", user=conf["dbuser"], password=conf["dbpw"], database="wakeful"))
if pwd.getpwuid(os.getuid())[0] == "pi": # check if username is pi
    bot.run(token) # run stable
else:
    bot.run(devtoken) # run development version