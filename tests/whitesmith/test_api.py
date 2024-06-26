from tests.resources.address.phonenumbers import GetPhone, Phone
from tests.resources.organization.user import CollectionGetUser


def test_sync_client(sync_client):
    address = sync_client("address")
    resp = address.phonenumbers.get(GetPhone(phonenumber="0611223344", country="FR"))
    assert resp.unwrap() == Phone(international=resp.json["international"])


def test_list_collection(sync_client):
    organization = sync_client("organization")
    resp = organization.users.collection_get(CollectionGetUser(per_page=2))
    assert len(list(resp.unwrap())) == 1
