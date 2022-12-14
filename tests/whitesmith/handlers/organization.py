from typing import Any

from blacksmith import HTTPRequest
from whitesmith import router, HTTPResponse
from pydantic_factories import ModelFactory


from tests.resources.organization.user import UserCreated
from tests.resources.organization.user import User
from tests.resources.organization.user import PartialUser


class UserCreatedFactory(ModelFactory[UserCreated]):
    __model__ = UserCreated


class UserFactory(ModelFactory[User]):
    __model__ = User


class PartialUserFactory(ModelFactory[PartialUser]):
    __model__ = PartialUser


@router.register("GET http://organization.v5/users")
def organization_users_collection_get(req: HTTPRequest) -> HTTPResponse[PartialUser]:
    return HTTPResponse(PartialUserFactory.build())


@router.register("POST http://organization.v5/users")
def organization_users_collection_post(req: HTTPRequest) -> HTTPResponse[UserCreated]:
    return HTTPResponse(UserCreatedFactory.build())


@router.register("GET http://organization.v5/users/{user_id}")
def organization_users_get(req: HTTPRequest) -> HTTPResponse[User]:
    return HTTPResponse(UserFactory.build())


@router.register("PATCH http://organization.v5/users/{user_id}")
def organization_users_patch(req: HTTPRequest) -> HTTPResponse[Any]:
    return HTTPResponse()
