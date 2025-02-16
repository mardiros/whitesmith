from typing import Any

from pydantic import BaseModel
import pytest
from blacksmith import HTTPRequest
from blacksmith.domain.model.http import HTTPResponse
from whitesmith.router import Router
from whitesmith.model import HTTPResponse


@pytest.fixture
def router() -> Router:
    return Router()


def test_router_register(router: Router):
    @router.register("GET /foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...

    assert router.routes == {("GET", "/foo"): foo}


def test_router_get(router: Router):
    @router.get("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...

    assert router.routes == {("GET", "/foo"): foo}


def test_router_post(router: Router):
    @router.post("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...

    assert router.routes == {("POST", "/foo"): foo}


def test_router_put(router: Router):
    @router.put("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...

    assert router.routes == {("PUT", "/foo"): foo}


def test_router_patch(router: Router):
    @router.patch("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...

    assert router.routes == {("PATCH", "/foo"): foo}


def test_router_delete(router: Router):
    @router.delete("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...

    assert router.routes == {("DELETE", "/foo"): foo}


def test_router_handle(router: Router):
    class Foo(BaseModel):
        name: str

    @router.get("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Foo]:
        return HTTPResponse(body=Foo(name="foobar"))

    assert router.handle(HTTPRequest("GET", "/foo")).json == {"name": "foobar"}

    assert router.handle(HTTPRequest("GET", "/bar")).json == {
        "message": "Unregister whitesmith route: GET /bar",
    }
