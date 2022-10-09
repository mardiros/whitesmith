import blacksmith

from whitesmith.transport import AsyncFakeTransport, SyncFakeTransport

blacksmith.scan("tests.resources")
blacksmith.scan(f"{__package__}.handlers")


def sync_whitesmith_client() -> blacksmith.SyncClientFactory:
    sd = blacksmith.SyncRouterDiscovery(
        service_url_fmt="http://{service}.{version}",
        unversioned_service_url_fmt="http://{service}.NaN",
    )
    return blacksmith.SyncClientFactory(sd=sd, transport=SyncFakeTransport())


def async_whitesmith_client() -> blacksmith.AsyncClientFactory:
    sd = blacksmith.AsyncRouterDiscovery(
        service_url_fmt="http://{service}.{version}",
        unversioned_service_url_fmt="http://{service}.NaN",
    )
    return blacksmith.AsyncClientFactory(sd=sd, transport=AsyncFakeTransport())
