from typing import Any

import pytest
from blacksmith import HTTPRequest
from pydantic import BaseModel

from whitesmith.model import HTTPResponse
from whitesmith.router import Router


@pytest.fixture
def router() -> Router:
    return Router()


def test_router_register(router: Router) -> None:
    @router.register("GET /foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...  # type: ignore

    assert router.routes == {("GET", "/foo"): foo}


def test_router_get(router: Router):
    @router.get("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...  # type: ignore

    assert router.routes == {("GET", "/foo"): foo}


def test_router_post(router: Router):
    @router.post("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...  # type: ignore

    assert router.routes == {("POST", "/foo"): foo}


def test_router_put(router: Router):
    @router.put("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...  # type: ignore

    assert router.routes == {("PUT", "/foo"): foo}


def test_router_patch(router: Router):
    @router.patch("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...  # type: ignore

    assert router.routes == {("PATCH", "/foo"): foo}


def test_router_delete(router: Router):
    @router.delete("/foo")
    def foo(req: HTTPRequest) -> HTTPResponse[Any]: ...  # type: ignore

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
