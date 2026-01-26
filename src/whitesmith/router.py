from collections.abc import Callable, MutableMapping
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import tamahagane as th
from blacksmith import HTTPRequest
from blacksmith import HTTPResponse as BMResponse
from blacksmith.typing import HTTPMethod

from whitesmith import HTTPCollectionResponse, HTTPResponse

Handler = Callable[[HTTPRequest], HTTPResponse[Any] | HTTPCollectionResponse[Any]]


TH_CATEGORY = "whitesmith"


@dataclass
class Registry:
    whitesmith: "Router"


class Router:
    def __init__(self) -> None:
        self.routes: MutableMapping[tuple[str, str], Handler] = {}

    def handle(self, req: HTTPRequest) -> BMResponse:
        try:
            return self.routes[(req.method, req.url_pattern)](req).build()
        except KeyError:
            return BMResponse(
                500,
                {},
                {
                    "message": f"Unregister whitesmith route: "
                    f"{req.method} {req.url_pattern}"
                },
            )

    def register(self, meth: HTTPMethod, url: str, fn: Handler) -> None:
        self.routes[(meth, url)] = fn


class RouterBuilder:
    def __init__(self) -> None:
        self.scanned: set[ModuleType] = set()

    def get(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("GET", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def post(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("POST", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def put(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("PUT", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def patch(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("PATCH", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def delete(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("DELETE", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def options(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("OPTIONS", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def head(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(registry: Registry) -> None:
                registry.whitesmith.register("HEAD", url, wrapped)

            th.attach(wrapped, callback, category=TH_CATEGORY)
            return wrapped

        return configure

    def build_router(self, mod: ModuleType) -> Router:
        assert mod
        router = Router()
        scanner = th.Scanner(Registry(whitesmith=router))
        scanner.scan(mod)
        return router


router = RouterBuilder()
