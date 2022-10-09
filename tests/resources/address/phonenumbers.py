from typing import Optional
from blacksmith import PathInfoField, Request, Response, register, QueryStringField


class GetPhone(Request):
    phonenumber: str = PathInfoField(...)
    country: Optional[str] = QueryStringField(None)


class Phone(Response):
    phonenumber: str


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
