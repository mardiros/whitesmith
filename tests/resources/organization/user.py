from typing import Optional

from blacksmith import (
    PathInfoField,
    PostBodyField,
    QueryStringField,
    Request,
    Response,
    register,
)


class CollectionGetUser(Request):
    per_page: int = QueryStringField(default=42)


class GetUser(Request):
    user_id: str = PathInfoField()


class CreateUser(Request):
    name: str = PostBodyField()
    lang: str = PostBodyField()


class PatchUser(GetUser):
    name: Optional[str] = PostBodyField()
    lang: Optional[str] = PostBodyField()


class User(Response):
    id: str
    name: str
    lang: str


class UserCreated(Response):
    id: str


class PartialUser(Response):
    id: str
    name: str


register(
    client_name="organization",
    resource="users",
    service="organization",
    version="v5",
    collection_path="/users",
    collection_contract={
        "GET": (CollectionGetUser, PartialUser),
        "POST": (CreateUser, UserCreated),
    },
    path="/users/{user_id}",
    contract={
        "GET": (GetUser, User),
        "PATCH": (PatchUser, None),
    },
)
