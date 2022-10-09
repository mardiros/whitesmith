from tests.resources.address.phonenumbers import GetPhone, Phone

def test_sync_client(sync_client):
    address = sync_client("address")
    resp = address.phonenumbers.get(GetPhone(phonenumber="0611223344", country="FR"))
    assert resp.response == Phone(international=resp.json["international"])
