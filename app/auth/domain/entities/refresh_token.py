from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass
class RefreshToken:
    """
    Domain entity representing a refresh token.
    """

    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    is_revoked: bool = field(default=False)

    def is_expired(self) -> bool:
        """
        Returns True if the refresh token has expired.
        """
        return datetime.now(UTC) >= self.expires_at

    def revoke(self) -> None:
        """
        Revokes the refresh token.
        """
        self.is_revoked = True

    @classmethod
    def create(
        cls,
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> "RefreshToken":
        """
        Factory method for creating a new refresh token.
        """
        return cls(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )