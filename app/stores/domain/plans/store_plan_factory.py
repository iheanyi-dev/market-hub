"""
Store Plan Factory.

Creates StorePlan instances from their identifiers.
"""

from __future__ import annotations

from app.stores.domain.exceptions.invalid_store_plan_error import (
    InvalidStorePlanError,
)
from app.stores.domain.plans.professional_plan import ProfessionalPlan
from app.stores.domain.plans.starter_plan import StarterPlan
from app.stores.domain.plans.store_plan import StorePlan


class StorePlanFactory:
    """
    Factory for creating StorePlan instances.
    """

    _PLANS: dict[str, type[StorePlan]] = {
        "starter": StarterPlan,
        "professional": ProfessionalPlan,
    }

    @classmethod
    def create(cls, plan: str) -> StorePlan:
        """
        Create a StorePlan from its identifier.

        Args:
            plan:
                The plan identifier.

        Returns:
            A StorePlan instance.

        Raises:
            InvalidStorePlanError:
                If the requested plan is not supported.
        """
        normalized_plan = plan.strip().lower()

        try:
            plan_type = cls._PLANS[normalized_plan]
        except KeyError as exc:
            raise InvalidStorePlanError(
                f"Unsupported store plan: '{plan}'."
            ) from exc

        return plan_type()