from dataclasses import dataclass


@dataclass(frozen=True)
class RefreshTokenResult:
    """
    Tokens returned after a successful refresh.
    """

    access_token: str
    refresh_token: str