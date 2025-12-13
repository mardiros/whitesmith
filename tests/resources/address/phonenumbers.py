from blacksmith import PathInfoField, QueryStringField, Request, Response, register


class GetPhone(Request):
    phonenumber: str = PathInfoField(...)
    country: str | None = QueryStringField(None)


class Phone(Response):
    international: str


register(
    client_name="address",
    resource="phonenumbers",
    service="address",
    version=None,
    path="/phonenumbers/{phonenumber}",
    contract={
        "GET": (GetPhone, Phone),
    },
)
