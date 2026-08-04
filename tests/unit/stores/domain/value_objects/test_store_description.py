import pytest

from app.stores.domain.value_objects.store_description import StoreDescription


def test_create_valid_description() -> None:
    description = StoreDescription("My awesome store.")

    assert description.value == "My awesome store."


def test_description_is_trimmed() -> None:
    description = StoreDescription("  Hello  ")

    assert description.value == "Hello"


def test_empty_description_is_allowed() -> None:
    description = StoreDescription("")

    assert description.value == ""


def test_description_too_long_raises() -> None:
    with pytest.raises(ValueError):
        StoreDescription("a" * 1001)