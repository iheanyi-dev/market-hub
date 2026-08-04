"""
Unit tests for the StarterPlan.
"""

import pytest

from app.stores.domain.exceptions.store_product_limit_exceeded_error import (
    StoreProductLimitExceededError,
)
from app.stores.domain.plans.starter_plan import StarterPlan


def test_starter_plan_name() -> None:
    plan = StarterPlan()

    assert plan.name == "Starter"


def test_starter_plan_max_products() -> None:
    plan = StarterPlan()

    assert plan.max_products == 20


def test_can_add_product_before_limit() -> None:
    plan = StarterPlan()

    assert plan.can_add_product(19) is True


def test_cannot_add_product_at_limit() -> None:
    plan = StarterPlan()

    assert plan.can_add_product(20) is False


def test_ensure_can_add_product_does_not_raise() -> None:
    plan = StarterPlan()

    plan.ensure_can_add_product(19)


def test_ensure_can_add_product_raises() -> None:
    plan = StarterPlan()

    with pytest.raises(StoreProductLimitExceededError):
        plan.ensure_can_add_product(20)

def test_starter_plan_code() -> None:
    plan = StarterPlan()

    assert plan.code == "starter"