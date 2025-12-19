from typing import Literal

import pytest
from blacksmith import PathInfoField, PostBodyField, QueryStringField, Request
from blacksmith.domain.model import Response
from pydantic import Field

from whitesmith.generate_openapis import (
    Content,
    MediaType,
    OperationResponse,
    Parameter,
    RequestBody,
    request_schema_to_params,
    response_schema_to_responses,
)


class GetPhone(Request):
    phonenumber: str = PathInfoField()
    country: str | None = QueryStringField(None)


class CreateCat(Request):
    pet_type: Literal["cat"] = PostBodyField()
    meows: int = PostBodyField()


class CreateDog(Request):
    pet_type: Literal["dog"] = PostBodyField()
    barks: float = PostBodyField()


class Cat(Response):
    pet_type: Literal["cat"] = Field()
    meows: int = Field()


class Dog(Response):
    pet_type: Literal["dog"] = Field()
    barks: float = Field()


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
                        "in": "query",
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "default": None,
                            "location": "query",
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
            CreateCat,
            [],
            RequestBody(
                description="CreateCat",
                required=True,
                content=Content.model_validate(
                    {
                        "application/json": MediaType.model_validate(
                            {
                                "schema": {
                                    "$ref": "#/components/schemas/"
                                    "tests_unittests_test_generate_openapi__CreateCat"
                                }
                            }
                        )
                    }
                ),
            ),
            {
                "tests_unittests_test_generate_openapi__CreateCat": {
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
                    "title": "tests_unittests_test_generate_openapi__CreateCat",
                    "type": "object",
                }
            },
            id="Request with body",
        ),
        pytest.param(
            CreateCat | CreateDog,
            [],
            RequestBody(
                description="CreateCat, CreateDog",
                required=True,
                content=Content.model_validate(
                    {
                        "application/json": MediaType.model_validate(
                            {
                                "schema": {
                                    "oneOf": [
                                        {
                                            "$ref": "#/components/schemas/"
                                            "tests_unittests_test_generate_openapi__"
                                            "CreateCat"
                                        },
                                        {
                                            "$ref": "#/components/schemas/"
                                            "tests_unittests_test_generate_openapi__"
                                            "CreateDog"
                                        },
                                    ]
                                }
                            }
                        )
                    }
                ),
            ),
            {
                "tests_unittests_test_generate_openapi__CreateCat": {
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
                    "title": "tests_unittests_test_generate_openapi__CreateCat",
                    "type": "object",
                },
                "tests_unittests_test_generate_openapi__CreateDog": {
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
                    "title": "tests_unittests_test_generate_openapi__CreateDog",
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


@pytest.mark.parametrize(
    "resp,expected_responses,expected_schemas",
    [
        pytest.param(
            Cat,
            {
                "200": OperationResponse(
                    description="Cat",
                    content=Content.model_validate(
                        {
                            "application/json": MediaType.model_validate(
                                {
                                    "schema": {
                                        "$ref": "#/components/schemas/"
                                        "tests_unittests_test_generate_openapi__Cat"
                                    }
                                }
                            )
                        }
                    ),
                )
            },
            {
                "tests_unittests_test_generate_openapi__Cat": {
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
                    "title": "Cat",
                    "type": "object",
                },
            },
            id="Response Body",
        ),
        pytest.param(
            Cat | Dog,
            {
                "200": OperationResponse(
                    description="Cat, Dog",
                    content=Content.model_validate(
                        {
                            "application/json": MediaType.model_validate(
                                {
                                    "schema": {
                                        "oneOf": [
                                            {
                                                "$ref": "#/components/schemas/"
                                                "tests_unittests_test_generate_openapi"
                                                "__Cat"
                                            },
                                            {
                                                "$ref": "#/components/schemas/"
                                                "tests_unittests_test_generate_openapi"
                                                "__Dog"
                                            },
                                        ]
                                    }
                                }
                            )
                        }
                    ),
                )
            },
            {
                "tests_unittests_test_generate_openapi__Cat": {
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
                    "title": "Cat",
                    "type": "object",
                },
                "tests_unittests_test_generate_openapi__Dog": {
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
                    "title": "Dog",
                    "type": "object",
                },
            },
            id="Union Body",
        ),
    ],
)
def test_response_schema_to_responses(
    resp: type[Response],
    expected_responses: dict[str, Response],
    expected_schemas: dict[str, Content],
):
    assert response_schema_to_responses(resp) == (
        expected_responses,
        expected_schemas,
    )
