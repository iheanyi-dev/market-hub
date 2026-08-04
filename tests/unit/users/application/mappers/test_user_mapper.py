"""
Unit tests for the UserMapper.
"""

from app.users.application.mappers.user_mapper import UserMapper
from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName


class TestUserMapper:
    """
    Test suite for the UserMapper.
    """

    def test_to_register_result(self) -> None:
        """
        Verify a User aggregate is correctly mapped to RegisterUserResult.
        """
        user = User.create(
            full_name=FullName.create("John Doe"),
            email=Email.create("john@example.com"),
            password_hash="hashed-password",
        )

        result = UserMapper.to_register_result(user)

        assert result.id == user.id.value
        assert result.full_name == "John Doe"
        assert result.email == "john@example.com"
        assert result.role == "customer"
        assert result.status == "active"
        assert result.created_at == user.created_at
        assert result.updated_at == user.updated_at