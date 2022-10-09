from blacksmith import HTTPRequest
from pydantic_factories import ModelFactory

from tests.resources.organization.user import User
from whitesmith import HTTPResponse, router


class UserFactory(ModelFactory):
    __model__ = User


@router.register("GET http://organization.v5/users/{user_id}")
def organization_users_get(req: HTTPRequest) -> HTTPResponse[User]:
    return HTTPResponse(UserFactory.build())
