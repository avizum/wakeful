import discord
import os
import datetime
import json
import aiohttp
import pwd
import asyncpg
import logging
import coloredlogs
import discordTogether
from discord.ext import commands, tasks
from colorama import Fore
from utils import menus
from utils.context import SusContext
from utils.checks import is_blacklisted, is_mod

with open('config.json') as f:
    conf = json.load(f)


async def get_prefix(bot: "Wakeful", message: discord.Message):
    await bot.wait_until_ready()

    if message.author.id == bot.ownersid and bot.emptyPrefix is True:
        return commands.when_mentioned_or("")(bot, message)

    if message.guild is None:
        return commands.when_mentioned_or("!")(bot, message)
    else:
        try:
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return commands.when_mentioned_or(prefix["prefix"])(bot, message)
        except Exception:
            if pwd.getpwuid(os.getuid())[0] != "pi":
                await bot.db.execute("INSERT INTO prefixes(guild, prefix) VALUES($1, $2)", message.guild.id, ',w')
            else:
                await bot.db.execute("INSERT INTO prefixes(guild, prefix) VALUES($1, $2)", message.guild.id, 'w,')
            prefix = await bot.db.fetchrow("SELECT prefix FROM prefixes WHERE guild = $1", message.guild.id)
            return commands.when_mentioned_or(prefix["prefix"])(bot, message)


class Wakeful(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uptime = datetime.datetime.utcnow()
        self.github = "https://github.com/jottew/wakeful"  # the github the bot is hosted on
        self.invite = "https://discord.gg/RkCqvMJsDY"
        self.icons = conf["ICONS"]
        with open('config.json') as f:
            self.config = json.load(f)
        self.color = int(conf["COLOR"], 16)
        self.together = discordTogether.DiscordTogether(self)
        self.cmdsSinceRestart = 0
        self.message_cache = {}
        self.directorys = []
        self.command_usage = {}
        self.roos = []
        self.games = {
            "akinator": {}
        }
        self.maintainance = False
        self.emptyPrefix = False
        self.cmdsSinceRestart = 0
        self.ownersid = 797044260196319282
        self.afks = {}
        # self.banner = "https://media.discordapp.net/attachments/832746281335783426/849721738987307008/banner.png"
        self.session = aiohttp.ClientSession()
        self.status = None
        self.guild = int(conf["GUILD"])
        self.mod_role = int(conf["MODROLE"])

    def paginate(self, paginator):
        return menus.MenuPages(paginator)

    async def get_context(self, message, *, cls=SusContext):
        return await super().get_context(message, cls=cls)

    class roo():

        def __init__(self, bot):
            self.bot = bot

        def getEmoji(self, name: str):
            try:
                return self.bot.roos[name.lower()]
            except KeyError:
                return "didnt found find :anguished::anguished::anguished::anguished::anguished:"

        def __getattr__(self, attr):
            async def predicate():
                return self.getEmoji(attr)
            return predicate

    async def on_ready(self):
        logger.info(f"Logged in as: {bot.user} ({bot.user.id})")

        bot.roos = {em.name.lower().strip("roo"): str(em) for em in bot.emojis if em.name.lower().startswith("roo")}

    async def on_message(self, msg):
        if self.emptyPrefix and msg.author.id == self.ownersid:
            await self.process_commands(msg)
            return

        if pwd.getpwuid(os.getuid())[0] != "pi" and not is_mod(self, msg.author):
            return

        prefix = await get_prefix(self, msg)

        if msg.guild is None and msg.content.startswith(prefix):
            return await msg.channel.send(f"DM commands are disabled, please invite me to a guild\nInvite: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=self\nSupport Server: {self.invite}")

        if msg.author.bot:
            return

        if await is_blacklisted(self, msg.author):
            return

        for i in prefix:
            if msg.content.startswith(i):
                if self.maintainance is True and not is_mod(self, msg.author):
                    return await msg.reply("This bot is currently under maintainance, please wait", mention_author=False)
                if msg.guild is not None:
                    try:
                        command = msg.content.split(i)
                    except ValueError:
                        command = msg.content
                    command = command[1]

                    res = await self.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
                    try:
                        commands = res["commands"]
                    except (KeyError, TypeError):
                        success = False
                    else:
                        success = True

                    if success:
                        command_obj = self.get_command(command)
                        try:
                            self.get_command(command).parent
                        except AttributeError:
                            command_name = None
                        else:
                            command_name = "".join(command_obj.name if command_obj.parent is None else f"{command_obj.parent.name} {command_obj.name}")
                        commands = commands.split(",")
                        if (
                            command_name in commands
                            and command != ""
                            and not is_mod(self, msg.author)
                        ):
                            em = discord.Embed(description="This command has been disabled by the server administrators", color=self.color)
                            return await msg.channel.send(embed=em)
                await self.process_commands(msg)
                return

            if msg.content in [f"<@!{self.user.id}>", f"<@{self.user.id}>"]:
                if msg.guild:
                    em = discord.Embed(description=f"The prefix for `{msg.guild.name}` is `{prefix[2]}`", color=self.color)
                else:
                    em = discord.Embed(description=f"The prefix for dms is `{prefix[2]}`", color=self.color)

                return await msg.channel.send(embed=em)


bot = Wakeful(command_prefix=get_prefix, case_insensitive=True, ShardCount=10, intents=discord.Intents.all())
bot.remove_command("help")

token = conf["TOKEN"]
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

coloredlogs.install()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="data/logs/discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@tasks.loop(seconds=10)
async def presence():
    await bot.wait_until_ready()
    if bot.status is None:
        await bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(bot.guilds)} guilds & {len(bot.users)} users"))

@tasks.loop(seconds=10)
async def update_config():
    with open('config.json') as f:
        conf = json.load(f)
    bot.config = conf

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            logger.info(f"{Fore.GREEN}cogs.{filename[:-3]} has been succesfully loaded{Fore.RESET}")
        except Exception as exc:
            logger.info(f"{Fore.RED}An error occured while loading cogs.{filename[:-3]}{Fore.RESET}")
            raise exc

bot.config = conf
bot.load_extension("jishaku")
presence.start()
update_config.start()
bot.db = bot.loop.run_until_complete(asyncpg.create_pool(host="localhost", port="5432", user=conf["dbuser"], password=conf["dbpw"], database="wakeful"))

if __name__ == "__main__":
    bot.run(token)  # run stable
