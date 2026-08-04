"""
Unit tests for the ProfessionalPlan.
"""

import pytest

from app.stores.domain.exceptions.store_product_limit_exceeded_error import (
    StoreProductLimitExceededError,
)
from app.stores.domain.plans.professional_plan import ProfessionalPlan


def test_professional_plan_name() -> None:
    plan = ProfessionalPlan()

    assert plan.name == "Professional"


def test_professional_plan_max_products() -> None:
    plan = ProfessionalPlan()

    assert plan.max_products == 500


def test_can_add_product_before_limit() -> None:
    plan = ProfessionalPlan()

    assert plan.can_add_product(499) is True


def test_cannot_add_product_at_limit() -> None:
    plan = ProfessionalPlan()

    assert plan.can_add_product(500) is False


def test_ensure_can_add_product_does_not_raise() -> None:
    plan = ProfessionalPlan()

    plan.ensure_can_add_product(499)


def test_ensure_can_add_product_raises() -> None:
    plan = ProfessionalPlan()

    with pytest.raises(StoreProductLimitExceededError):
        plan.ensure_can_add_product(500)

def test_professional_plan_code() -> None:
    plan = ProfessionalPlan()

    assert plan.code == "professional"