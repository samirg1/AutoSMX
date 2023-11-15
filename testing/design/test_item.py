from datetime import datetime, timedelta
from design.Item import Item
from utils.constants import DAYMONTHYEAR_FORMAT, SIMPLIFIED_TIME_FORMAT
from utils.get_sysmodtime import get_sysmodtime


def test_item_creation_and_properties() -> None:
    item = Item("123", "123A", "Test Item", "Model123", "Test Manufacturer", "ABC456", "RM1", "2019-01-01 03:45:44.759")

    assert item.number == "123"
    assert item.customer_barcode == "123A"
    assert item.description == "Test Item"
    assert item.model == "Model123"
    assert item.manufacturer == "Test Manufacturer"
    assert item.serial == "ABC456"
    assert item.room == "RM1"
    assert item.last_update
    assert item.last_update.strftime(f"{DAYMONTHYEAR_FORMAT} {SIMPLIFIED_TIME_FORMAT}") == "01-01-2019 03:45AM"
    assert item.full_info == "123 - Test Item - Model: Model123 - Manufacturer: Test Manufacturer - SN: ABC456 - Last Update: 01-01-2019 03:45AM"

    item = Item("123", "123A", "Test Item", "Model123", "Test Manufacturer", "ABC456", "RM1", get_sysmodtime(datetime.today()))
    assert "Today" in item.full_info.split(" - ")[-1]
    item = Item("123", "123A", "Test Item", "Model123", "Test Manufacturer", "ABC456", "RM1", get_sysmodtime(datetime.today() - timedelta(days=1)))
    assert "Yesterday" in item.full_info.split(" - ")[-1]

    item.set_room("123")
    assert item.room == "123"


def test_item_string_representation() -> None:
    item = Item("789", "789", "Another Item", "Model789", "Another Manufacturer", "DEF789", "RM1", None)

    assert str(item) == "789 - Another Item"
    assert item.last_update is None


def test_item_hashing_and_eq() -> None:
    item1 = Item("111", "111", "Item A", "ModelA", "ManufacturerA", "AAA111", "RM1", "2019-01-01 03:45:44.759")
    item2 = Item("222", "111", "Item B", "ModelB", "ManufacturerB", "BBB222", "RM1", "2019-01-01 03:45:44.759")
    item3 = Item("111", "111", "Item C", "ModelC", "ManufacturerC", "CCC333", "RM1", "2019-01-01 03:45:44.759")

    assert len({item1, item2}) == 2
    assert len({item1, item3}) == 1
    assert hash(item1) != hash(item2)
    assert hash(item1) == hash(item3)
