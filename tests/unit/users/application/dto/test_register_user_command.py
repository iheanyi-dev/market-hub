"""
Unit tests for the RegisterUserCommand DTO.
"""

from app.users.application.dto.register_user_command import (
    RegisterUserCommand,
)


class TestRegisterUserCommand:
    """
    Test suite for the RegisterUserCommand DTO.
    """

    def test_create_command(self) -> None:
        """
        Verify that a command stores the supplied registration data.
        """
        command = RegisterUserCommand(
            full_name="John Doe",
            email="john@example.com",
            password="StrongPass@123",
        )

        assert command.full_name == "John Doe"
        assert command.email == "john@example.com"
        assert command.password == "StrongPass@123"