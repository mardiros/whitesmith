from blacksmith import HTTPRequest
from whitesmith import HTTPResponse, router

from polyfactory.factories.pydantic_factory import ModelFactory


from tests.resources.address.phonenumbers import Phone


class PhoneFactory(ModelFactory[Phone]):
    __model__ = Phone


@router.register("GET http://address.NaN/phonenumbers/{phonenumber}")
def address_phonenumbers_get(req: HTTPRequest) -> HTTPResponse[Phone]:
    return HTTPResponse(PhoneFactory.build())
