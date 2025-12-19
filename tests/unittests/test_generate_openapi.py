from typing import Literal

import pytest
from blacksmith import PathInfoField, PostBodyField, QueryStringField, Request
from blacksmith.domain.model import Response

from whitesmith.generate_openapis import (
    Content,
    MediaType,
    Parameter,
    RequestBody,
    request_schema_to_params,
    response_schema_to_responses,
)


class GetPhone(Request):
    phonenumber: str = PathInfoField()
    country: str | None = QueryStringField(None)


class Cat(Request):
    pet_type: Literal["cat"] = PostBodyField()
    meows: int = PostBodyField()


class Dog(Request):
    pet_type: Literal["dog"] = PostBodyField()
    barks: float = PostBodyField()


@pytest.mark.parametrize(
    "req,expected_parameters,expected_request_body,expected_schemas",
    [
        pytest.param(
            GetPhone,
            [
                Parameter.model_validate(
                    {
                        "name": "phonenumber",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "location": "path",
                            "title": "Phonenumber",
                            "type": "string",
                        },
                    }
                ),
                Parameter.model_validate(
                    {
                        "name": "country",
                        "in": "querystring",
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "default": None,
                            "location": "querystring",
                            "title": "Country",
                        },
                    }
                ),
            ],
            None,
            {},
            id="Request with parameters",
        ),
        pytest.param(
            Cat,
            [],
            RequestBody(
                description="Cat",
                required=True,
                content=Content.model_validate(
                    {
                        "application/json": MediaType.model_validate(
                            {"schema": {"$ref": "#/components/schemas/CatRequestBody"}}
                        )
                    }
                ),
            ),
            {
                "CatRequestBody": {
                    "properties": {
                        "meows": {
                            "title": "Meows",
                            "type": "integer",
                        },
                        "pet_type": {
                            "const": "cat",
                            "title": "Pet Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "pet_type",
                        "meows",
                    ],
                    "title": "CatRequestBody",
                    "type": "object",
                }
            },
            id="Request with body",
        ),
        pytest.param(
            Cat | Dog,
            [],
            RequestBody(
                description="Cat, Dog",
                required=True,
                content=Content.model_validate(
                    {
                        "application/json": MediaType.model_validate(
                            {
                                "schema": {
                                    "oneOf": [
                                        {"$ref": "#/components/schemas/CatRequestBody"},
                                        {"$ref": "#/components/schemas/DogRequestBody"},
                                    ]
                                }
                            }
                        )
                    }
                ),
            ),
            {
                "CatRequestBody": {
                    "properties": {
                        "meows": {
                            "title": "Meows",
                            "type": "integer",
                        },
                        "pet_type": {
                            "const": "cat",
                            "title": "Pet Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "pet_type",
                        "meows",
                    ],
                    "title": "CatRequestBody",
                    "type": "object",
                },
                "DogRequestBody": {
                    "properties": {
                        "barks": {
                            "title": "Barks",
                            "type": "number",
                        },
                        "pet_type": {
                            "const": "dog",
                            "title": "Pet Type",
                            "type": "string",
                        },
                    },
                    "required": [
                        "pet_type",
                        "barks",
                    ],
                    "title": "DogRequestBody",
                    "type": "object",
                },
            },
            id="Request with body",
        ),
        pytest.param(Request, [], None, {}, id="empty request"),
    ],
)
def test_request_schema_to_params(
    req: type[Request],
    expected_parameters: list[Parameter],
    expected_request_body: RequestBody,
    expected_schemas: dict[str, Content],
):
    assert request_schema_to_params(req) == (
        expected_parameters,
        expected_request_body,
        expected_schemas,
    )
