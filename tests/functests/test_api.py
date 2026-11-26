from tests.resources.address.phonenumbers import GetPhone, Phone
from tests.resources.blacksmith_client import (
    AsyncAppClientFactory,
    SyncAppClientFactory,
)
from tests.resources.organization.users import CollectionGetUser


def test_sync_blacksmith_client(sync_blacksmith_client: SyncAppClientFactory):
    address = sync_blacksmith_client("address")
    resp = address.phonenumbers.get(
        GetPhone(phonenumber="0611223344", country="FR"),
    )
    assert resp.unwrap() == Phone(
        international=resp.json["international"],  # type: ignore
    )


def test_list_collection(sync_blacksmith_client: SyncAppClientFactory):
    organization = sync_blacksmith_client("organization")
    resp = organization.users.collection_get(CollectionGetUser(per_page=2))
    assert len(list(resp.unwrap())) == 1


async def test_async_blacksmith_client(
    async_blacksmith_client: AsyncAppClientFactory,
):
    address = await async_blacksmith_client("address")
    resp = await address.phonenumbers.get(
        GetPhone(phonenumber="0611223344", country="FR")
    )
    assert resp.unwrap() == Phone(
        international=resp.json["international"],  # type: ignore
    )


async def test_async_list_collection(async_blacksmith_client: AsyncAppClientFactory):
    organization = await async_blacksmith_client("organization")
    resp = await organization.users.collection_get(CollectionGetUser(per_page=2))
    assert len(list(resp.unwrap())) == 1
