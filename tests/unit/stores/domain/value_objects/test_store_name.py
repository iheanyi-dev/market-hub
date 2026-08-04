import pytest

from app.stores.domain.value_objects.store_name import StoreName


def test_create_valid_store_name() -> None:
    name = StoreName("My Store")

    assert name.value == "My Store"


def test_store_name_is_trimmed() -> None:
    name = StoreName("  My Store  ")

    assert name.value == "My Store"


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_empty_store_name_raises(value: str) -> None:
    with pytest.raises(ValueError):
        StoreName(value)


def test_store_name_too_short_raises() -> None:
    with pytest.raises(ValueError):
        StoreName("ab")


def test_store_name_too_long_raises() -> None:
    with pytest.raises(ValueError):
        StoreName("a" * 101)