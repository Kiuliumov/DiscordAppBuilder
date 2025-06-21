from typing import Callable

import discord
import inspect
from events.valid_events import DiscordEvents
from exceptions.EventExceptions import EventHandlerException, InvalidEventError



class EventManager:
    def __init__(self, bot: discord.Client, tree: discord.app_commands.CommandTree):
        self.bot = bot
        self.tree = tree
        self.EVENTS = DiscordEvents()

    def _validate_event_name(self, event_name: str):
        if event_name not in self.EVENTS.events:
            raise InvalidEventError(event_name)

    def _validate_handler_signature(self, event_name: str, handler: Callable):
        expected_params = self.EVENTS.events.get(event_name, None)
        if expected_params is None:
            raise InvalidEventError("The event " + event_name + " has no handler.");

        if not inspect.iscoroutinefunction(handler):
            raise EventHandlerException(f"Handler for '{event_name}' must be an async function.")

        sig = inspect.signature(handler)
        params = list(sig.parameters.values())

        # Check if handler has at least expected parameters
        if len(params) < len(expected_params):
            raise EventHandlerException(
                f"Handler for '{event_name}' expects at least {len(expected_params)} "
                f"parameter(s) {expected_params}, but handler has {len(params)}."
            )

    def register_event(self, event_name: str, handler: Callable):
        """
        Register a callback function as a handler for a specific Discord event.

        Args:
            event_name (str): The name of the Discord event to register (e.g., "on_message").
            handler (Callable): The async function that will be called when the event occurs.

        Raises:
            InvalidEventError: If the event_name is not a recognized Discord event.
            EventHandlerException: If the handler function is invalid (wrong signature or not async).
        """
        self._validate_event_name(event_name)
        self._validate_handler_signature(event_name, handler)

        try:
            self.bot.event(handler)

            setattr(self.bot, event_name, handler)
        except Exception as e:
            raise EventHandlerException(f"Failed to register handler for '{event_name}': {e}")