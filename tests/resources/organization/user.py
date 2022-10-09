from blacksmith import PathInfoField, Request, Response, register


class GetUser(Request):
    user_id: str = PathInfoField()


class User(Response):
    id: str
    name: str
    lang: str


register(
    client_name="organization",
    resource="users",
    service="organization",
    version="v5",
    path="/users/{user_id}",
    contract={
        "GET": (GetUser, User),
    },
)
