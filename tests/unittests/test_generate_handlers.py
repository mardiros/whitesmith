from pathlib import Path

from blacksmith import PathInfoField, QueryStringField, Request, Response
from blacksmith.domain.registry import HttpResource

from whitesmith.generate_handlers import (
    HandlerTemplateContext,
    ResponseModel,
    Route,
    generate_handlers,
)


class GetPhone(Request):
    phonenumber: str = PathInfoField(...)
    country: str | None = QueryStringField(None)


class Phone(Response):
    international: str


def test_generate_handlers_missing_resources():
    context = HandlerTemplateContext()
    context.add_resource("/v1/foo", service="foobar", name="foo", resource=None)
    assert context.extra_import_lines == set()
    assert context.whitesmith_imports == {"router"}
    assert context.has_missing_schema is False
    assert context.response_models == set()
    assert context.routes == []


def test_generate_handlers_context():
    context = HandlerTemplateContext()
    context.add_resource(
        "/v1/foo",
        service="foobar",
        name="foo",
        resource=HttpResource(path="/foo", contract={"GET": (GetPhone, Phone)}),
    )
    assert context.extra_import_lines == {
        "from polyfactory.factories.pydantic_factory import ModelFactory",
    }
    assert context.whitesmith_imports == {
        "HTTPResponse",
        "router",
    }
    assert context.has_missing_schema is False
    assert context.response_models == {
        ResponseModel(mod="tests.unittests.test_generate_handlers", name="Phone"),
    }
    assert context.routes == [
        Route(
            python_method="foobar_foo_get",
            http_method="GET",
            url_pattern="/v1/foo/foo",
            response_model="Phone",
            response_class="HTTPResponse",
        ),
    ]


def test_generate_collection_handlers():
    context = HandlerTemplateContext()
    context.add_resource(
        "/v1/foo",
        service="foobar",
        name="foo",
        resource=HttpResource(path="/foo", contract={"GET": (GetPhone, Phone)}),
        prefix="collection_",
    )
    assert context.extra_import_lines == {
        "from polyfactory.factories.pydantic_factory import ModelFactory",
    }
    assert context.whitesmith_imports == {
        "HTTPCollectionResponse",
        "router",
    }
    assert context.has_missing_schema is False
    assert context.response_models == {
        ResponseModel(mod="tests.unittests.test_generate_handlers", name="Phone"),
    }
    assert context.routes == [
        Route(
            python_method="foobar_foo_collection_get",
            http_method="GET",
            url_pattern="/v1/foo/foo",
            response_model="Phone",
            response_class="HTTPCollectionResponse",
        ),
    ]


def test_generate_handlers_missing_return_schema():
    context = HandlerTemplateContext()
    context.add_resource(
        "/v1/foo",
        service="foobar",
        name="foo",
        resource=HttpResource(path="/foo", contract={"GET": (GetPhone, None)}),
    )
    assert context.extra_import_lines == set()
    assert context.whitesmith_imports == {
        "HTTPResponse",
        "router",
    }
    assert context.has_missing_schema is True
    assert context.response_models == set()
    assert context.routes == [
        Route(
            python_method="foobar_foo_get",
            http_method="GET",
            url_pattern="/v1/foo/foo",
            response_model="",
            response_class="HTTPResponse",
        ),
    ]


def test_generate_handlers(tmp_path: Path):
    generate_handlers(tmp_path, ["tests.whitesmith_handlers"], overwrite=True)
    files = {f.name: f.read_text() for f in tmp_path.glob("whitesmith_handlers/*.py")}
    assert files.keys() == {"__init__.py", "address.py", "notif.py", "organization.py"}
