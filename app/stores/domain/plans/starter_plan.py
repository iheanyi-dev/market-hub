"""
Starter Store Plan.

Defines the capabilities and limits of the Starter plan.
"""

from app.stores.domain.plans.store_plan import StorePlan


class StarterPlan(StorePlan):
    """
    Starter plan.

    Intended for new vendors with a small product catalogue.
    """

    @property
    def name(self) -> str:
        """
        Return the plan name.
        """
        return "Starter"

    @property
    def code(self) -> str:
        return "starter"

    @property
    def max_products(self) -> int:
        """
        Return the maximum number of products allowed.
        """
        return 20