from typing import Any

from blacksmith import HTTPRequest
from whitesmith import HTTPResponse, router, HTTPCollectionResponse
from pydantic_factories import ModelFactory


from tests.resources.organization.user import User
from tests.resources.organization.user import PartialUser
from tests.resources.organization.user import UserCreated


class UserFactory(ModelFactory[User]):
    __model__ = User


class PartialUserFactory(ModelFactory[PartialUser]):
    __model__ = PartialUser


class UserCreatedFactory(ModelFactory[UserCreated]):
    __model__ = UserCreated


@router.get("http://organization.v5/users")
def organization_users_collection_get(
    req: HTTPRequest,
) -> HTTPCollectionResponse[PartialUser]:
    return HTTPCollectionResponse([PartialUserFactory.build()])


@router.post("http://organization.v5/users")
def organization_users_collection_post(req: HTTPRequest) -> HTTPResponse[UserCreated]:
    return HTTPResponse(UserCreatedFactory.build())


@router.get("http://organization.v5/users/{user_id}")
def organization_users_get(req: HTTPRequest) -> HTTPResponse[User]:
    return HTTPResponse(UserFactory.build())


@router.patch("http://organization.v5/users/{user_id}")
def organization_users_patch(req: HTTPRequest) -> HTTPResponse[Any]:
    return HTTPResponse()
