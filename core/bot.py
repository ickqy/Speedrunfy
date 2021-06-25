import discord
import logging
import re
import aiohttp
import aiosqlite
import time
import config

from discord.ext import commands
from databases import Database

from core.objects import Connection


def get_cogs():
    """callable extensions"""
    extensions = [
        "cogs.fun",
        "cogs.general",
        "cogs.help",
        "cogs.mods",
        "cogs.starboard",
        "cogs.status",
        "cogs.error_handler",
        "cogs.time",
        "cogs.src",
        "cogs.runget",
        "cogs.fair",
    ]

    return extensions


extensions = get_cogs()

start_time = time.time()


def _callable_prefix(bot, message):
    """Callable Prefix for the bot."""
    user_id = bot.user.id
    base = [f"<@!{user_id}> ", f"<@{user_id}> "]
    if not message.guild:
        base.extend(bot.def_prefix)
    else:
        # can be changed for per-server prefix
        #
        # example:
        #   base.extend(
        #       sorted(bot.cache[message.guild.id].get("prefixes", bot.def_prefix))
        #   )

        base.extend(bot.def_prefix)
    return base


class Speedrunfy(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=_callable_prefix,
            case_insensitive=True,
            intents=discord.Intents.all(),
        )
        # Get Bot Master's ID
        self.master = [564610598248120320]

        # make cogs case insensitive
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

        self.logger = logging.getLogger("discord")

        # bot's default prefix
        self.def_prefix = ["s!"]

        # Uptime
        self.start_time = time.time()

        # Database
        self.db = Database(config.sql, factory=Connection)

        # Session
        self.session = aiohttp.ClientSession()

    async def asyncInit(self):
        """`__init__` but async"""
        self.db = await aiosqlite.connect("database.db")

    async def on_ready(self):
        # load all listed extensions
        for extension in extensions:
            self.load_extension(extension)

        self.logger.warning(f"Online: {self.user} (ID: {self.user.id})")

    async def on_message(self, message):
        # dont accept commands from bot
        if message.author.bot:
            return

        # if bot is mentioned without any other message, send prefix list
        pattern = f"<@(!?){self.user.id}>"
        if re.fullmatch(pattern, message.content):
            prefixes = _callable_prefix(self, message)
            prefixes.pop(0)
            prefixes.pop(0)
            prefixes = ", ".join([f"`{x}`" for x in prefixes])
            await message.reply("My prefixes are: `{}` or {}".format(prefixes, self.user.mention))

        await self.process_commands(message)

    async def close(self):
        await super().close()
        await self.db.close()
        await self.session.close()

    def run(self):
        super().run(config.token, reconnect=True)

    @property
    def config(self):
        return __import__("config")
