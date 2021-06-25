import discord
import time
import textwrap
import asyncio
import unicodedata
import discord.utils


from discord.ext import commands

from pytz import timezone
from typing import Union


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """`See the bot's latency`"""
        websocket = round(self.bot.latency*1000, 2)

        ping_start = time.perf_counter()
        msg = await ctx.reply(f"Pong! `{websocket}` ms")
        ping_end = time.perf_counter()
        typing = (ping_end - ping_start) * 1000
        return await msg.edit(content=f"Pong! `{websocket}` ms | `{round(typing, 2)}` ms")

    @commands.command(aliases=["bi", "about", "info"])
    async def botinfo(self, ctx):
        """`Shows the bot's information.`"""
        bot_ver = "v3.0"
        embed = discord.Embed(
            title="About Speedrunfy",
            colour=discord.Colour(0x000000),
            timestamp=ctx.message.created_at,
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Speedrunfy Dev Team", value="<@564610598248120320>, <@186713080841895936>")
        embed.add_field(
            name="discord.py",
            value=f"[{discord.__version__}](https://github.com/ickqy/Speedrunfy)",
        )
        embed.add_field(
            name="About",
            value="**Speedrunfy** is an open source bot, "
            + "a fork of [mcbeDiscordBot](https://github.com/AnInternetTroll/mcbeDiscordBot) "
            + "(Steve the Bot) created by [AnInternetTroll](https://github.com/AnInternetTroll), "
            + "and from [ZiRO-Bot](https://github.com/ZiRO-Bot/ziBot) (ziBot) created by "
            + "[null2264](https://github.com/null2264), "
            + f"but rewritten a bit.\n\n**Bot Version**: {bot_ver}",
            inline=False,
        )
        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ui"], usage="[member]")
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """`Shows user information.`"""
        member = user or ctx.message.author

        def stat(x):
            return {
                "offline": "<:offline:854498073622872094>",
                "idle": "<:idle:854498072784535583>",
                "dnd": "<:dnd:854498023027113984>",
                "online": "<:online:854498112700940349>",
                "streaming": "<:streaming:854498144866664458>",
            }.get(str(x), "None")

        def badge(x):
            return {
                "UserFlags.bug_hunter": "<:bughunter:854497987682500630>",
                "UserFlags.bug_hunter_level_2": "<:goldbughunter:854498044899885096>",
                "UserFlags.early_supporter": "<:earlysupporter:854498023014006834>",
                "UserFlags.verified_bot_developer": "<:verifiedbotdev:854498023027113994>",
                "UserFlags.hypesquad": "<:hypesquad:854498045013655553>",
                "UserFlags.hypesquad_balance": "<:balance:854497958606798858>",
                "UserFlags.hypesquad_bravery": "<:bravery:854497968262610944>",
                "UserFlags.hypesquad_brilliance": "<:brilliance:855167273659662366>",
                "UserFlags.partner": "<:partner:854498113107656714>",
                "UserFlags.staff": "<:staff:854498113284472872>",
                "UserFlags.verified": "<:verified:854498144879509514>",
                "UserFlags.verified_bot": "<:verified:854498144879509514>",
                "UserFlags.booster": "<:booster:855190686382030848>",
                "UserFlags.owner": "<:owner:855191603597541397>",
            }.get(x, "🚫")

        def activity(x):
            return {
                "playing": "Playing ",
                "watching": "Watching ",
                "listening": "Listening to ",
                "streaming": "Streaming ",
                "custom": "",
            }.get(x, "None ")

        badges = []
        for x in list(member.public_flags.all()):
            x = str(x)
            if member == ctx.guild.owner:
                badges.append(badge("UserFlags.owner"))
            badges.append(badge(x))

        roles = []
        if member:
            for role in member.roles:
                if role.name != "@everyone":
                    roles.append(role.mention)

        jakarta = timezone("Europe/London")

        if member:
            status = member.status
            statEmoji = stat(member.status)
        else:
            status = "Unknown"
            statEmoji = "❓"
        embed = discord.Embed(
            description=f"{statEmoji}({status})\n"
            + (
                "<:activity:854497939229376512>"
                + activity(str(member.activity.type).replace("ActivityType.", ""))
                + f"**{member.activity.name}**"
                if member and member.activity
                else ""
            ),
            colour=member.colour if member else discord.Colour(0x000000),
            timestamp=ctx.message.created_at,
        )
        embed.set_author(
            name=f"{member}", icon_url=member.avatar_url
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Guild name", value=member.display_name)
        embed.add_field(
            name="Badges", value=" ".join(badges) if badges else "No badge."
        )
        embed.add_field(
            name="Created on",
            value=member.created_at.replace(tzinfo=timezone("GMT"))
            .astimezone(jakarta)
            .strftime("%a, %#d %B %Y, %H:%M UTC"),
        )
        embed.add_field(
            name="Joined on",
            value=member.joined_at.replace(tzinfo=timezone("GMT"))
            .astimezone(jakarta)
            .strftime("%a, %#d %B %Y, %H:%M UTC")
            if member
            else "Not a member.",
        )
        if len(", ".join(roles)) <= 1024:
            embed.add_field(
                name=f"Roles ({len(roles)})",
                value=", ".join(roles) or "No roles.",
                inline=False,
            )
        else:
            embed.add_field(name="Roles", value=f"{len(roles)}", inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        """`Show server information.`"""
        embed = discord.Embed(
            title=f"About {ctx.guild.name}",
            colour=discord.Colour(0x000000),
            timestamp=ctx.message.created_at,
        )

        roles = []
        for role in ctx.guild.roles:
            if role.name != "@everyone":
                roles.append(role.mention)
        width = 3

        boosters = [x.mention for x in ctx.guild.premium_subscribers]

        embed.add_field(name="Owner", value=f"{ctx.guild.owner.mention}", inline=False)
        embed.add_field(name="Created on", value=f"{ctx.guild.created_at.date()}")
        embed.add_field(name="Region", value=f"``{ctx.guild.region}``")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(
            name="Verification Level", value=f"{ctx.guild.verification_level}".title()
        )
        embed.add_field(
            name="Channels",
            value="<:category:855196538912768041>"
            + f" {len(ctx.guild.categories)}\n"
            + "<:text_channel:854498144866795572>"
            + f" {len(ctx.guild.text_channels)}\n"
            + "<:voice_channel:854498144917127209>"
            + f" {len(ctx.guild.voice_channels)}\n"
            + "<:stage_channel:854498113376747550>"
            + f" {len(ctx.guild.stage_channels)}",
        )
        embed.add_field(name="Members", value=f"{ctx.guild.member_count}")
        if len(boosters) < 5:
            embed.add_field(
                name=f"Boosters ({len(boosters)})",
                value=",\n".join(
                    ", ".join(boosters[i:i + width])
                    for i in range(0, len(boosters), width)
                )
                if boosters
                else "No booster.",
            )
        else:
            embed.add_field(name=f"Boosters ({len(boosters)})", value=len(boosters))
        if len(", ".join(roles)) <= 1024:
            embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles))
        else:
            embed.add_field(name="Roles", value=f"{len(roles)}")
        embed.set_footer(text=f"ID: {ctx.guild.id}")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ut"])
    async def uptime(self, ctx):
        """`Check the bot's uptime`"""
        seconds = time.time() - self.bot.start_time
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        uptime_str = f'{int(d)}d : {int(h)}h : {int(m)}m : {int(s)}s'

        await ctx.reply(f"Heyo! I have been awake for `{uptime_str}`")

    @commands.command(name="emojiinfo", aliases=["ei"], brief="Get an emoji's information")
    async def emojiinfo(
        self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str]
    ):
        try:
            if emoji.animated:
                e = discord.Embed(
                    title=f":{emoji.name}:",
                    description=f"`ID: {emoji.id}`\n`Bot String: <\u200b:{emoji.name}:{emoji.id}>`\n`Type: Custom Emoji`",
                    color=discord.Colour(0x000000)
                )
                e.set_image(url=emoji.url)
            else:
                e = discord.Embed(
                    title=f":{emoji.name}:",
                    description=f"`ID: {emoji.id}`\n`Bot String: <\u200b:{emoji.name}:{emoji.id}>`\n`Type: Custom Emoji`",
                    colour=discord.Colour(0x000000)
                )
                e.set_image(url=emoji.url)
        except AttributeError:
            try:
                e = discord.Embed(
                    title=" - ".join(
                        (
                            emoji,
                            hex(ord(emoji)).replace("0x", r"\u"),
                            unicodedata.name(emoji),
                        )
                    ),
                    description="`Type: Unicode`",
                    colour=discord.Colour(0x000000)
                )
            except TypeError:
                return await ctx.reply("`{}` is not a valid emoji!".format(emoji))
        return await ctx.reply(embed=e)

    @commands.command(aliases=["el"])
    async def emojilist(self, ctx):
        """`List all emojis in the server.`"""
        emojis = " ".join([str(emoji) for emoji in ctx.guild.emojis])
        emoji_list = textwrap.wrap(emojis, 1024)

        page = 1
        total_page = len(emoji_list)
        embed_reactions = ["◀️", "⏹️", "▶️"]

        def check_reactions(reaction, user):
            if user == ctx.author and str(reaction.emoji) in embed_reactions:
                return str(reaction.emoji)
            else:
                return False

        def create_embed(ctx, page):
            e = discord.Embed(
                title="Emojis",
                description=emoji_list[page - 1],
                color=discord.Colour(0x000000),
                timestamp=ctx.message.created_at,
            )
            e.set_author(
                name=f"{ctx.guild.name} - {page}/{total_page}",
                icon_url=ctx.guild.icon_url,
            )
            e.set_footer(
                text=f"Requested by {ctx.message.author.name}#{ctx.message.author.discriminator}"
            )
            return e

        embed = create_embed(ctx, page)
        msg = await ctx.reply(embed=embed)
        for emoji in embed_reactions:
            await msg.add_reaction(emoji)
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check_reactions, timeout=60.0
                )
            except asyncio.TimeoutError:
                break
            else:
                emoji = check_reactions(reaction, user)
                try:
                    await msg.remove_reaction(reaction.emoji, user)
                except discord.Forbidden:
                    pass
                if emoji == "◀️" and page != 1:
                    page -= 1
                    embed = create_embed(ctx, page)
                    await msg.edit(embed=embed)
                if emoji == "▶️" and page != total_page:
                    page += 1
                    embed = create_embed(ctx, page)
                    await msg.edit(embed=embed)
                if emoji == "⏹️":
                    # await msg.clear_reactions()
                    break
        return


def setup(bot):
    bot.add_cog(General(bot))
