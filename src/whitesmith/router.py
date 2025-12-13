from collections.abc import Callable, MutableMapping
from types import ModuleType
from typing import Any

import venusian
from blacksmith import HTTPRequest
from blacksmith import HTTPResponse as BMResponse
from blacksmith.typing import HTTPMethod

from whitesmith import HTTPCollectionResponse, HTTPResponse

Handler = Callable[[HTTPRequest], HTTPResponse[Any] | HTTPCollectionResponse[Any]]


VENUSIAN_CATEGORY = "whitesmith"


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
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("GET", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def post(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("POST", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def put(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("PUT", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def patch(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("PATCH", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def delete(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("DELETE", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def options(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("OPTIONS", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def head(self, url: str) -> Callable[[Handler], Handler]:
        def configure(wrapped: Handler) -> Handler:
            def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
                if not hasattr(scanner, "router"):
                    return  # coverage: ignore
                scanner.router.register("HEAD", url, wrapped)  # type: ignore

            venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
            return wrapped

        return configure

    def build_router(self, mod: ModuleType) -> Router:
        assert mod
        router = Router()
        scanner = venusian.Scanner(router=router)
        scanner.scan(mod, categories=[VENUSIAN_CATEGORY])
        return router


router = RouterBuilder()
