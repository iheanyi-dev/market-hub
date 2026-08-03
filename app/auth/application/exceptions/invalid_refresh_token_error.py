class InvalidRefreshTokenError(Exception):
    """
    Raised when a refresh token is invalid, expired, or revoked.
    """

    def __init__(self) -> None:
        super().__init__("Invalid refresh token.")