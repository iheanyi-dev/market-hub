"""
Unit tests for the UserPersistenceMapper.
"""

from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.infrastructure.database.mappers.user_persistence_mapper import (
    UserPersistenceMapper,
)


class TestUserPersistenceMapper:
    """
    Test suite for the UserPersistenceMapper.
    """

    def test_to_model(self) -> None:
        """
        Verify a User aggregate is correctly mapped to a UserModel.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        model = UserPersistenceMapper.to_model(user)

        assert str(model.id) == str(user.id)
        assert model.full_name == "John Doe"
        assert model.email == "john@example.com"
        assert model.password_hash == "hashed-password"
        assert model.role == user.role
        assert model.status == user.status
        assert model.created_at == user.created_at
        assert model.updated_at == user.updated_at

    def test_to_domain(self) -> None:
        """
        Verify a UserModel is correctly mapped back to a User aggregate.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        model = UserPersistenceMapper.to_model(user)

        restored = UserPersistenceMapper.to_domain(model)

        assert restored.id == user.id
        assert restored.full_name == user.full_name
        assert restored.email == user.email
        assert restored.password_hash == user.password_hash
        assert restored.role == user.role
        assert restored.status == user.status
        assert restored.created_at == user.created_at
        assert restored.updated_at == user.updated_at