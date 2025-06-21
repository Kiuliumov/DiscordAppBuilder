# This exception is invoked whenever someone tries to run a command with insufficient permissions.


class PermissionsMissingError(Exception):
    def __init__(self, missing):
        super().__init__(f"Bot is missing permissions: {', '.join(missing)}")