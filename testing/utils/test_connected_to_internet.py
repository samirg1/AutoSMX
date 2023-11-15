from utils.connected_to_internet import connected_to_internet
import pytest
import http.client

class MockHTTPObject:
    def __init__(self, value: bool) -> None:
        self.value = value
    
    def close(self):
        ...

    def request(self, x: str, y: str):
        if not self.value:
            raise OSError


def base(monkeypatch: pytest.MonkeyPatch, value: bool) -> MockHTTPObject:
    obj = MockHTTPObject(value)

    def mock_connect(url: str, timeout: int) -> MockHTTPObject:
        return obj

    monkeypatch.setattr(http.client, "HTTPSConnection", mock_connect)

    return obj

@pytest.fixture
def has_internet(monkeypatch: pytest.MonkeyPatch) -> MockHTTPObject:
    return base(monkeypatch, True)

@pytest.fixture
def has_no_internet(monkeypatch: pytest.MonkeyPatch) -> MockHTTPObject:
    return base(monkeypatch, False)

def test_connected_to_internet(has_internet: MockHTTPObject) -> None:
    assert connected_to_internet()

def test_not_connected_to_internet(has_no_internet: MockHTTPObject) -> None:
    assert not connected_to_internet()