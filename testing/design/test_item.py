# pyright: reportPrivateUsage=false
from design.Item import Item


def test_item_creation_and_properties() -> None:
    item = Item("123", "Test Item", "Model123", "Test Manufacturer", "ABC456", "RM1", "2019")

    assert item.number == "123"
    assert item.description == "Test Item"
    assert item.model == "Model123"
    assert item.manufacturer == "Test Manufacturer"
    assert item.serial == "ABC456"
    assert item.room == "RM1"
    assert item.last_update == "2019"


def test_item_string_representation() -> None:
    item = Item("789", "Another Item", "Model789", "Another Manufacturer", "DEF789", "RM1", "2019")

    assert str(item) == "789 - Another Item"


def test_item_hashing_and_eq() -> None:
    item1 = Item("111", "Item A", "ModelA", "ManufacturerA", "AAA111", "RM1", "2019")
    item2 = Item("222", "Item B", "ModelB", "ManufacturerB", "BBB222", "RM1", "2019")
    item3 = Item("111", "Item C", "ModelC", "ManufacturerC", "CCC333", "RM1", "2019")

    assert len({item1, item2}) == 2
    assert len({item1, item3}) == 1
    assert hash(item1) != hash(item2)
    assert hash(item1) == hash(item3)
