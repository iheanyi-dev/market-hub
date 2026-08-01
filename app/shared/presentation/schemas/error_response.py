"""
Standard API error response schema.
"""

from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    message: str
    timestamp: datetime