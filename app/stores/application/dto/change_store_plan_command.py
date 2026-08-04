"""
Application command for changing a store's subscription plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.stores.domain.plans.store_plan import StorePlan


@dataclass(slots=True, frozen=True)
class ChangeStorePlanCommand:
    """
    Command for changing a store's subscription plan.
    """

    owner_id: UUID
    plan: str