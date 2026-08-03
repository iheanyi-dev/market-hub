from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshTokenCommand:
    """
    Request to refresh an access token.
    """

    refresh_token: str