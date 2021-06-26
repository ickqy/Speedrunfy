import asyncio
import discord
import prettify_exceptions
import pytz
import traceback
import sys


from discord.ext import commands

from .utils.src import GameNotFound


class ErrorHandler(commands.Cog):
    """Handle errors."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = self.bot.logger

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        if isinstance(error, pytz.exceptions.UnknownTimeZoneError):
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(
                "That's not a valid timezone. You can look them up at https://kevinnovak.github.io/Time-Zone-Picker/"
            )

        if isinstance(error, GameNotFound):
            e = discord.Embed(title=str(error), colour=discord.Colour.red())
            return await ctx.reply(embed=e)

        if isinstance(error, pytz.exceptions.UnknownTimeZoneError):
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(
                "That's not a valid timezone. You can look them up at https://kevinnovak.github.io/Time-Zone-Picker/"
            )
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply("Command not Found")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(
                f"Usage: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
            )

        if isinstance(error, commands.CommandOnCooldown):
            bot_msg = await ctx.reply(
                f"{ctx.author.mention}, you have to wait {round(error.retry_after, 2)} seconds before using this again"
            )
            await asyncio.sleep(round(error.retry_after))
            await bot_msg.delete()
            return

        if isinstance(error, commands.CommandInvokeError):
            _traceback = ''.join(prettify_exceptions.DefaultFormatter().format_exception(type(error), error, error.__traceback__))
            self.bot.logger.error(f"Something went wrong! error: {error}\n{_traceback}")

            error = discord.Embed(
                title="Something went wrong!",
                description=f"Here is the error\n```{error}```",
                color=0x2E3137
            )
            await ctx.reply(embed=error)
        else:
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
