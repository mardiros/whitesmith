from blacksmith import HTTPRequest
from polyfactory.factories.pydantic_factory import ModelFactory

from tests.resources.address.phonenumbers import Phone
from whitesmith import HTTPResponse, router


class PhoneFactory(ModelFactory[Phone]):
    __model__ = Phone


@router.get("http://address.NaN/phonenumbers/{phonenumber}")
def address_phonenumbers_get(req: HTTPRequest) -> HTTPResponse[Phone]:
    return HTTPResponse(PhoneFactory.build())