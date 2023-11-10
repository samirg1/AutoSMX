import http.client as httplib


def connected_to_internet() -> bool:
    connection = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        connection.request("HEAD", "/")
        return True
    except OSError:
        return False
    finally:
        connection.close()
