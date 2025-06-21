# Defines an exception that is raised each time a command is entered with insufficient intents.

class IntentsMissingError(Exception):

    def __init__(self, missing):
        self.missing = missing
        super().__init__(f"Missing required intents: {', '.join(missing)}")