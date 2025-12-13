"""Pytest plugin"""

import importlib
from typing import Any

import blacksmith
import pytest

from whitesmith import Router
from whitesmith.router import RouterBuilder
from whitesmith.transport import AsyncFakeTransport, SyncFakeTransport

HANDLERS: dict[str, Router | None] = {}


@pytest.fixture()
def whitesmith_router(request: pytest.FixtureRequest) -> Router:
    mods: list[str] = request.module.__package__.split(".")
    mods.pop()  # we don't look at the file
    full_modname = ""
    while mods:
        full_modname = f"{'.'.join(mods)}.whitesmith_handlers"
        if full_modname in HANDLERS:
            break
        try:
            mod = importlib.import_module(full_modname)
            router = RouterBuilder().build_router(mod)
        except ImportError:
            HANDLERS[full_modname] = None
            mods.pop()
        else:
            HANDLERS[full_modname] = router
            break

    handler = HANDLERS.get(full_modname)
    assert handler is not None, "no whitesmith_handlers fund, did you generates some?"
    return handler


@pytest.fixture()
def sync_blacksmith_client(
    whitesmith_router: Router,
) -> blacksmith.SyncClientFactory[Any]:
    sd = blacksmith.SyncRouterDiscovery(
        service_url_fmt="http://{service}.{version}",
        unversioned_service_url_fmt="http://{service}.NaN",
    )
    return blacksmith.SyncClientFactory(
        sd=sd, transport=SyncFakeTransport(whitesmith_router)
    )


@pytest.fixture()
def async_blacksmith_client(
    whitesmith_router: Router,
) -> blacksmith.AsyncClientFactory[Any]:
    sd = blacksmith.AsyncRouterDiscovery(
        service_url_fmt="http://{service}.{version}",
        unversioned_service_url_fmt="http://{service}.NaN",
    )
    return blacksmith.AsyncClientFactory(
        sd=sd, transport=AsyncFakeTransport(whitesmith_router)
    )
