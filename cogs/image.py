import discord, asyncdagpi, datetime, io
from discord.ext import commands
from utils.get import get_config
from utils.configs import color
from jishaku.functools import executor_function

dagpi = asyncdagpi.Client(get_config("DAGPI"))

@executor_function
def rounden(img):
    from PIL import Image, ImageOps, ImageDraw
    mask = Image.new('L', (1024, 1024), 255)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + (1024, 1024), fill=0)
    img = Image.open(img)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(500)
    output.paste(0, mask=mask)
    output.convert('P', palette=Image.ADAPTIVE)
    array = io.BytesIO()
    output.save(array, format="png")
    return discord.File(io.BytesIO(array.getvalue()), "circular.png")

class Image(commands.Cog):

    """Image manipulation commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["circle", "round", "circular"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def rounden(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await self.bot.session.get(str(url))
            img = await img.read()
            res = await rounden(io.BytesIO(img))
            em=discord.Embed(color=color())
            em.set_image(url="attachment://circular.png")
        await ctx.reply(file=res, embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pixel(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pixel(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def america(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.america(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triggered(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triggered(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.gif")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.gif")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wasted(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wasted(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def invert(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.invert(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def sobel(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.sobel(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def triangle(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.triangle(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def blur(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.blur(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def angel(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.angel(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["s8n"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def satan(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.satan(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def delete(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.delete(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def fedora(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.fedora(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command(aliases=["hitler", "wth"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def worsethanhitler(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.hitler(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def wanted(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.wanted(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def jail(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.jail(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def pride(self, ctx, flag : str = "gay", member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.pride(), url=str(url), flag=flag)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def trash(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.trash(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def magik(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.magik(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.gif")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.gif")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def paint(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.paint(), url=str(url))
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def captcha(self, ctx, text : str, member : discord.Member = None):
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
        async with ctx.typing():
            img = await dagpi.image_process(asyncdagpi.ImageFeatures.captcha(), url=str(url), text=text)
            file=discord.File(img.image, f"{ctx.command.name}.png")
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=f"attachment://{ctx.command.name}.png")
            em.set_footer(text=f"Powered by dagpi.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=em)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def clyde(self, ctx, *, message):
        message = message.replace(" ", "%20")
        async with ctx.typing():
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={message}")
            res = await res.json()
            res = res["message"]
            em=discord.Embed(color=color())
            em.set_image(url=res)
            em.set_footer(text=f"Powered by nekobot.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def stickbug(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=stickbug&url={url}")
            res = await res.json()
            res = res["message"]
            img = await self.bot.session.get(res)
            img = await img.read()
            em=discord.Embed(color=color())
            em.set_footer(text=f"Powered by nekobot.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, file=discord.File(io.BytesIO(img), filename="stickbug.mp4"), mention_author=False)

    @commands.command(aliases=["cmm"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def changemymind(self, ctx, *, message):
        message = message.replace(" ", "%20")
        async with ctx.typing():
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={message}")
            res = await res.json()
            res = res["message"]
            em=discord.Embed(color=color())
            em.set_image(url=res)
            em.set_footer(text=f"Powered by nekobot.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["phc", "pornhubcomment"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def phcomment(self, ctx, *, message):
        message = message.replace(" ", "%20")
        async with ctx.typing():
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={ctx.author.avatar_url_as(format='png')}&username={ctx.author.display_name}&text={message}")
            res = await res.json()
            res = res["message"]
            em=discord.Embed(color=color())
            em.set_image(url=res)
            em.set_footer(text=f"Powered by nekobot.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["iphonex"])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def iphone(self, ctx, member : discord.Member = None):
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
        async with ctx.typing():
            res = await self.bot.session.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={url}")
            res = await res.json()
            image = res["message"]
            em=discord.Embed(color=color(), timestamp=datetime.datetime.utcnow())
            em.set_image(url=image)
            em.set_footer(text=f"Powered by nekobot.xyz • {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=em, mention_author=False)


def setup(bot):
    bot.add_cog(Image(bot))