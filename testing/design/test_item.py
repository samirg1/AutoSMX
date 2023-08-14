# pyright: reportPrivateUsage=false
from design.Item import Item


def test_item_creation_and_properties():
    item = Item(number="123", description="Test Item", model="Model123", manufacturer="Test Manufacturer", room="Room A", last_service="2022-01-01", serial="ABC456")

    assert item.number == "123"
    assert item.description == "Test Item"
    assert item.model == "Model123"
    assert item.manufacturer == "Test Manufacturer"
    assert item.room == "Room A"
    assert item.last_service == "2022-01-01"
    assert item.serial == "ABC456"


def test_item_string_representation():
    item = Item(number="789", description="Another Item", model="Model789", manufacturer="Another Manufacturer", room="Room B", last_service="2022-02-15", serial="DEF789")

    assert str(item) == "789 - Another Item"


def test_item_full_info():
    item = Item(number="456", description="Yet Another Item", model="Model456", manufacturer="Yet Another Manufacturer", room="Room C", last_service="2022-03-10", serial="GHI012")

    expected_info = "456 - Yet Another Item\nModel: Model456\nManufacturer: Yet Another Manufacturer\nRoom: Room C\nLast Service: 2022-03-10\nSerial: GHI012"
    assert item.full_info() == expected_info


def test_item_hashing():
    item1 = Item("111", "Item A", "ModelA", "ManufacturerA", "Room X", "2022-01-01", "AAA111")
    item2 = Item("222", "Item B", "ModelB", "ManufacturerB", "Room Y", "2022-02-02", "BBB222")

    items_set = {item1, item2}

    assert len(items_set) == 2  # Ensure both items are considered distinct
