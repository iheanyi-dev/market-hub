"""
Professional Store Plan.

Defines the capabilities and limits of the Professional plan.
"""

from app.stores.domain.plans.store_plan import StorePlan


class ProfessionalPlan(StorePlan):
    """
    Professional plan.

    Intended for growing businesses with a larger catalogue.
    """

    @property
    def name(self) -> str:
        """
        Return the plan name.
        """
        return "Professional"

    @property
    def code(self) -> str:
        return "professional"

    @property
    def max_products(self) -> int:
        """
        Return the maximum number of products allowed.
        """
        return 500