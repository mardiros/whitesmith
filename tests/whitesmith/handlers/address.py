from blacksmith import HTTPRequest
from whitesmith import router, HTTPResponse
from pydantic_factories import ModelFactory


from tests.resources.address.phonenumbers import Phone


class PhoneFactory(ModelFactory[Phone]):
    __model__ = Phone


@router.register("GET http://address.NaN/phonenumbers/{phonenumber}")
def address_phonenumbers_get(req: HTTPRequest) -> HTTPResponse[Phone]:
    return HTTPResponse(PhoneFactory.build())