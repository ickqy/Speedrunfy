import discord
import asyncio
import time
import typing

import cogs.utils.checks as checks

from discord.errors import Forbidden, NotFound
from discord.ext import commands

from core.bot import get_cogs
from .utils.formatting import realtime


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cc"])
    @checks.is_mod()
    async def purge(self, ctx, amount=1):
        """`Deletes messages in bulk (Only People with [manage_messages = True] can use this command)`"""
        await ctx.channel.purge(limit=amount)
        await ctx.reply("Messages Deleted", delete_after=5)

    @commands.command(usage="(member) [reason]")
    @checks.is_mod()
    async def kick(
        self,
        ctx,
        members: commands.Greedy[discord.Member],
        *,
        reason: str = "No Reason",
    ):
        """Kick a member."""
        if not members:
            return await ctx.reply(
                f"Usage: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
            )

        for member in members:
            if self.bot.user == member:  # Just why would you want to mute him?
                await ctx.reply("You're not allowed to kick Speedrunfy!")
            else:
                try:
                    await member.send(
                        f"You have been kicked from {ctx.guild.name} for {reason}!"
                    )
                except discord.errors.HTTPException:
                    pass

                try:
                    await ctx.guild.kick(member, reason=reason)
                except Forbidden:
                    await ctx.reply(
                        f"I can't kick {member.mention} (No permission or the member is higher than me on the hierarchy)"
                    )
                    return
                await ctx.send(
                    f"{member.mention} has been kicked by {ctx.author.mention} for {reason}!"
                )

    @commands.command(usage="(user) [reason];[ban duration]")
    @checks.is_mod()
    async def ban(
        self,
        ctx,
        members: commands.Greedy[discord.User],
        *,
        reason_duration: str = "No Reason;0",
    ):
        """Ban a member."""
        r_and_d = reason_duration.split(";")
        if len(r_and_d) < 2:
            r_and_d.append("0")
        reason = r_and_d[0] or "No Reason"
        try:
            min_ban = int(r_and_d[1])
        except ValueError:
            await ctx.reply(
                f"**WARNING**: {r_and_d[1]} is not a valid number, value `0` is used instead."
            )
            min_ban = 0

        if not members:
            return await ctx.reply(
                f"Usage: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
            )

        for member in members:
            if self.bot.user == member:  # Just why would you want to mute him?
                await ctx.reply("You're not allowed to ban Speedrunfy!")
            else:
                try:
                    await member.send(
                        f"You have been banned from {ctx.guild.name} for {reason}!"
                    )
                except Forbidden:
                    self.logger.error(
                        "discord.errors.Forbidden: Can't send DM to member"
                    )

                try:
                    await ctx.guild.ban(member, reason=reason, delete_message_days=0)
                except Forbidden:
                    await ctx.reply(
                        f"I can't ban {member.mention} (No permission or the member is higher than me on the monarchy )"
                    )
                    return
                duration = ""
                if min_ban > 0:
                    duration = f" ({min_ban} minutes)"
                await ctx.send(
                    f"{member.mention} has been banned by {ctx.author.mention} for {reason}!{duration}"
                )

            if min_ban > 0:
                await asyncio.sleep(min_ban * 60)
                await ctx.guild.unban(member, reason="timed out")

    @commands.command(usage="(user)")
    @checks.is_mod()
    async def unban(self, ctx, members: commands.Greedy[discord.User]):
        """Unban a member."""
        if not members:
            return await ctx.reply(
                f"Usage: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
            )

        for member in members:
            # try:
            #     await member.send(f"You have been unbanned from {ctx.guild.name}!")
            # except Forbidden:
            #     self.logger.error("discord.errors.Forbidden: Can't send DM to member")
            # except AttributeError:
            #     self.logger.error("Attribute error!")
            try:
                await ctx.guild.unban(member)
            except NotFound:
                await ctx.reply(f"{member.mention} is not banned!")
            else:
                await ctx.send(
                    f"{member.mention} has been unbanned by {ctx.author.mention}!"
                )

    @commands.command(usage="(extension)", hidden=True)
    @checks.is_botmaster()
    async def unload(self, ctx, ext):
        """Unload an extension."""
        await ctx.send(f"Unloading {ext}...")
        try:
            self.bot.unload_extension(f"cogs.{ext}")
            await ctx.send(f"{ext} has been unloaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{ext} doesn't exist!")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"{ext} is not loaded!")
        except commands.ExtensionFailed:
            await ctx.send(f"{ext} failed to unload! Check the log for details.")
            self.bot.logger.exception(f"Failed to reload extension {ext}:")

    @commands.command(usage="[extension]", hidden=True)
    @checks.is_botmaster()
    async def reload(self, ctx, ext: str = None):
        """Reload an extension."""
        if not ext:
            reload_start = time.time()
            exts = get_cogs()
            reloaded = []
            error = 0
            for ext in exts:
                try:
                    self.bot.reload_extension(f"{ext}")
                    reloaded.append(f"<:check:854498005221769228>| {ext}")
                except commands.ExtensionNotFound:
                    reloaded.append(f"<:check:854498005221769228>| {ext}")
                    error += 1
                except commands.ExtensionNotLoaded:
                    reloaded.append(f"<:cross:854498023061061633>| {ext}")
                    error += 1
                except commands.ExtensionFailed:
                    self.bot.logger.exception(f"Failed to reload extension {ext}:")
                    reloaded.append(f"<:cross:854498023061061633>| {ext}")
                    error += 1
            reloaded = "\n".join(reloaded)
            embed = discord.Embed(
                title="Reloading all cogs...",
                description=f"{reloaded}",
                colour=discord.Colour(0x2F3136),
            )
            embed.set_footer(
                text=f"{len(exts)} cogs has been reloaded"
                + f", with {error} errors \n"
                + f"in {realtime(time.time() - reload_start)}"
            )
            await ctx.send(embed=embed)
            return
        await ctx.send(f"Reloading {ext}...")
        try:
            self.bot.reload_extension(f"cogs.{ext}")
            await ctx.send(f"{ext} has been reloaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{ext} doesn't exist!")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"{ext} is not loaded!")
        except commands.ExtensionFailed:
            await ctx.send(f"{ext} failed to reload! Check the log for details.")
            self.bot.logger.exception(f"Failed to reload extension {ext}:")

    @commands.command(usage="(extension)", hidden=True)
    @checks.is_botmaster()
    async def load(self, ctx, ext):
        """Load an extension."""
        await ctx.send(f"Loading {ext}...")
        try:
            self.bot.load_extension(f"cogs.{ext}")
            await ctx.send(f"{ext} has been loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{ext} doesn't exist!")
        except commands.ExtensionFailed:
            await ctx.send(f"{ext} failed to load! Check the log for details.")
            self.bot.logger.exception(f"Failed to reload extension {ext}:")

    @commands.command()
    @checks.is_mod()
    async def poll(self, ctx, title, role: typing.Union[discord.Role, str], *options):
        """`Create a poll with the bot`"""
        emojiLetters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
        ]

        if role is None:
            await ctx.reply("Please choose what role you want to ping. `-poll <everyone/here/id of role> <rest of poll>`")
            return

        else:
            await discord.Message.delete(ctx.message)
            options = list(options)
            for i in range(len(options)):
                options[i] = f"{emojiLetters[i]}  {options[i]}"
            embed = discord.Embed(
                title=title,
                description='\n'.join(options),
                color=0x000000
            )
            try:
                message = await ctx.send(content=role.mention, embed=embed)
            except AttributeError:
                message = await ctx.send(content="@"+role, embed=embed)
            for i in range(len(options)):
                await message.add_reaction(emojiLetters[i])


def setup(bot):
    bot.add_cog(Moderation(bot))
