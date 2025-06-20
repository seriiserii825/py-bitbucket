class BitbucketApiException(Exception):
    """Custom exception for Bitbucket API errors."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code
