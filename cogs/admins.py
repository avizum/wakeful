import discord, json, asyncio, importlib
from discord.ext import commands
from utils.configs import color
from utils.checks import is_mod
from prettytable import PrettyTable

status_types = {
    "dnd": discord.Status.dnd,
    "online": discord.Status.online,
    "invis": discord.Status.offline,
    "invisible": discord.Status.offline,
    "offline": discord.Status.offline,
    "sleep": discord.Status.idle,
    "sleeping": discord.Status.idle,
    "idle": discord.Status.idle
}

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blacklist(self, ctx):
        pass

    @blacklist.command()
    async def add(self, ctx, user : discord.User):
        if is_mod(self.bot, ctx.author):
            await self.bot.db.fetch("INSERT INTO blacklist (user_id) VALUES ($1)", user.id)
            em=discord.Embed(description=f"successfully blacklisted {user.mention}", color=color())
            await ctx.send(embed=em)

    @blacklist.command()
    async def remove(self, ctx, user : discord.User):
        if is_mod(self.bot, ctx.author):
            await self.bot.db.fetch("DELETE FROM blacklist WHERE user_id = $1", user.id)
            em=discord.Embed(description=f"successfully unblacklisted {user.mention}", color=color())
            await ctx.send(embed=em)

    @blacklist.command()
    async def check(self, ctx, user : discord.User):
        if is_mod(self.bot, ctx.author):
            try:
                thing = await self.bot.db.fetchrow("SELECT * FROM blacklist WHERE user_id = $1", user.id)
                thing["user_id"]
            except TypeError:
                em=discord.Embed(description=f"{user.mention} isn't blacklisted", color=color())
                await ctx.send(embed=em)
            else:
                em=discord.Embed(description=f"{user.mention} is blacklisted", color=color())
                await ctx.send(embed=em)

    @commands.group(invoke_without_command=True, name="setstatus", aliases=["setrp", "setrichpresence", "setactivity"])
    async def status(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command.name})

    @status.command()
    async def streaming(self, ctx, url, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Streaming(name=str(game), url=f'https://www.twitch.tv/{url.lower()}'))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command()
    async def playing(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Game(name=game))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command()
    async def watching(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=3))
            await ctx.message.add_reaction("✅")

    @status.command()
    async def listening(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=2))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command()
    async def competing(self, ctx, *, game):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Activity(name=f"{game}", type=5))
            await ctx.message.add_reaction("✅")
            self.bot.status = ""

    @status.command(aliases=["default", "original"])
    async def reset(self, ctx):
        if is_mod(self.bot, ctx.author):
            await self.bot.change_presence(activity=discord.Game(f"@wakeful for prefix | {len(self.bot.guilds)} guilds & {len(self.bot.users)} users"))
            self.bot.status = None
            await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        proc = await asyncio.create_subprocess_shell("git pull", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stdout:
            shell = stdout.decode()
        if stderr:
            shell = stderr.decode()
        em=discord.Embed(description=f"```sh\n{shell}```", color=color())
        await ctx.send(embed=em)
        await self.bot.close() # close the bot, so systemd will start it right back up

    @commands.command()
    @commands.is_owner()
    async def sql(self, ctx, *, query):
        res = await self.bot.db.fetch(query)
        if len(res) == 0:
            await ctx.message.add_reaction('✅')
        else:
            headers = list(res[0].keys())
            table = PrettyTable()
            table.field_names = headers
            for rec in res:
                lst = list(rec)
                table.add_row(lst)
            msg = table.get_string()
            await ctx.send(f"```\n{msg}\n```")

def setup(bot):
    bot.add_cog(admin(bot))