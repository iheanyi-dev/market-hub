"""
Create Store Command.

Carries the data required to create a new store.
"""

from dataclasses import dataclass

from app.users.domain.value_objects.user_id import UserId


@dataclass(slots=True, frozen=True)
class CreateStoreCommand:
    """
    Input data for CreateStoreUseCase.
    """

    user_id: UserId
    name: str
    slug: str
    description: str
    plan: str