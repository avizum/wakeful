import discord, datetime, async_cse, psutil, humanize, os, sys, inspect, mystbin, googletrans, asyncio, aiohttp, random, time, asyncdagpi, hashlib, asyncpg, io, base64, typing, gdshortener, pathlib, textwrap, async_tio
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from utils.configs import color
from utils.get import *
from utils.checks import *
from jishaku.codeblocks import codeblock_converter
from utils.functions import * 
from jishaku.functools import executor_function
import idevision

@executor_function
def do_translate(output, text):
    """
    You have to install googletrans==3.1.0a0 for it to work, as the dev somehow broke it and it doesn't work else
    """
    translator = googletrans.Translator()
    translation = translator.translate(str(text), dest=str(output))
    return translation

google = async_cse.Search(get_config("GOOGLE"))
mystbinn = mystbin.Client()
dagpi = asyncdagpi.Client(get_config("DAGPI"))
idevisionn = idevision.async_client(get_config("IDEVISION"))
isgd = gdshortener.ISGDShortener()

class Utility(commands.Cog):

    """Useful commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mem=[]
        if message.guild:
            for m in message.guild.members:
                if not m.bot:
                    mem.append(m)
            if "@someone" in message.content:
                if message.author.guild_permissions.mention_everyone:
                    await message.channel.send(random.choice(mem).mention)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id in list(self.bot.afks):
            self.bot.afks.pop(msg.author.id)
            em=discord.Embed(description=f"Welcome back, {msg.author.mention}, I've unmarked you as afk", color=color(), timestamp=datetime.datetime.utcnow())
            await msg.channel.send(embed=em)
        for user in list(self.bot.afks):
            data = self.bot.afks[user]
            obj = self.bot.get_user(user)
            if f"<@!{user}>" in msg.content or f"<@{user}>" in msg.content:
                if data["reason"] is None:
                    mseg = f"Hey! {obj.name} is currently marked as afk"
                else:
                    mseg = f"Hey! {obj.name} is currently marked as afk for `{data['reason']}`"
                await msg.channel.reply(embed=em, mention_author=False)


    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if ";;" in msg.content:
            emojis = msg.content.split(";;")
            emoji_ = emojis[1]
            if emoji_ != "" and not " " in emoji_:
                res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", msg.guild.id)
                try:
                    res["commands"]
                except TypeError:
                    pass
                else:
                    commands = res["commands"]
                    commands = commands.split(",")
                    if len(commands) != 0 and commands != ['']:
                        if "emojis" in commands:
                            return
                        else:
                            pass
                    else:
                        pass
                res = await self.bot.db.fetchrow("SELECT user_id FROM emojis WHERE user_id = $1", msg.author.id)
                try:
                    res["user_id"]
                except TypeError:
                    return
                else:
                    emoji = None
                    for e in self.bot.emojis:
                        if e.name.lower().startswith(emoji_.lower()):
                            emoji = e
                    if emoji is not None:
                        await msg.reply(str(emoji), mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emojiinfo(self, ctx, emoji: typing.Union[discord.PartialEmoji, discord.Emoji, str]):
        if isinstance(emoji, discord.PartialEmoji):
            em=discord.Embed(title=emoji.name, color=color(), timestamp=datetime.datetime.utcnow())
            em.add_field(
                name="Created At",
                value=f"{emoji.created_at.strftime('%d/%m/20%y at %H:%M:%S')} ({humanize.naturaltime(emoji.created_at)})",
                inline=True
            )
            em.add_field(
                name="Animated?",
                value="".join(self.bot.icons['greentick'] if emoji.animated == True else self.bot.icons['redtick']),
                inline=True
            )
            em.set_thumbnail(url=str(emoji.url)+"?size=1024")
            em.set_footer(text=f"ID: {emoji.id} • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(emoji, discord.Emoji):
            em=discord.Embed(title=emoji.name, color=color(), timestamp=datetime.datetime.utcnow())
            em.add_field(
                name="Guild",
                value=f"""
{self.bot.icons['arrow']}Name: {emoji.guild.name}
> {emoji.guild.description}

{self.bot.icons['arrow']}Created At: {emoji.guild.created_at.strftime('%d/%m/20%y at %H:%M:%S')} ({humanize.naturaltime(emoji.guild.created_at)})
{self.bot.icons['arrow']}Verification Level: {str(emoji.guild.verification_level).title()}
""", inline=True
            )
            em.add_field(
                name="Created At",
                value=f"{emoji.created_at.strftime('%d/%m/20%y at %H:%M:%S')} ({humanize.naturaltime(emoji.created_at)})",
                inline=True
            )
            em.add_field(
                name="Animated?",
                value="".join(self.bot.icons['greentick'] if emoji.animated == True else self.bot.icons['redtick']),
                inline=True
            )
            em.set_thumbnail(url=str(emoji.url)+"?size=1024")
            em.set_footer(text=f"ID: {emoji.id} • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        elif isinstance(emoji, str):
            await ctx.message.add_reaction(self.bot.icons['redtick'])
            em=discord.Embed(description=f"This command does not support default emojis, please input a custom emoji", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)


    @commands.command(aliases=["shorten"])
    @commands.cooldown(1,10, commands.BucketType.user)
    async def shortener(self, ctx, url, custom_url = None):
        async with ctx.typing():
            if custom_url is None:
                res = list(isgd.shorten(url=url))[0]
            else:
                res = list(isgd.shorten(url=url, custom_url=custom_url))[0]
        em=discord.Embed(description=f"Here's your [shortened url]({res})", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url="https://support.rebrandly.com/hc/article_attachments/360020801793/rebrandly_url_shortener_010.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True, aliases=["emoji"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def emojis(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command": ctx.command})

    @emojis.command(aliases=["opt-in"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def optin(self, ctx):
        try:
            await self.bot.db.execute("INSERT INTO emojis (user_id) VALUES ($1)", ctx.author.id)
        except asyncpg.UniqueViolationError:
            em=discord.Embed(description=f"You've already opted into the emojis program", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"Alright! I've successfully opted you into the emojis program", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @emojis.command(aliases=["opt-out"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def optout(self, ctx):
        res = await self.bot.db.fetchrow("SELECT user_id FROM emojis WHERE user_id = $1", ctx.author.id)
        try:
            res["user_id"]
        except TypeError:
            em=discord.Embed(description=f"You aren't opted into the emojis program", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"Alright! I've successfully opted you out of the emojis program", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="sha256")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _sha(self, ctx, *, message):
        res = hashlib.sha256(message.encode()).hexdigest()
        await ctx.reply(res, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pypi(self, ctx, package):
        try:
            res = await self.bot.session.get(f"https://pypi.org/pypi/{package}/json")
            json = await res.json()
            name = json["info"]["name"] + " " + json["info"]["version"]
            author = json["info"]["author"] or "None"
            author_email = json["info"]["author_email"] or "None"
            url = json["info"]["project_url"] or "None"
            description = json["info"]["summary"] or "None"
            author = json["info"]["author"] or "None"
            license_ = json["info"]["license"] or "None"
            try:
                documentation = json["info"]["project_urls"]["Documentation"] or "None"
            except:
                documentation = "None"
            try:
                website = json["info"]["project_urls"]["Homepage"] or "None"
            except:
                website = "None"
            keywords = json["info"]["keywords"] or "None"
            em=discord.Embed(
                title=name,
                description=f"""
{description}
{self.bot.icons['arrow']}**Author**: {author}
{self.bot.icons['arrow']}**Author Email**: {author_email}

{self.bot.icons['arrow']}**Website**: {website}
{self.bot.icons['arrow']}**Documentation**: {documentation}
{self.bot.icons['arrow']}**Keywords**: {keywords}
{self.bot.icons['arrow']}**License**: {license_}""",
                url=url,
                color=color()
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/381963689470984203/814267252437942272/pypi.png")
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        except aiohttp.ContentTypeError:
            em=discord.Embed(description=f"This package wasn't found", color=color(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["g"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, term):
        async with ctx.typing():
            if ctx.channel.is_nsfw():
                safe_search_setting=False
                safe_search="Disabled"
            else:
                safe_search_setting=True
                safe_search="Enabled"
            value=0
            results = await google.search(str(term), safesearch=safe_search_setting)
            image = None
            for res in results:
                if res.image_url.endswith("png") or res.image_url.endswith("jpg") or res.image_url.endswith("jpeg") or res.image_url.endswith("webp"):
                    image = res.image_url
            em=discord.Embed(
                title=f"Results for: `{term}`",
                timestamp=datetime.datetime.utcnow(),
                color=color()
            )
            em.set_footer(text=f"Requested by {ctx.author} • Safe-Search: {safe_search}", icon_url=ctx.author.avatar_url)
            if image is not None:
                em.set_thumbnail(url=image)
            for result in results:
                if not value > 4:
                    epic = results[int(value)]
                    em.add_field(
                        name=f" \uFEFF",
                        value=f"**[{str(epic.title)}]({str(epic.url)})**\n{str(epic.description)}\n",
                        inline=False
                    )
                    value+=1
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["gimage"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def googleimage(self, ctx, *, query):
        if ctx.channel.is_nsfw():
            safe_search_setting=False
            safe_search="Disabled"
        else:
            safe_search_setting=True
            safe_search="Enabled"
        async with ctx.typing():
            results = await google.search(query, safesearch=safe_search_setting)
            image = None
            for res in results:
                if res.image_url.endswith("png") or res.image_url.endswith("jpg") or res.image_url.endswith("jpeg") or res.image_url.endswith("webp"):
                    image = res
        if image is not None:
            em=discord.Embed(title=f"Results for: `{query}`", description=f"[{image.title}]({image.url})", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author} • Safe-Search: {safe_search}", icon_url=ctx.author.avatar_url)
            em.set_image(url=image.image_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find any images with the query `{query}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["trans", "tr"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, output : str, *, text : str):
        async with ctx.typing():
            translation = await do_translate(output, text)
            em = discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.add_field(name=f"Input [{translation.src.upper()}]", value=f"```{text}```", inline=True)
            em.add_field(name=f"Output [{translation.dest.upper()}]", value=f"```{translation.text}```", inline=True)
            em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/d/db/Google_Translate_Icon.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def commits(self, ctx):
        github = self.bot.github.replace("https://github.com/", "").split("/")
        username = github[0]
        repo = github[1]
        res = await self.bot.session.get(f"https://api.github.com/repos/{username}/{repo}/commits")
        res = await res.json()
        em = discord.Embed(title=f"Commits", description="\n".join(f"[`{commit['sha'][:6]}`]({commit['html_url']}) {commit['commit']['message']}" for commit in res[:5]), url=self.bot.github+"/commits", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url="https://image.flaticon.com/icons/png/512%2F25%2F25231.png")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["guildav", "servericon", "serverav", "sav", "srvav"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serveravatar(self, ctx, member : discord.Member = None):
        async with ctx.typing():
            avatar_png = ctx.guild.icon_url_as(format="png")
            avatar_jpg = ctx.guild.icon_url_as(format="jpg")
            avatar_jpeg = ctx.guild.icon_url_as(format="jpeg")
            avatar_webp = ctx.guild.icon_url_as(format="webp")
            if ctx.guild.is_icon_animated():
                avatar_gif = ctx.guild.icon_url_as(format="gif")
            if ctx.guild.is_icon_animated():
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp}) | [gif]({avatar_gif})", color=color(), timestamp=datetime.datetime.utcnow())
            else:
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp})", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=ctx.guild.icon_url)
            em.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["si", "guildinfo", "gi"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx):
        if ctx.guild.description is None:
            description=""
        else:
            description = ctx.guild.description
        
        bots = online = dnd = idle = offline = 0
        for member in ctx.guild.members:
            if member.bot:
                bots+=1
            elif member.raw_status == "online":
                online += 1
            elif member.raw_status == "dnd":
                dnd += 1
            elif member.raw_status == "offline":
                offline += 1
            elif member.raw_status == "idle":
                idle += 1
        
        try:
            booster_role = ctx.guild.premium_subscriber_role.mention 
        except AttributeError:
            booster_role = "None"
        created_at = ctx.guild.created_at.strftime("%d/%m/20%y at %H:%M:%S")
        em=discord.Embed(title=ctx.guild.name, description=f"{description}", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_image(url=ctx.guild.banner_url)
        em.set_thumbnail(url=ctx.guild.icon_url)
        em.add_field(name="Members", value=f"""
{self.bot.icons['arrow']}Online: `{online}`
{self.bot.icons['arrow']}DND: `{dnd}`
{self.bot.icons['arrow']}Idle: `{idle}`
{self.bot.icons['arrow']}Offline: `{offline}`
{self.bot.icons['arrow']}Bots: `{bots}`""", inline=True)
        em.add_field(name="Boosts", value=f"""
{self.bot.icons['arrow']} Amount: `{ctx.guild.premium_subscription_count}`
{self.bot.icons['arrow']}Role: {booster_role}""",inline=True)
        em.add_field(name="Channels", value=f"""
{self.bot.icons['arrow']} All `{len(ctx.guild.channels)}`
{self.bot.icons['arrow']}Text: `{len(ctx.guild.text_channels)}`
{self.bot.icons['arrow']}Voice: `{len(ctx.guild.voice_channels)}`""", inline=True)
        em.add_field(name="Other", value=f"""
{self.bot.icons['arrow']} Owner: {ctx.guild.owner.mention}
{self.bot.icons['arrow']}Roles: `{len(ctx.guild.roles)}`
{self.bot.icons['arrow']}Region: `{ctx.guild.region}`
{self.bot.icons['arrow']}Created at: `{created_at}` ({humanize.naturaltime(ctx.guild.created_at)})""", inline=True)
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["ui", "whois"], description="A command to get information about the given member", usage="[@member]")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
            
        if "offline" != str(member.mobile_status):
            platform = "Mobile"
        elif "offline" != str(member.desktop_status):
            platform = "Desktop"
        elif "offline" != str(member.web_status):
            platform = "Web"
        else:
            platform = "None"

        created_at = member.created_at.strftime("%d/%m/20%y at %H:%M:%S")
        joined_at = member.joined_at.strftime("%d/%m/20%y at %H:%M:%S")

        if member.top_role.name == "@everyone":
            top_role="None"
        else:
            top_role=member.top_role.mention

        join_position = sum(member.joined_at > m.joined_at if m.joined_at is not None else "1" for m in ctx.guild.members)

        em=discord.Embed(title=str(member), color=color(), timestamp=datetime.datetime.utcnow())
        em.add_field(name="Info", value=f"""
{self.bot.icons['arrow']}Name: {member.name}
{self.bot.icons['arrow']}Nickname: {member.nick}
{self.bot.icons['arrow']}Status: {''.join(member.raw_status.title() if member.raw_status != "dnd" else "DND")}
{self.bot.icons['arrow']}Platform: `{platform}`
{self.bot.icons['arrow']}Created at: {created_at} ({humanize.naturaltime(member.created_at)})""", inline=True)
        em.add_field(name="Guild", value=f"""
{self.bot.icons['arrow']}Roles: {len(member.roles)}
{self.bot.icons['arrow']}Top Role: {top_role}
{self.bot.icons['arrow']}Join Position: {join_position}
{self.bot.icons['arrow']}Joined at: {joined_at} ({humanize.naturaltime(member.joined_at)})""", inline=True)
        em.set_footer(text=f"ID: {member.id} • {ctx.author}", icon_url=ctx.author.avatar_url)
        em.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def suggest(self, ctx):
        em=discord.Embed(description=f"Please now enter your suggestion below or type `cancel` to cancel", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.reply(embed=em, mention_author=False)
        try:
            suggestion = await self.bot.wait_for("message", check=lambda msg: msg.channel == ctx.channel and msg.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            em=discord.Embed(description="You took too long to respond, now ignoring next messages", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=em)
        else:
            if suggestion.content.lower() != "cancel":
                webhook = Webhook.from_url(str(get_config("SUGGESTIONS")), adapter=AsyncWebhookAdapter(self.bot.session))
                em=discord.Embed(description=f"```{suggestion.clean_content}```", color=color(), timestamp=datetime.datetime.utcnow())
                em.set_footer(text=f"Suggestion by {ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
                attachment = None
                if ctx.message.attachments:
                    attachment = ctx.message.attachments[0].url
                if attachment is not None:
                    em.set_image(url=attachment)
                await webhook.send(embed=em)
                await suggestion.add_reaction("✅")
                em=discord.Embed(description="Your suggestion has been sent to the admins\nNote: abuse may get you blacklisted", color=color(), timestamp=datetime.datetime.utcnow())
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await msg.edit(embed=em)
            else:
                await msg.delete()

    @commands.command(aliases=["gif"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def giphy(self, ctx, *, query : str):
        query = query.replace(" ", "%20")
        res = await self.bot.session.get(f"https://api.giphy.com/v1/gifs/search?api_key={get_config('GIPHY')}&q={query}&limit=50&offset=0&rating=g&lang=en")
        res = await res.json()
        if res["data"] != [] and len(res["data"]) != 0:
            res = random.choice(res["data"])
            image = res["images"]["original"]["url"]
            em=discord.Embed(title=res["title"], url=res["url"], color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=image)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find any results with the query `{query}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)


    @commands.command(aliases=["urban"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def urbandictionary(self, ctx, *, term):
        res = await self.bot.session.get("http://api.urbandictionary.com/v0/define", params={"term": term})
        res = await res.json()
        if res["list"] != [] and len(res["list"]) != 0:
            res = res["list"][0]
            definition = res["definition"].replace("[", "").replace("]", "")
            permalink = res["permalink"]
            upvotes = res["thumbs_up"]
            author = res["author"]
            example = res["example"].replace("[", "").replace("]", "")
            word = res["word"]
            em=discord.Embed(title=word, description=f"""
{self.bot.icons['arrow']}**Definition**:
{definition}
{self.bot.icons['arrow']}**Example**:
{example}""", url=permalink, color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"👍 {upvotes} • 👤 {author} • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I could not find any results for `{term}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["src"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def source(self, ctx, *, command_name : str = None):
        if command_name == None:
            em=discord.Embed(description=f"My source code can be found [here]({self.bot.github})", color=color(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=em, mention_author=False)
        else:
            command = self.bot.get_command(command_name)
            if not command:
                em=discord.Embed(description=f"Couldn't find command `{command_name}`", color=color(), timestamp=datetime.datetime.utcnow())
                await ctx.reply(embed=em, mention_author=False)
            else:
                try:
                    source_lines, _ = inspect.getsourcelines(command.callback)
                except (TypeError, OSError):
                    em=discord.Embed(description=f"Couldn't retrieve source for `{command_name}`", color=color(), timestamp=datetime.datetime.utcnow())
                    await ctx.reply(embed=em, mention_author=False)
                else:
                    source_lines = ''.join(source_lines).split('\n')
                    src = textwrap.dedent("\n".join(line for line in source_lines))
                    print(src)
                    await ctx.author.send(file=await getFile(src, "py"))
                    await ctx.message.add_reaction("✅")

    @commands.command(name="avatar", aliases=["icon", "av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _avatar(self, ctx, member : discord.Member = None):
        async with ctx.typing():
            if not member:
                member = ctx.author
            avatar_png = member.avatar_url_as(format="png")
            avatar_jpg = member.avatar_url_as(format="jpg")
            avatar_jpeg = member.avatar_url_as(format="jpeg")
            avatar_webp = member.avatar_url_as(format="webp")
            if member.is_avatar_animated():
                avatar_gif = member.avatar_url_as(format="gif")
            if member.is_avatar_animated():
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp}) | [gif]({avatar_gif})", color=color(), timestamp=datetime.datetime.utcnow())
            else:
                em=discord.Embed(description=f"[png]({avatar_png}) | [jpg]({avatar_jpg}) | [jpeg]({avatar_jpeg}) | [webp]({avatar_webp})", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=member.avatar_url)
            em.set_author(name=f"{member}", icon_url=member.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["lc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def lettercount(self, ctx, *, text):
        em=discord.Embed(description=f"Your text is {len(text)} letters long", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["wc"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wordcount(self, ctx, *, text):
        text_list = text.split(" ")
        em=discord.Embed(description=f"Your text is {len(text_list)} words long", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def invite(self, ctx):
        em=discord.Embed(description=f"Here's my [invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)", color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["botinfo", "about", "bi"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        operating_system=None
        if os.name == "nt":
            operating_system = "Windows"
        elif os.name == "posix":
            operating_system = "Linux"
        async with ctx.typing():
            process = psutil.Process()
            p = pathlib.Path('./')
            version = sys.version_info
            em = discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            # Uptime
            delta_uptime = datetime.datetime.utcnow() - self.bot.uptime
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            # File Stats
            files = classes = funcs = coroutines = comments = lines = 0
            for f in p.rglob("*.py"):
                files += 1
                with f.open() as of:
                    for line in of.readlines():
                        line = line.strip()
                        if line.startswith("class"):
                            classes += 1
                        if line.startswith("def"):
                            funcs += 1
                        if line.startswith("async def"):
                            coroutines += 1
                        if "#" in line:
                            comments += 1
                        lines += 1
            # Channels
            channels = 0
            for guild in self.bot.guilds:
                for channel in guild.channels:
                    channels += 1
            cogs = []
            # Disabled commands
            if ctx.guild is not None:
                disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                try:
                    disabled = disabled["commands"]
                except:
                    disabled = []
                else:
                    disabled = disabled.split(",")
            else:
                disabled = []
            # Cogs
            for cog in self.bot.cogs:
                cog = get_cog(self.bot, cog)
                if not cog.qualified_name.lower() in ["jishaku"]:
                    if is_mod(self.bot, ctx.author):
                        cmds = [cmd for cmd in cog.get_commands()]
                    else:
                        cmds = [cmd for cmd in cog.get_commands() if not cmd.hidden and not cmd.name in disabled]
                    if len(cmds) != 0 and cmds != []:
                        cogs.append(cog)
            # Embed
            owner = self.bot.get_user(self.bot.ownersid)
            em.add_field(name="System", value=f"""
{self.bot.icons['arrow']}**OS**: `{operating_system}`
{self.bot.icons['arrow']}**CPU**: `{process.cpu_percent()}`%
{self.bot.icons['arrow']}**Memory**: `{humanize.naturalsize(process.memory_full_info().rss)}`
{self.bot.icons['arrow']}**Process**: `{process.pid}`
{self.bot.icons['arrow']}**Threads**: `{process.num_threads()}`
{self.bot.icons['arrow']}**Language**: `Python`
{self.bot.icons['arrow']}**Python version**: `{version[0]}.{version[1]}.{version[2]}`
{self.bot.icons['arrow']}**discord.py version**: `{discord.__version__}`""", inline=False)
            em.add_field(name="Bot", value=f"""
{self.bot.icons['arrow']}**Guilds**: `{len(self.bot.guilds)}`
{self.bot.icons['arrow']}**Users**: `{len(self.bot.users)}`
{self.bot.icons['arrow']}**Channels**: `{channels}`:
{self.bot.icons['arrow']}**Shards**: `{len(list(self.bot.shards))}`
{self.bot.icons['arrow']}**Commands**: `{len([cmd for cmd in self.bot.commands if not cmd.hidden])}`
{self.bot.icons['arrow']}**Commands executed**: `{self.bot.cmdsSinceRestart}`
{self.bot.icons['arrow']}**Cogs**: `{len(cogs)}`
{self.bot.icons['arrow']}**Uptime**: `{days}d {hours}h {minutes}m {seconds}s`""", inline=False)
            em.add_field(name="File Statistics", value=f"""
{self.bot.icons['arrow']}**Files**: `{files}`
{self.bot.icons['arrow']}**Lines**: `{lines}`
{self.bot.icons['arrow']}**Functions**: `{funcs}`
{self.bot.icons['arrow']}**Coroutines**: `{coroutines}`
{self.bot.icons['arrow']}**Comments**: `{comments}`""", inline=False)
            em.add_field(name="Links", value=f"""
{self.bot.icons['arrow']}[Developer](https://discord.com/users/{owner.id})
{self.bot.icons['arrow']}[Source]({self.bot.github})
{self.bot.icons['arrow']}[Invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)""", inline=False)
            em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_footer(text=f"Made by {owner}", icon_url=owner.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def unspoiler(self, ctx, *, msg : str = None):
        if msg is None:
            if ctx.message.reference:
                text = ctx.message.reference.resolved.clean_content
        else:
            text = msg
        await ctx.reply(text.replace("|", ""), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
    
    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def spoiler(self, ctx, *, msg : str = None):
        if msg is None:
            if ctx.message.reference:
                text = ctx.message.reference.resolved.clean_content
        else:
            text = msg
        await ctx.reply("".join(f"||{letter}||" for letter in text), mention_author=False, allowed_mentions=discord.AllowedMentions.none())
    
    @commands.command(aliases=["rp", "activity", "richpresence", "status"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def presence(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        em=discord.Embed(title=f"{member.name}'s activities", color=color(), timestamp=datetime.datetime.utcnow())
        for activity in member.activities:
            if isinstance(activity, discord.activity.Spotify):
                artists = ", ".join(artist for artist in activity.artists)
                duration = activity.duration
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                em.add_field(
                    name="Spotify",
                    value=f"""
{self.bot.icons['arrow']}Title: `{activity.title}`
{self.bot.icons['arrow']}Artists: `{artists}`
{self.bot.icons['arrow']}Album: `{activity.album}`
{self.bot.icons['arrow']}Album Cover: [url]({activity.album_cover_url})
{self.bot.icons['arrow']}Duration: `{hours}`h `{minutes}`m `{seconds}`s
""",
                    inline=True
                )
            elif isinstance(activity, discord.activity.CustomActivity):
                if activity.emoji != None:
                    emoji = f"[url]({activity.emoji.url})"
                    emojiName = f"`{activity.emoji.name}`"
                else:
                    emoji = "`None`"
                    emojiName = "`None`"
                em.add_field(
                    name="Custom",
                    value=f"""
{self.bot.icons['arrow']}Text: `{activity.name}`
{self.bot.icons['arrow']}Emoji Name: {emojiName}
{self.bot.icons['arrow']}Emoji: {emoji}
""",
                    inline=True
                )
            elif isinstance(activity, discord.activity.Game):
                em.add_field(
                    name="Game",
                    value=f"{self.bot.icons['arrow']}Name: `{activity.name}`",
                    inline=True
                )
            elif isinstance(activity, discord.activity.Streaming):
                em.add_field(
                    name="Stream",
                    value=f"""
{self.bot.icons['arrow']}Title: `{activity.name}`
{self.bot.icons['arrow']}Platform: `{activity.platform}`
{self.bot.icons['arrow']}URL: [{activity.url.split("/")[3]}]({activity.url})
""", inline=True
                )
            else:
                try:
                    type = str(activity.type).lower().split("activitytype.")[1].title()
                except:
                    type = "None"
                em.add_field(
                    name="Unknown",
                    value=f"""
{self.bot.icons['arrow']}Name: `{activity.name}`
{self.bot.icons['arrow']}Details: `{activity.details}`
{self.bot.icons['arrow']}Emoji: `{activity.emoji}`
{self.bot.icons['arrow']}Type: `{type}`
""",
                    inline=True
                )
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.group(name="qr", invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _qr(self, ctx):
        await ctx.invoke(self.bot.get_command("help"), **{"command":ctx.command})

    @_qr.command(name="create", aliases=["make"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _create(self, ctx, *, text):
        text = text.replace(" " ,"%20")
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Powered by qrserver.com • {ctx.author}", icon_url=ctx.author.avatar_url)
        em.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?data={text}&size=200x200")
        await ctx.reply(embed=em, mention_author=False)

    @_qr.command(name="read", aliases=["show"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _read(self, ctx):
        if ctx.message.attachments:
            if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                attachment = ctx.message.attachments[0].url
            else:
                em=discord.Embed(description=f"Please attach a png, jpg, jpeg or webp file", color=color(), timestamp=datetime.datetime.utcnow())
                return await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"Please attach a png, jpg, jpeg or webp file", color=color(), timestamp=datetime.datetime.utcnow())
            return await ctx.reply(embed=em, mention_author=False)
        res = await self.bot.session.get(f"http://api.qrserver.com/v1/read-qr-code/?fileurl={attachment}")
        res = await res.json()
        res = res[0]["symbol"][0]
        if res["error"] is None:
            await ctx.reply(res["data"], mention_author=False, allowed_mentions=discord.AllowedMentions.none())
        else:
            em=discord.Embed(description=res["error"], color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["run", "tio"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def execute(self, ctx, language, *, code : codeblock_converter):
        tio= await async_tio.Tio()
        async with ctx.typing():
            res = await tio.execute(code.content, language=language)
            await tio.close()
        lang = "".join(code.language if code.language is not None else "txt")
        f = await getFile(res.output, lang, "output")
        await ctx.reply(file=f, mention_author=False, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(aliases=["fortnite", "fn", "fnstats"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def fortnitestats(self, ctx, username, *, platform):
        platforms = {
            "pc": "kbm",
            "computer": "kbm",
            "switch": "gamepad",
            "nintendo switch": "gamepad",
            "xbox": "gamepad",
            "xbox one": "gamepad",
            "playstation": "gamepad",
            "playstation 4": "gamepad",
            "ps":"gamepad",
            "ps4": "gamepad",
            "phone": "touch",
            "android": "touch",
            "iphone": "touch"
        }
        try:
            platformm = platforms[platform.lower()]
        except KeyError:
            em=discord.Embed(description=f"I couldn't find the platform `{platform}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            async with ctx.typing():
                res = await self.bot.session.get(f"https://api.fortnitetracker.com/v1/profile/{platformm}/{username}", headers={"TRN-Api-Key":get_config("FORTNITE")})
                res = await res.json()
            try:
                error = str(res["accountId"])
            except KeyError:
                em=discord.Embed(description=res["error"], color=color(), timestamp=datetime.datetime.utcnow())
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)
            else:
                accid = res["accountId"]
                avatar = res["avatar"]
                name = res["epicUserHandle"]
                recentMatches = res["recentMatches"]
                em=discord.Embed(title=name, color=color(), timestamp=datetime.datetime.utcnow())
                em.set_footer(text=f"ID: {accid} • Powered by fortnitetracker.com • {ctx.author}", icon_url=ctx.author.avatar_url)
                em.set_thumbnail(url=avatar)
                amount = len(recentMatches)
                if amount > 1:
                    amount = 1
                for x in range(amount):
                    match = recentMatches[x]
                    type_ = match["playlist"]
                    kills = match["kills"]
                    playTime = match["minutesPlayed"]
                    score = match["score"]
                    em.add_field(
                        name=f"Latest Match",
                        value=f"""
{self.bot.icons['arrow']}Game Type: `{type_.title()}`
{self.bot.icons['arrow']}Kills: `{kills}`
{self.bot.icons['arrow']}Play Time: `{playTime}` minutes
{self.bot.icons['arrow']}Score: `{score}`
""",
                        inline=True
                    )
                await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def snipe(self, ctx):
        try:
            msg = self.bot.message_cache[ctx.guild.id][ctx.channel.id]
        except KeyError:
            em=discord.Embed(description=f"There's no message to snipe", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"`{msg.content}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_author(name=f"{msg.author} ({msg.author.id})", icon_url=msg.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["ss"])
    @commands.is_nsfw()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def screenshot(self, ctx, website):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://api.screenshotmachine.com?key={get_config('SCREENSHOT')}&url={website}&dimension=1280x720&user-agent=Mozilla/5.0 (Windows NT 10.0; rv:80.0) Gecko/20100101 Firefox/80.0")
            res = io.BytesIO(await res.read())
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url="attachment://screenshot.jpg")
            em.set_footer(text=f"Powered by screenshotmachine.com • {ctx.author}", icon_url=ctx.author.avatar_url)
        msg = await ctx.reply(embed=em, file=discord.File(res, "screenshot.jpg"), mention_author=False)
        await msg.add_reaction("🚮")
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: str(reaction.emoji) == "🚮" and reaction.message == msg and not user.bot)
        await msg.delete()
        em=discord.Embed(description=f"The screenshot has been deleted by {user.mention}", color=color(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=em, mention_author=False)


    @commands.command()
    @commands.cooldown(1,5, commands.BucketType.user)
    async def disabled(self, ctx):
        res = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
        try:
            res["commands"]
        except TypeError:
            em=discord.Embed(description=f"There are no disabled commands", color=color(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=em, mention_author=False)
        else:
            commands = res["commands"]
            commands = commands.split(",")
            if len(commands) != 0 and commands != ['']:
                em=discord.Embed(title="Disabled commands", description=", ".join(cmd for cmd in commands if cmd != ""), color=color(), timestamp=datetime.datetime.utcnow())
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"There are no disabled commands", color=color(), timestamp=datetime.datetime.utcnow())
                await ctx.reply(embed=em, mention_author=False)

    @commands.group(aliases=["rtfd"], invoke_without_command=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def rtfm(self, ctx, query):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://idevision.net/api/public/rtfm?query={query}&location=https://discordpy.readthedocs.io/en/latest&show-labels=false&label-labels=false")
            res = await res.json()
            nodes = res["nodes"]
        if nodes != {}:
            em=discord.Embed(description="\n".join(f"[`{e}`]({nodes[e]})" for e in nodes), color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Powered by idevision.net • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"No results found for `{query}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @rtfm.command(aliases=["py"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def python(self, ctx, query):
        async with ctx.typing():
            res = await self.bot.session.get(f"https://idevision.net/api/public/rtfm?query={query}&location=https://docs.python.org/3&show-labels=false&label-labels=false")
            res = await res.json()
            nodes = res["nodes"]
        if nodes != {}:
            em=discord.Embed(description="\n".join(f"[`{e}`]({nodes[e]})" for e in nodes), color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Powered by idevision.net • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"No results found for `{query}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def weather(self, ctx, state):
        state = state.replace(" ", "%20")
        async with ctx.typing():
            location = await self.bot.session.get(f"https://www.metaweather.com/api/location/search/?query={state}")
            location = await location.json()
            try:
                woeid = location[0]["woeid"]
            except:
                em=discord.Embed(description=f"I couldn't retrieve the weather for `{state}`", color=color(), timestamp=datetime.datetime.utcnow())
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)
            else:
                results = await google.search(location[0]["title"], safesearch=True)
                image = None
                for res in results:
                    if res.image_url.endswith("png") or res.image_url.endswith("jpg") or res.image_url.endswith("jpeg") or res.image_url.endswith("webp"):
                        image = res.image_url
                res = await self.bot.session.get(f"https://www.metaweather.com/api/location/{woeid}")
                res = await res.json()
                res = res["consolidated_weather"][0]
                em=discord.Embed(title=location[0]["title"], description=f"""
{self.bot.icons['arrow']}Type: `{res["weather_state_name"]}`
{self.bot.icons['arrow']}Wind Direction: `{res["wind_direction_compass"]}`
{self.bot.icons['arrow']}Temperature: `{round(int(res["the_temp"]), 1)}`
{self.bot.icons['arrow']}Minimum Temperature: `{round(int(res["min_temp"]), 1)}`
{self.bot.icons['arrow']}Maximum Temperature: `{round(int(res["max_temp"]), 1)}`
{self.bot.icons['arrow']}Wind Speed: `{round(int(res["wind_speed"]), 1)}`
{self.bot.icons['arrow']}Air Pressure: `{round(int(res["air_pressure"]), 1)}`
{self.bot.icons['arrow']}Humidity: `{res["humidity"]}`
{self.bot.icons['arrow']}Visibility: `{round(int(res["visibility"]), 1)}`
""", color=color(), timestamp=datetime.datetime.utcnow())
                if image is not None:
                    em.set_thumbnail(url=image)
                em.set_footer(text=f"Powered by metaweather.com • {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["shard", "shards"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def shardinfo(self, ctx, shard : int = None):
        if shard is None:
            em=discord.Embed(title="Shards", color=color(), timestamp=datetime.datetime.utcnow())
            for shard in list(self.bot.shards):
                shard = dict(self.bot.shards)[shard]
                em.add_field(
                    name=f"Shard {shard.id+1}",
                    value=f"""
{self.bot.icons['arrow']}Latency: `{round(shard.latency, 1)}`ms
{self.bot.icons['arrow']}Count: `{shard.shard_count}`
""", inline=True
                )
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *, command : str = None):
        if command is None:
            em=discord.Embed(
                title="Help Page",
                description=f'''
```diff
- Type "{ctx.prefix}help [command]" or "{ctx.prefix}help [cog]" for more information about a command or cog
+ [argument] for an optional argument
+ <argument> for a required argument
```
[Developer](https://discord.com/users/{self.bot.ownersid}) | [Support]({self.bot.invite}) | [Invite](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)
''',
                timestamp=datetime.datetime.utcnow(),
                color=color()
            )
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            if ctx.guild is not None:
                disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                try:
                    disabled = disabled["commands"]
                except:
                    disabled = []
                else:
                    disabled = disabled.split(",")
            else:
                disabled = []
            cogs = []
            for cog in self.bot.cogs:
                cog = get_cog(self.bot, cog)
                if not cog.qualified_name.lower() in ["jishaku"]:
                    if is_mod(self.bot, ctx.author):
                        cmds = [cmd for cmd in cog.get_commands()]
                    else:
                        cmds = [cmd for cmd in cog.get_commands() if not cmd.hidden and not cmd.name in disabled]
                    if len(cmds) != 0 and cmds != []:
                        cogs.append(cog)
            em.add_field(
                name=f"Cogs [{len(cogs)}]",
                value="\n".join(f"`{cog.qualified_name}`" for cog in cogs),
                inline=True
            )
            process = psutil.Process()
            delta_uptime = datetime.datetime.utcnow() - self.bot.uptime
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            em.add_field(
                name="Information",
                value=f"""
**Uptime**: `{days}d {hours}h {minutes}m {seconds}s`
**Commands**: `{len([cmd for cmd in self.bot.commands if not cmd.hidden])}`
**Shards**: `{len(list(self.bot.shards))}`
**Memory**: `{humanize.naturalsize(process.memory_full_info().rss)}`
""",
                inline=True
            )
            em.set_image(url=self.bot.banner)
            await ctx.reply(embed=em, mention_author=False)
        else:
            if self.bot.get_command(str(command)) is not None:
                given_command = self.bot.get_command(str(command))
                disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                try:
                    disabled = disabled["commands"]
                except:
                    disabled = []
                else:
                    disabled = disabled.split(",")
                if not given_command.hidden == True and not given_command.name in disabled or is_mod(self.bot, ctx.author):
                    #-------------------------------------
                    try:
                        command_subcommands = "> " + ", ".join(f"`{command.name}`" for command in given_command.commands if not command.hidden or not command.name in disabled)
                    except:
                        command_subcommands = "None"
                    #-------------------------------------
                    if given_command.usage:
                        command_usage = given_command.usage
                    else:
                        parameters = {}
                        for param in list(given_command.params):
                            if not param in ["self", "ctx"]:
                                parameter = dict(given_command.params)[str(param)]
                                if parameter.kind.name.lower() == "positional_or_keyword":
                                    parameters[str(param)] = "required"
                                else:
                                    parameters[str(param)] = "optional"
                        command_usage = " ".join(f"<{param}>" if dict(parameters)[param] == "required" else f"[{param}]" for param in list(parameters))
                    #---------------------------------------
                    em=discord.Embed(
                        title=given_command.name,
                        timestamp=datetime.datetime.utcnow(),
                        description=given_command.description,
                        color=color()
                    )
                    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    em.add_field(name="Usage", value=f"{ctx.prefix}{given_command.name} {command_usage}", inline=False)
                    if given_command.aliases:
                        em.add_field(name=f"Aliases [{len(given_command.aliases)}]", value="> " + ", ".join(f"`{alias}`" for alias in given_command.aliases), inline=False)
                    else:
                        em.add_field(name="Aliases [0]", value="None", inline=False)
                    try:
                        if is_mod(self.bot, ctx.author):
                            commands_ = [cmd for cmd in given_command.commands]
                        else:
                            commands_ = [cmd for cmd in given_command.commands if not cmd.hidden and not cmd.name in disabled]
                    except:
                        commands_ = "None"
                    try:
                        em.add_field(name=f"Subcommands [{len(commands_)}]", value=command_subcommands, inline=False)
                    except AttributeError:
                        em.add_field(name=f"Subcommands [0]", value="None", inline=False)
                    em.add_field(name="Category", value=given_command.cog_name, inline=False)
                    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=em, mention_author=False)
                else:
                    em=discord.Embed(description=f"This command does not exist", color=color(), timestamp=datetime.datetime.utcnow())
                    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=em, mention_author=False)
            else:
                disabled = await self.bot.db.fetchrow("SELECT commands FROM commands WHERE guild = $1", ctx.guild.id)
                try:
                    disabled = disabled["commands"]
                except:
                    disabled = []
                else:
                    disabled = disabled.split(",")
                given_cog = get_cog(self.bot, command)
                if given_cog is not None:
                    if is_mod(self.bot, ctx.author):
                        commands_ = [cmd for cmd in given_cog.walk_commands() if cmd.parent is None]
                    else:
                        commands_ = [cmd for cmd in given_cog.walk_commands() if not cmd.hidden and not cmd.name in disabled and cmd.parent is None]
                    if commands_ is not None and commands_ != []:
                        em=discord.Embed(title=f"{given_cog.qualified_name} commands [{len(commands_)}]", description=f"{given_cog.description}\n\n> "+", ".join(f"`{cmd.name}`" for cmd in commands_), color=color(), timestamp=datetime.datetime.utcnow())
                        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        em.set_image(url=self.bot.banner)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em=discord.Embed(description=f"There isn't a cog / command with the name `{command}`", color=color(), timestamp=datetime.datetime.utcnow())
                        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.reply(embed=em, mention_author=False)
                else:
                    em=discord.Embed(description=f"There isn't a cog / command with the name `{command}`", color=color(), timestamp=datetime.datetime.utcnow())
                    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=em, mention_author=False)

    @commands.command(name="file", aliases=["makefile", "createfile"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def _file_(self, ctx, *, content):
        f = await getFile(content)
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, file=f, mention_author=False)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def minecraft(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=name, description=f"""
{self.bot.icons['arrow']}Name: `{name}`
{self.bot.icons['arrow']}UID: `{uid}`
""", color=color(), timestamp=datetime.datetime.utcnow(), url=f"https://namemc.com/profile/{name}")
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url=f"https://crafatar.com/avatars/{uid}?default=MHF_Steve&overlay&size=256")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def avatar(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=f"{name}'s avatar", color=color(), timestamp=datetime.datetime.utcnow(), url=f"https://namemc.com/profile/{name}")
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url=f"https://crafatar.com/avatars/{uid}?default=MHF_Steve&overlay&size128")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def skin(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=f"{name}'s skin", color=color(), timestamp=datetime.datetime.utcnow(), url=f"https://namemc.com/profile/{name}")
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url=f"https://crafatar.com/renders/body/{uid}?default=MHF_Steve&overlay&scale=5")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def head(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            em=discord.Embed(title=f"{name}'s head", color=color(), timestamp=datetime.datetime.utcnow(), url=f"https://namemc.com/profile/{name}")
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            em.set_image(url=f"https://crafatar.com/renders/head/{uid}?default=MHF_Steve&overlay&scale=5")
            await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @minecraft.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def friends(self, ctx, username):
        uid = await self.bot.session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        if uid.status == 200:
            uid = await uid.json()
            name = uid["name"]
            uid = uid["id"]
            res = await self.bot.session.get(f"https://api.namemc.com/profile/{uid}/friends")
            res = await res.json()
            if res != []:
                em=discord.Embed(title=f"{name}'s friends", color=color(), timestamp=datetime.datetime.utcnow(), url=f"https://namemc.com/profile/{name}")
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                for friend in list(res):
                    em.add_field(
                        name=friend["name"],
                        value=f"""
{self.bot.icons['arrow']}Name: `{friend['name']}`
{self.bot.icons['arrow']}UUID: `{friend['uuid']}`
{self.bot.icons['arrow']}[NameMC](https://namemc.com/profile/{friend['name']})
""",
                        inline=True
                    )
                await ctx.reply(embed=em, mention_author=False)
            else:
                em=discord.Embed(description=f"`{name}` has no friends on namemc.com", color=color(), timestamp=datetime.datetime.utcnow(), url=f"https://namemc.com/profile/{name}")
                em.set_thumbnail(url=f"https://crafatar.com/avatars/{uid}?default=MHF_Steve&overlay&size=256")
                em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=em, mention_author=False)
        else:
            em=discord.Embed(description=f"I couldn't find a player with the name `{username}`", color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def inviteinfo(self, ctx, invite):
        code = discord.utils.resolve_invite(invite)
        invite = await self.bot.fetch_invite(invite)
        guild = invite.guild
        if guild.description is not None:
            em=discord.Embed(title=guild.name,description=f"""
> {guild.description}

{self.bot.icons['arrow']}Created at: {guild.created_at.strftime('%d/%m/20%y at %H:%M:%S')} ({humanize.naturaltime(guild.created_at)})
{self.bot.icons['arrow']}Verification Level: {str(guild.verification_level).title()}""", color=color(), timestamp=datetime.datetime.utcnow(), url=invite)
        else:
            em=discord.Embed(title=guild.name,description=f"""
{self.bot.icons['arrow']}Created at: {guild.created_at.strftime('%d/%m/20%y at %H:%M:%S')} ({humanize.naturaltime(guild.created_at)})
{self.bot.icons['arrow']}Verification Level: {str(guild.verification_level).title()}""", color=color(), timestamp=datetime.datetime.utcnow(), url=invite)
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text=f"ID: {guild.id} • {ctx.author}", icon_url=ctx.author.avatar_url)
        if guild.banner_url is not None:
            em.set_image(url=guild.banner_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        dagpi_ping = round(await dagpi.image_ping(), 3) * 1000
        em.add_field(name="latency", value=f"""
{self.bot.icons['arrow']}**Typing**: `pinging`
{self.bot.icons['arrow']}**Bot**: `{round(self.bot.latency*1000)}`ms
{self.bot.icons['arrow']}**Database**: `pinging`
{self.bot.icons['arrow']}**Dagpi**: `{dagpi_ping}`ms""", inline=False)
        start=time.perf_counter()
        msg = await ctx.reply(embed=em, mention_author=False)
        end=time.perf_counter()
        final=end-start
        api_latency = round(final*1000)
        em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
        poststart = time.perf_counter()
        await self.bot.db.fetch("SELECT 1")
        postduration = (time.perf_counter()-poststart) * 1000
        db_ping = round(postduration, 1)
        em.add_field(name="latency", value=f"""
{self.bot.icons['arrow']}**Typing**: `{api_latency}`ms
{self.bot.icons['arrow']}**Bot**: `{round(self.bot.latency*1000)}`ms
{self.bot.icons['arrow']}**Database**: `{db_ping}`ms
{self.bot.icons['arrow']}**Dagpi**: `{dagpi_ping}`ms""", inline=False)
        await msg.edit(embed=em)

    @commands.command()
    async def afk(self, ctx, *, reason : str = None):
        if reason is None:
            msg = f"Okay, I've marked you as afk"
        else:
            msg = f"Okay, I've marked you as afk for `{reason}`"
        em=discord.Embed(description=msg, color=color(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=em, mention_author=False)
        await asyncio.sleep(3)
        self.bot.afks[ctx.author.id] = {"reason": reason}

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def ocr(self, ctx, member : discord.Member = None):
        if member is None:
            if ctx.message.attachments:
                if ctx.message.attachments[0].url.endswith("png") or ctx.message.attachments[0].url.endswith("jpg") or ctx.message.attachments[0].url.endswith("jpeg") or ctx.message.attachments[0].url.endswith("webp"):
                    url = ctx.message.attachments[0].proxy_url or ctx.message.attachments[0].url
                else:
                    url = ctx.author.avatar_url_as(format="png", size=1024)
            else:
                url = ctx.author.avatar_url_as(format="png", size=1024)
        else:
            url = member.avatar_url_as(format="png", size=1024)

        url = url.replace("cdn.discordapp.com", "media.discordapp.com")

        res = await self.bot.session.get(url)

        image = await res.read()

        if url.endswith("png"):
            filetype = "png"
        elif url.endswith("jpg"):
            filetype = "jpg"
        elif url.endswith("jpeg"):
            filetype = "jpeg"
        elif url.endswith("webp"):
            filetype = "webp"
        else:
            filetype = None
        
        async with ctx.typing():
            res = await idevisionn.ocr(image, filetype=filetype)

        if res != "":
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_footer(text=f"Powered by idevision.net • {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em, mention_author=False, file=getFile(res))
        else:
            em=discord.Embed(description=f"I couldn't read what your image says", color=color(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=em, mention_author=False)

def setup(bot):
    bot.add_cog(Utility(bot))
