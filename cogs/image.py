import discord
import asyncdagpi
import io
from discord.ext import commands
from utils.get import *
from utils.functions import *
from jishaku.functools import executor_function
from __main__ import bot as bot_

dagpi = asyncdagpi.Client(bot_.config["DAGPI"])

class Image(commands.Cog):

    """Image manipulation commands"""

    def __init__(self, bot):
        self.bot = bot

    @executor_function
    def rounden(self, img, ellipse: tuple):
        from PIL import Image, ImageOps, ImageDraw
        size = (1024, 1024)
        mask = Image.new('L', size, 255)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(ellipse + size, fill=0)
        img = Image.open(img)
        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(500)
        output.paste(0, mask=mask)
        output.convert('P', palette=Image.ADAPTIVE)
        buffer = io.BytesIO()
        output.save(buffer, format="png")
        return discord.File(io.BytesIO(buffer.getvalue()), "circular.png")

    @commands.command(name="rounden", aliases=["circle", "round", "circular"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def _rounden(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await self.bot.session.get(str(url))
            img = await img.read()
            res = await self.rounden(io.BytesIO(img), (0,0))
            em=discord.Embed(color=self.bot.color)
            em.set_image(url="attachment://circular.png")
        await ctx.reply(file=res, embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pixel(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pixel(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["amhu"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def allmyhomiesuse(self, ctx, bad: str, good: str):
        async with ctx.processing(ctx):
            img = await dagpi.image_process(
                asyncdagpi.ImageFeatures.retro_meme(),
                url="https://media.discordapp.net/attachments/698057848449400832/855803039649366036/dee.png",
                top_text=f"Fuck {bad}",
                bottom_text=f"All My Homies use {good}"
            )
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def retromeme(self, ctx, top: str, bottom: str, url: str = None):
        url = await getImage(ctx, url)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(
                asyncdagpi.ImageFeatures.retro_meme(),
                url=url,
                top_text=top,
                bottom_text=bottom
            )
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def modernmeme(self, ctx, top: str, bottom: str, url: str = None):
        url = await getImage(ctx, url)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(
                asyncdagpi.ImageFeatures.retro_meme(),
                url=url,
                top_text=top,
                bottom_text=bottom
            )
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def america(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.america(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triggered(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triggered(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.gif")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.gif")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wasted(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wasted(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def invert(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.invert(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def sobel(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.sobel(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triangle(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triangle(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def angel(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.angel(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["s8n"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def satan(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.satan(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def delete(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.delete(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def fedora(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.fedora(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["hitler", "wth"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def worsethanhitler(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.hitler(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wanted(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wanted(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["ytcomment"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def youtubecomment(self, ctx, member: discord.Member, *, text):
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.youtube(), url=getImage(ctx, member), username=member.display_name, text=text)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command(name="discord")
    @commands.cooldown(1,10,commands.BucketType.user)
    async def _discord(self, ctx, member: discord.Member, *, text):
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.discord(), url=str(member.avatar_url_as(format="png")), username=member.display_name, text=text)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def jail(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
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
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.jail(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pride(self, ctx, flag: str = "gay", member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pride(), url=str(url), flag=flag)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def trash(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.trash(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def magik(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.magik(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def paint(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.paint(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def captcha(self, ctx, text: str, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.captcha(), url=str(url), text=text)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=f"attachment://{ctx.command.name}.png")
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def clyde(self, ctx, *, message):
        message = message.replace(" ", "%20")
        async with ctx.processing(ctx):
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={message}")
            res = await res.json()
            res = res["message"]
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=res)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def stickbug(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=stickbug&url={url}")
            res = await res.json()
            res = res["message"]
            img = await self.bot.session.get(res)
            img = await img.read()
        await ctx.reply(file=discord.File(io.BytesIO(img), filename="stickbug.mp4"), mention_author=False)

    @commands.command(aliases=["cmm"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def changemymind(self, ctx, *, message):
        message = message.replace(" ", "%20")
        async with ctx.processing(ctx):
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={message}")
            res = await res.json()
            res = res["message"]
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=res)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["phc", "pornhubcomment"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def phcomment(self, ctx, member: discord.Member, *, message):
        message = message.replace(" ", "%20")
        async with ctx.processing(ctx):
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={member.avatar_url_as(format='png')}&username={member.display_name}&text={message}")
            res = await res.json()
            res = res["message"]
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=res)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["iphonex"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def iphone(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={url}")
            res = await res.json()
            image = res["message"]
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=image)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def jpeg(self, ctx, member: typing.Union[discord.Emoji, discord.PartialEmoji, discord.Member, str] = None):
        url = await getImage(ctx, member)
        async with ctx.processing(ctx):
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=jpeg&url={url}")
            res = await res.json()
            image = res["message"]
            em=discord.Embed(color=self.bot.color)
            em.set_image(url=image)
        await ctx.reply(embed=em, mention_author=False)


def setup(bot):
    bot.add_cog(Image(bot))
