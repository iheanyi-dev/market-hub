from uuid import UUID

from app.stores.domain.value_objects.store_id import StoreId


def test_create_store_id() -> None:
    store_id = StoreId.create()

    assert isinstance(store_id.value, UUID)


def test_create_store_id_from_string() -> None:
    original = StoreId.create()

    reconstructed = StoreId.from_string(str(original))

    assert reconstructed == original