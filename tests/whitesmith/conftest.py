import blacksmith
import pytest

from .fixtures import async_whitesmith_client, sync_whitesmith_client


@pytest.fixture
def sync_client() -> blacksmith.SyncClientFactory:
    return sync_whitesmith_client()


@pytest.fixture
def async_client() -> blacksmith.AsyncClientFactory:
    return async_whitesmith_client()
