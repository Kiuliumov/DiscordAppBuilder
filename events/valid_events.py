from dataclasses import field, dataclass
from typing import Set


@dataclass(frozen=True)
class DiscordEvents:
    events: Set[str] = field(default_factory=lambda: {
        "on_ready",
        "on_connect",
        "on_disconnect",
        "on_resumed",
        "on_error",
        "on_shard_connect",
        "on_shard_disconnect",
        "on_shard_ready",
        "on_shard_resume",

        "on_message",
        "on_message_edit",
        "on_message_delete",
        "on_bulk_message_delete",
        "on_reaction_add",
        "on_reaction_remove",
        "on_reaction_clear",
        "on_reaction_clear_emoji",

        "on_guild_join",
        "on_guild_remove",
        "on_guild_update",
        "on_guild_available",
        "on_guild_unavailable",
        "on_guild_role_create",
        "on_guild_role_delete",
        "on_guild_role_update",
        "on_guild_emojis_update",
        "on_guild_stickers_update",
        "on_guild_integrations_update",

        "on_member_join",
        "on_member_remove",
        "on_member_update",
        "on_user_update",

        "on_voice_state_update",
        "on_voice_server_update",

        "on_typing",

        "on_presence_update",

        "on_invite_create",
        "on_invite_delete",

        "on_webhooks_update",

        "on_integration_create",
        "on_integration_update",
        "on_integration_delete",

        "on_private_channel_delete",
        "on_private_channel_create",
        "on_private_channel_update",
        "on_relationship_add",
        "on_relationship_remove",
        "on_relationship_update",
    })