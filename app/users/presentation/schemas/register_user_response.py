"""
Response schema for user registration.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    Response returned after successful user registration.
    """

    id: UUID
    full_name: str
    email: str
    role: str
    status: str
    created_at: datetime
    updated_at: datetime