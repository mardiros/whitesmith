import pytest
from blacksmith import (
    HTTPError,
    HTTPRequest,
    HTTPResponse,
    HTTPTimeout,
)

from whitesmith.router import Router, RouterBuilder
from whitesmith.transport import AsyncFakeTransport, SyncFakeTransport


@pytest.fixture
def router() -> Router:
    from tests import whitesmith_handlers

    builder = RouterBuilder()
    return builder.build_router(whitesmith_handlers)


def test_sync_transport_call(router: Router):
    resp = SyncFakeTransport(router)(
        HTTPRequest("POST", "http://notif.v2/notifications"),
        "notif",
        "/notifications",
        HTTPTimeout(),
    )
    assert resp == HTTPResponse(status_code=200, headers={}, json=None)


def test_sync_transport_call_error(router: Router):
    with pytest.raises(HTTPError) as err:
        SyncFakeTransport(router)(
            HTTPRequest("POST", "http://yolo.v1/"),
            "yolo",
            "/",
            HTTPTimeout(),
        )
    assert err.value.json == {
        "message": "Unregister whitesmith route: POST http://yolo.v1/",
    }


async def test_async_transport_call(router: Router):
    resp = await AsyncFakeTransport(router)(
        HTTPRequest("POST", "http://notif.v2/notifications"),
        "notif",
        "/notifications",
        HTTPTimeout(),
    )
    assert resp == HTTPResponse(status_code=200, headers={}, json=None)


async def test_async_transport_call_error(router: Router):
    with pytest.raises(HTTPError) as err:
        await AsyncFakeTransport(router)(
            HTTPRequest("POST", "http://yolo.v1/"),
            "yolo",
            "/",
            HTTPTimeout(),
        )
    assert err.value.json == {
        "message": "Unregister whitesmith route: POST http://yolo.v1/",
    }
