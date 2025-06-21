from typing import Dict, List, Any, Optional, Callable

import discord
from discord import app_commands
from discord.app_commands import commands, Cooldown
from discord.ext.commands import BucketType

from exceptions.IntentsMissingException import IntentsMissingError
from exceptions.PermissionsMissingException import PermissionsMissingError


class CommandManager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tree = bot.tree
        self.commands: Dict[str, Dict[str, Any]] = {}

    def _check_intents(self, required_intents: List[str]):
        missing = [intent for intent in required_intents if not getattr(self.bot.intents, intent, False)]
        if missing:
            raise IntentsMissingError(missing)

    async def _check_permissions(self, interaction: discord.Interaction, required_perms: List[str]):
        if not interaction.guild:
            return []
        bot_perms = interaction.guild.me.guild_permissions
        missing = [perm for perm in required_perms if not getattr(bot_perms, perm, False)]
        return missing

    def register_slash_command(
            self,
            *,
            name: Optional[str] = None,
            description: str = "No description provided",
            callback: Callable,
            required_intents: Optional[List[str]] = None,
            required_perms: Optional[List[str]] = None,
            cooldown: Optional[Cooldown] = None,
            guild_only: bool = False,
            guild_ids: Optional[List[int]] = None
    ):
        """
        Register a slash command with permission and intent checks.

        Args:
            name: Command name. Defaults to callback.__name__.
            description: Command description.
            callback: Async function called when command is used.
            required_intents: List of intents required for this command.
            required_perms: List of bot permissions required.
            cooldown: Cooldown object to rate limit command usage per user.
            guild_only: Restrict command to guilds if True.
            guild_ids: Limit command registration to specific guild IDs.
        """

        required_intents = required_intents or []
        required_perms = required_perms or []

        self._check_intents(required_intents)

        command_name = name or callback.__name__

        async def command_wrapper(interaction: discord.Interaction, *args, **kwargs):
            if cooldown and cooldown.is_on_cooldown(interaction.user.id):
                await interaction.response.send_message(
                    f"⏳ You are on cooldown. Please wait before using this command again.",
                    ephemeral=True
                )
                return

            missing_perms = await self._check_permissions(interaction, required_perms)
            if missing_perms:
                raise PermissionsMissingError(missing_perms)

            await callback(interaction, *args, **kwargs)

            if cooldown:
                cooldown.update_usage(interaction.user.id)

        slash_command = app_commands.Command(
            name=command_name,
            description=description,
            callback=command_wrapper
        )

        if guild_only and guild_ids:
            for guild_id in guild_ids:
                self.tree.add_command(slash_command, guild=discord.Object(id=guild_id))
        elif guild_only:
            raise ValueError("guild_only is True but no guild_ids were provided.")
        else:
            self.tree.add_command(slash_command)

        self.commands[command_name] = {
            "callback": callback,
            "required_intents": required_intents,
            "required_perms": required_perms,
            "cooldown": cooldown,
            "guild_only": guild_only,
            "guild_ids": guild_ids,
        }

    def register_legacy_command(
            self,
            *,
            name: Optional[str] = None,
            description: str = "No description provided",
            callback: Callable,
            required_intents: Optional[List[str]] = None,
            required_perms: Optional[List[str]] = None,
            cooldown: Optional[Cooldown] = None,
    ):
        """
        Register a legacy (prefix) command.

        Args:
            name: Command name. Defaults to callback.__name__.
            description: Command description/help.
            callback: Async function called when command is invoked.
            required_intents: List of intents required.
            required_perms: List of bot permissions required.
            cooldown: Cooldown for rate limiting.
        """

        required_intents = required_intents or []
        required_perms = required_perms or []

        self._check_intents(required_intents)

        command_name = name or callback.__name__

        @self.bot.command(name=command_name, help=description)
        @commands.cooldown(rate=cooldown.rate if cooldown else 0, per=cooldown.per if cooldown else 0,
                           type=commands.BucketType.user)
        async def wrapped_command(ctx: commands.Context, *args, **kwargs):
            if ctx.guild:
                missing_perms = [perm for perm in required_perms if
                                 not getattr(ctx.guild.me.guild_permissions, perm, False)]
                if missing_perms:
                    raise PermissionsMissingError(missing_perms)

            await callback(ctx, *args, **kwargs)

        self.commands[command_name] = {
            "callback": callback,
            "required_intents": required_intents,
            "required_perms": required_perms,
            "cooldown": cooldown,
            "legacy": True,
        }

    def get_command(self, name: str):
        return self.commands.get(name)