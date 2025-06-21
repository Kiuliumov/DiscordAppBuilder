
class RolesMissingError(Exception):
    def __init__(self, missing):
        super().__init__(f"User is missing required roles: {', '.join(missing)}")
        self.missing = missing