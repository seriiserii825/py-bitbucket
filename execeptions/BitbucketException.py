class BitbucketException(Exception):
    """Base class for exceptions in the Bitbucket API module."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
