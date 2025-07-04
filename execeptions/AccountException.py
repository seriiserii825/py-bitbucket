class AccountException(Exception):
    """Base class for exceptions in the account module."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
