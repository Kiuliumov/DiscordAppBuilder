class InvalidEventError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EventHandlerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
