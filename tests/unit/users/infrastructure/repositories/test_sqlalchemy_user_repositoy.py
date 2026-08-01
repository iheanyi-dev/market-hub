"""
Integration tests for the SqlAlchemyUserRepository.
"""

from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName


class TestSqlAlchemyUserRepository:
    """
    Integration tests for the SQLAlchemy repository.
    """
    async def test_save_user(
        self,
        user_repository,
    ) -> None:
        """
        A user should be persisted successfully.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        await user_repository.save(user)

        exists = await user_repository.exists_by_email(
            Email.create("john@example.com")
        )

        assert exists is True

    async def test_get_user_by_email(
        self,
        user_repository,
    ) -> None:
        """
        A persisted user should be retrievable by email.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        await user_repository.save(user)

        stored = await user_repository.get_by_email(
            Email.create("john@example.com")
        )

        assert stored is not None
        assert stored.id == user.id
        assert stored.email == user.email
        assert stored.full_name == user.full_name

    async def test_get_unknown_email_returns_none(
        self,
        user_repository,
    ) -> None:
        """
        Retrieving an unknown email should return None.
        """
        stored = await user_repository.get_by_email(
            Email.create("unknown@example.com")
        )

        assert stored is None