"""
Shared pytest fixtures.
"""

import pytest

from tests.fakes.fake_user_repository import FakeUserRepository


@pytest.fixture
def user_repository() -> FakeUserRepository:
    """
    Return a fresh in-memory user repository for each test.
    """
    return FakeUserRepository()