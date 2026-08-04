"""
Unit tests for StorePlanFactory.
"""

import pytest

from app.stores.domain.exceptions.invalid_store_plan_error import (
    InvalidStorePlanError,
)
from app.stores.domain.plans.professional_plan import ProfessionalPlan
from app.stores.domain.plans.starter_plan import StarterPlan
from app.stores.domain.plans.store_plan_factory import StorePlanFactory


def test_create_starter_plan() -> None:
    """
    A StarterPlan should be created from its identifier.
    """
    plan = StorePlanFactory.create("starter")

    assert isinstance(plan, StarterPlan)


def test_create_professional_plan() -> None:
    """
    A ProfessionalPlan should be created from its identifier.
    """
    plan = StorePlanFactory.create("professional")

    assert isinstance(plan, ProfessionalPlan)


@pytest.mark.parametrize(
    "plan",
    [
        "",
        "gold",
        "enterprise",
        "premium",
        "unknown",
    ],
)
def test_invalid_plan_raises(plan: str) -> None:
    """
    An unsupported plan should raise InvalidStorePlanError.
    """
    with pytest.raises(InvalidStorePlanError):
        StorePlanFactory.create(plan)


def test_plan_lookup_is_case_insensitive() -> None:
    """
    Plan lookup should ignore character casing.
    """
    assert isinstance(
        StorePlanFactory.create("Starter"),
        StarterPlan,
    )

    assert isinstance(
        StorePlanFactory.create("PROFESSIONAL"),
        ProfessionalPlan,
    )