from typing import Any

import pytest
from blacksmith import HTTPRequest

from whitesmith.model import HTTPResponse
from whitesmith.router import Router


@pytest.fixture
def router() -> Router:
    return Router()


def test_router_register(router: Router) -> None:
    def foo(req: HTTPRequest) -> HTTPResponse[Any]:
        raise NotImplementedError

    router.register("GET", "/foo", foo)
    assert router.routes == {("GET", "/foo"): foo}
