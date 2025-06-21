from typing import Dict


class ConfigManager:
    def __init__(self):
        self.guild_configs: Dict[int, dict] = {}

    def get_config(self, guild_id: int) -> dict:
        return self.guild_configs.setdefault(guild_id, {})

    def set_config(self, guild_id: int, data: dict):
        self.guild_configs[guild_id] = data