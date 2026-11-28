from typing import Literal, overload

from blacksmith import (
    AsyncBaseClient,
    AsyncClientFactory,
    AsyncRouteProxy,
    HTTPError,
    SyncBaseClient,
    SyncClientFactory,
    SyncRouteProxy,
)

from tests.resources.address.phonenumbers import Phone
from tests.resources.organization.users import PartialUser, User


class AsyncAddressClient(AsyncBaseClient[HTTPError]):
    phonenumbers: AsyncRouteProxy[None, Phone, HTTPError]


class AsyncNotifClient(AsyncBaseClient[HTTPError]):
    notifications: AsyncRouteProxy[None, None, HTTPError]


class AsyncOrganizationClient(AsyncBaseClient[HTTPError]):
    users: AsyncRouteProxy[PartialUser, User, HTTPError]


class AsyncAppClientFactory(
    AsyncClientFactory[Literal["address", "notif", "organization"], HTTPError]
):
    @overload
    async def __call__(self, client_name: Literal["address"]) -> AsyncAddressClient: ...

    @overload
    async def __call__(
        self, client_name: Literal["organization"]
    ) -> AsyncOrganizationClient: ...

    @overload
    async def __call__(self, client_name: Literal["notif"]) -> AsyncNotifClient: ...

    async def __call__(
        self, client_name: Literal["address", "notif", "organization"]
    ) -> AsyncBaseClient[HTTPError]:
        return await super().__call__(client_name)


class SyncAddressClient(SyncBaseClient[HTTPError]):
    phonenumbers: SyncRouteProxy[None, Phone, HTTPError]


class SyncNotifClient(SyncBaseClient[HTTPError]):
    notifications: SyncRouteProxy[None, None, HTTPError]


class SyncOrganizationClient(SyncBaseClient[HTTPError]):
    users: SyncRouteProxy[PartialUser, User, HTTPError]


class SyncAppClientFactory(
    SyncClientFactory[Literal["address", "notif", "organization"], HTTPError]
):
    @overload
    def __call__(self, client_name: Literal["address"]) -> SyncAddressClient: ...

    @overload
    def __call__(
        self, client_name: Literal["organization"]
    ) -> SyncOrganizationClient: ...

    @overload
    def __call__(self, client_name: Literal["notif"]) -> SyncNotifClient: ...

    def __call__(
        self, client_name: Literal["address", "notif", "organization"]
    ) -> SyncBaseClient[HTTPError]:
        return super().__call__(client_name)
