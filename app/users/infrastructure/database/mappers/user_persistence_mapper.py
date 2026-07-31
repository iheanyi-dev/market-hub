"""
User Persistence Mapper.

This module maps between the User aggregate and the SQLAlchemy UserModel.
"""

from app.users.domain.entities.user import User
from app.users.domain.value_objects.email import Email
from app.users.domain.value_objects.full_name import FullName
from app.users.domain.value_objects.user_id import UserId
from app.users.infrastructure.database.models.user_model import UserModel


class UserPersistenceMapper:
    """
    Maps between User aggregates and UserModel persistence objects.
    """
    @staticmethod
    def to_model(user: User) -> UserModel:
        """
        Convert a User aggregate into a UserModel.
        """
        return UserModel(
            id=user.id.value,
            full_name=user.full_name.value,
            email=user.email.value,
            password_hash=user.password_hash,
            role=user.role,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def to_domain(model: UserModel) -> User:
        """
        Convert a UserModel into a User aggregate.
        """
        return User.reconstitute(
            user_id=UserId(model.id),
            full_name=FullName.create(model.full_name),
            email=Email.create(model.email),
            password_hash=model.password_hash,
            role=model.role,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )