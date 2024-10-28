from typing import Any

from blacksmith import HTTPRequest
from whitesmith import router, HTTPCollectionResponse, HTTPResponse

from polyfactory.factories.pydantic_factory import ModelFactory


from tests.resources.organization.user import UserCreated
from tests.resources.organization.user import PartialUser
from tests.resources.organization.user import User


class UserCreatedFactory(ModelFactory[UserCreated]):
    __model__ = UserCreated


class PartialUserFactory(ModelFactory[PartialUser]):
    __model__ = PartialUser


class UserFactory(ModelFactory[User]):
    __model__ = User


@router.register("GET http://organization.v5/users")
def organization_users_collection_get(
    req: HTTPRequest,
) -> HTTPCollectionResponse[PartialUser]:
    return HTTPCollectionResponse([PartialUserFactory.build()])


@router.register("POST http://organization.v5/users")
def organization_users_collection_post(req: HTTPRequest) -> HTTPResponse[UserCreated]:
    return HTTPResponse(UserCreatedFactory.build())


@router.register("GET http://organization.v5/users/{user_id}")
def organization_users_get(req: HTTPRequest) -> HTTPResponse[User]:
    return HTTPResponse(UserFactory.build())


@router.register("PATCH http://organization.v5/users/{user_id}")
def organization_users_patch(req: HTTPRequest) -> HTTPResponse[Any]:
    return HTTPResponse()
