import pytest

from app.stores.domain.value_objects.store_slug import StoreSlug


def test_create_valid_slug() -> None:
    slug = StoreSlug.create("my-store")

    assert slug.value == "my-store"


def test_slug_is_normalized() -> None:
    slug = StoreSlug.create("  My-Store ")

    assert slug.value == "my-store"


@pytest.mark.parametrize(
    "slug",
    [
        "",
        "My Store",
        "my_store",
        "my@store",
        "admin",
        "api",
        "login",
    ],
)
def test_invalid_slug_raises(slug: str) -> None:
    with pytest.raises(ValueError):
        StoreSlug.create(slug)