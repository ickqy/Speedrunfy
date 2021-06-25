
import asyncio
import discord
import prettify_exceptions


from discord.ext import commands


class ErrorHandler(commands.Cog):
    """Handle errors."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = self.bot.logger

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
