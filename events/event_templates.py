from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class DiscordEvents:
    """
    Holds valid Discord event names with their expected handler parameter names.
    """
    events: Dict[str, List[str]] = None

    def __post_init__(self):
        object.__setattr__(self, "events", {
            # Bot lifecycle events
            "on_ready": [],
            "on_connect": [],
            "on_disconnect": [],
            "on_resumed": [],
            "on_error": ["event", "args", "kwargs"],

            # Message events
            "on_message": ["message"],
            "on_message_edit": ["before", "after"],
            "on_message_delete": ["message"],
            "on_bulk_message_delete": ["messages"],

            # Reaction events
            "on_reaction_add": ["reaction", "user"],
            "on_reaction_remove": ["reaction", "user"],
            "on_reaction_clear": ["message", "reactions"],
            "on_reaction_clear_emoji": ["reaction", "user"],

            # Member events
            "on_member_join": ["member"],
            "on_member_remove": ["member"],
            "on_member_update": ["before", "after"],
            "on_user_update": ["before", "after"],
            "on_guild_join": ["guild"],
            "on_guild_remove": ["guild"],
            "on_guild_update": ["before", "after"],

            # Guild role events
            "on_guild_role_create": ["role"],
            "on_guild_role_delete": ["role"],
            "on_guild_role_update": ["before", "after"],

            # Guild channel events
            "on_guild_channel_create": ["channel"],
            "on_guild_channel_delete": ["channel"],
            "on_guild_channel_update": ["before", "after"],

            # Voice events
            "on_voice_state_update": ["member", "before", "after"],

            # Command events (discord.ext.commands)
            "on_command": ["ctx"],
            "on_command_completion": ["ctx"],
            "on_command_error": ["ctx", "error"],
            "on_help_command": ["ctx", "command"],

            # Presence and typing
            "on_typing": ["channel", "user", "when"],
            "on_presence_update": ["before", "after"],

            # Invite events
            "on_invite_create": ["invite"],
            "on_invite_delete": ["invite"],

            # Raw events
            "on_raw_reaction_add": ["payload"],
            "on_raw_reaction_remove": ["payload"],
            "on_raw_reaction_clear": ["payload"],
            "on_raw_reaction_clear_emoji": ["payload"],
            "on_raw_message_edit": ["payload"],
            "on_raw_message_delete": ["payload"],
            "on_raw_message_delete_bulk": ["payloads"],
        })
