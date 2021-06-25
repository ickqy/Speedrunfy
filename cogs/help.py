import discord
import logging


from discord.ext import commands
from discord.ext.commands.core import Group


class CustomHelp(commands.HelpCommand):
    COLOUR = discord.Colour(0x000000)

    def get_desc(self):
        desc = "Bot prefix is `-`"
        return desc

    def get_ending_note(self):
        return "Use {0}{1} [command] for more info on a command, or {0}{1} [category] for more info on a category".format(
            self.clean_prefix, self.invoked_with
        )

    def get_command_signature(self, cmd):
        return f"{self.cmd_and_alias(cmd)} {cmd.signature}"

    def command_not_found(self, string):
        return f"There's no command called `{string}`"

    def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            return f"Command `{command.qualified_name}` has no subcommand called `{string}`"
        return f"Command `{command.qualified_name}` has no subcommands"

    def cmd_and_alias(self, command):
        cmd = "|".join([str(command.qualified_name), *command.aliases])
        return cmd

    async def send_error_message(self, error):
        embed = discord.Embed(
            title="Error!", description=f"{error}", colour=discord.Colour(0x2F3136)
        )

        await self.get_destination().send(embed=embed)

    async def send_bot_help(self, mapping):
        destination = self.get_destination()
        embed = discord.Embed(
            title="Categories",
            description=self.get_desc()
            + "\n"
            + "`()` = Required\n"
            + "`[]` = Optional",
            colour=self.COLOUR,
        )
        for cog, commands in mapping.items():
            if cog and str(cog.qualified_name).lower() == "helpcmd":
                continue

            def f(x):
                return {
                    "fun": "<:Fun:856015753059500092>",
                    "general": "<:General:856015735133306911>",
                    "moderation": "<:Moderation:856015703462641699>",
                    "music": "<:Music:856015703986667531>",
                    "stars": "<:Starboard:856015703881941012>",
                    "timer": "<:Timer:856015735155589121>"
                }.get(x.lower(), "​")

            name = (
                "No Category"
                if cog is None
                else f"{f(cog.qualified_name)} {cog.qualified_name}".title()
            )
            value = f"```{self.clean_prefix}help {'No Category' if cog is None else cog.qualified_name}```"
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                #     value = ", ".join(f"`{c.name}`" for c in commands)
                #     if cog and cog.description:
                #         value = f"{cog.description}\n{value}"
                if cog.qualified_name.lower() not in ["help", "pingloop"]:
                    embed.add_field(name=name, value=value, inline=True)
        embed.set_footer(text=self.get_ending_note())
        await destination.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"{cog.qualified_name} Commands",
            description=self.get_desc()
            + "\n\
                                 `()` = Required\n\
                                 `[]` = Optional",
            colour=self.COLOUR,
        )
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            if command.brief:
                value = command.brief
            else:
                value = command.short_doc
            embed.add_field(
                name=self.get_command_signature(command),
                value=value or "...",
                inline=False,
            )

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(
            title=self.clean_prefix + self.get_command_signature(group),
            description=self.get_desc(),
            colour=self.COLOUR,
        )
        if group.help:
            embed.description = "`()` = Required\n" + "`[]` = Optional\n" + group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            subcmds = "```"
            for command in filtered:
                if command.brief:
                    value = command.brief
                else:
                    value = command.short_doc
                subcmds += f"{self.clean_prefix}{self.get_command_signature(command)}\n{value}\n\n"
                # embed.add_field(
                #     name=self.get_command_signature(command),
                #     value=value or "No description.",
                #     inline=False,
                # )
            subcmds += "```"
            embed.add_field(name="Subcommands", value=subcmds)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=self.clean_prefix + self.get_command_signature(command),
            description=command.help or "No description.",
            colour=self.COLOUR,
        )

        await self.get_destination().send(embed=embed)


class HelpCmd(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(HelpCmd(bot))
