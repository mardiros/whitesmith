import pytest
from blacksmith import (
    HTTPError,
    HTTPRequest,
    HTTPResponse,
    HTTPTimeout,
)

from whitesmith.transport import AsyncFakeTransport, SyncFakeTransport


def test_sync_transport_call():
    resp = SyncFakeTransport()(
        HTTPRequest("POST", "http://notif.v2/notifications"),
        "notif",
        "/notifications",
        HTTPTimeout(),
    )
    assert resp == HTTPResponse(status_code=200, headers={}, json=None)


def test_sync_transport_call_error():
    with pytest.raises(HTTPError) as err:
        SyncFakeTransport()(
            HTTPRequest("POST", "http://yolo.v1/"),
            "yolo",
            "/",
            HTTPTimeout(),
        )
    assert err.value.json == {
        "message": "Unregister whitesmith route: POST http://yolo.v1/",
    }


async def test_async_transport_call():
    resp = await AsyncFakeTransport()(
        HTTPRequest("POST", "http://notif.v2/notifications"),
        "notif",
        "/notifications",
        HTTPTimeout(),
    )
    assert resp == HTTPResponse(status_code=200, headers={}, json=None)


async def test_async_transport_call_error():
    with pytest.raises(HTTPError) as err:
        await AsyncFakeTransport()(
            HTTPRequest("POST", "http://yolo.v1/"),
            "yolo",
            "/",
            HTTPTimeout(),
        )
    assert err.value.json == {
        "message": "Unregister whitesmith route: POST http://yolo.v1/",
    }
