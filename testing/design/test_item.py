# pyright: reportPrivateUsage=false
from design.Item import Item


def test_item_creation_and_properties():
    item = Item(number="123", description="Test Item", model="Model123", manufacturer="Test Manufacturer", serial="ABC456")

    assert item.number == "123"
    assert item.description == "Test Item"
    assert item.model == "Model123"
    assert item.manufacturer == "Test Manufacturer"
    assert item.serial == "ABC456"


def test_item_string_representation():
    item = Item(number="789", description="Another Item", model="Model789", manufacturer="Another Manufacturer", serial="DEF789")

    assert str(item) == "789 - Another Item"


def test_item_hashing_and_eq():
    item1 = Item("111", "Item A", "ModelA", "ManufacturerA", "AAA111")
    item2 = Item("222", "Item B", "ModelB", "ManufacturerB", "BBB222")
    item3 = Item("111", "Item C", "ModelC", "ManufacturerC", "CCC333")

    assert len({item1, item2}) == 2
    assert len({item1, item3}) == 1
    assert hash(item1) != hash(item2)
    assert hash(item1) == hash(item3)
