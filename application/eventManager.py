from typing import Optional, Callable

import discord

from events.valid_events import DiscordEvents
from exceptions.PermissionsMissingException import PermissionsMissingError
from exceptions.RolesMissingException import RolesMissingError



class EventManager:
    EVENTS = DiscordEvents()

    def __init__(self):
        self._on_ready_handler: Optional[Callable] = None
        self._on_error_handler: Optional[Callable] = None

    def _validate_event_name(self, event_name: str):
        if event_name not in self.EVENTS.events:
            raise InvalidEventError(event_name)

    def set_on_ready(self, handler: Callable):
        self._validate_event_name("on_ready")
        self._on_ready_handler = handler
        self.bot.event(self._on_ready_handler)

    def set_on_error(self, handler: Callable):
        self._validate_event_name("on_error")
        self._on_error_handler = handler
        self.tree.error(self._on_error_handler)

    async def __default_on_ready(self):
        print(f"✅ Logged in as {self.bot.user}")
        await self.tree.sync()

    async def __default_on_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, PermissionsMissingError):
            await interaction.response.send_message(
                f"❌ Missing permissions: {', '.join(error.missing)}",
                ephemeral=True
            )
        elif isinstance(error, RolesMissingError):
            await interaction.response.send_message(
                f"❌ You need roles: {', '.join(error.missing)}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"⚠️ Error: `{type(error).__name__}`",
                ephemeral=True
            )
