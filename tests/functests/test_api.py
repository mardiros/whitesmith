from typing import Any

from blacksmith import AsyncClientFactory
from blacksmith.service._sync.client import SyncClientFactory

from tests.resources.address.phonenumbers import GetPhone, Phone
from tests.resources.organization.user import CollectionGetUser


def test_sync_blacksmith_client(sync_blacksmith_client: SyncClientFactory[Phone]):
    address = sync_blacksmith_client("address")
    resp = address.phonenumbers.get(GetPhone(phonenumber="0611223344", country="FR"))
    assert resp.unwrap() == Phone(
        international=resp.json["international"],  # type: ignore
    )


def test_list_collection(sync_blacksmith_client: SyncClientFactory[Any]):
    organization = sync_blacksmith_client("organization")
    resp = organization.users.collection_get(CollectionGetUser(per_page=2))
    assert len(list(resp.unwrap())) == 1


async def test_async_blacksmith_client(
    async_blacksmith_client: AsyncClientFactory[Phone],
):
    address = await async_blacksmith_client("address")
    resp = await address.phonenumbers.get(
        GetPhone(phonenumber="0611223344", country="FR")
    )
    assert resp.unwrap() == Phone(
        international=resp.json["international"],  # type: ignore
    )


async def test_async_list_collection(async_blacksmith_client: AsyncClientFactory[Any]):
    organization = await async_blacksmith_client("organization")
    resp = await organization.users.collection_get(CollectionGetUser(per_page=2))
    assert len(list(resp.unwrap())) == 1
