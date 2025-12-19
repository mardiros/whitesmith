from typing import Any

from blacksmith import AsyncClientFactory, SyncClientFactory

from whitesmith import Router


async def test_router(whitesmith_router: Router):
    assert sorted(whitesmith_router.routes.keys()) == [
        (
            "GET",
            "http://address.NaN/phonenumbers/{phonenumber}",
        ),
        (
            "GET",
            "http://organization.v5/users",
        ),
        (
            "GET",
            "http://organization.v5/users/{user_id}",
        ),
        (
            "PATCH",
            "http://organization.v5/users/{user_id}",
        ),
        (
            "POST",
            "http://notif.v2/notifications",
        ),
        (
            "POST",
            "http://organization.v5/users",
        ),
    ]


async def test_async(async_blacksmith_client: AsyncClientFactory[Any]):
    cli = await async_blacksmith_client("organization")
    assert cli.endpoint == "http://organization.v5"


def test_sync(sync_blacksmith_client: SyncClientFactory[Any]):
    cli = sync_blacksmith_client("organization")
    assert cli.endpoint == "http://organization.v5"
