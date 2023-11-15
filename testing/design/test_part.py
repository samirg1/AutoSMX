from design.Part import Part


def test_part() -> None:
    p = Part("123", "manu", "manu_number", "desc")
    assert p.description == "desc"
    assert p.manufacturer == "manu"
    assert p.manufacturer_number == "manu_number"
    assert p.number == "123"
    assert repr(p) == "PN: 123, desc"