"""Pytest plugin"""

import sys
from typing import Any

import blacksmith
import pytest

from whitesmith import Router
from whitesmith.router import RouterBuilder
from whitesmith.transport import AsyncFakeTransport, SyncFakeTransport


@pytest.fixture()
def whitesmith_router(request: pytest.FixtureRequest) -> Router:
    modname = request.module.__package__.split(".")[0]
    mod = sys.modules[modname]
    return RouterBuilder().build_router(mod)


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
