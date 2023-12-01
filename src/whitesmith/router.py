from typing import Any, Callable, MutableMapping, Tuple, Union

from blacksmith import HTTPRequest
from blacksmith import HTTPResponse as BMResponse

from whitesmith import HTTPCollectionResponse, HTTPResponse

Handler = Callable[[HTTPRequest], Union[HTTPResponse[Any], HTTPCollectionResponse[Any]]]


class Router:
    routes: MutableMapping[Tuple[str, str], Handler] = {}

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

    def register(self, route: str) -> Callable[[Handler], Handler]:
        meth, url = route.split(maxsplit=2)

        def wrapper(fn: Handler) -> Handler:
            self.routes[(meth, url)] = fn
            return fn

        return wrapper

    def get(self, url: str) -> Callable[[Handler], Handler]:
        return self.register(f"GET {url}")

    def post(self, url: str) -> Callable[[Handler], Handler]:
        return self.register(f"POST {url}")

    def put(self, url: str) -> Callable[[Handler], Handler]:
        return self.register(f"PUT {url}")

    def patch(self, url: str) -> Callable[[Handler], Handler]:
        return self.register(f"PATCH {url}")

    def delete(self, url: str) -> Callable[[Handler], Handler]:
        return self.register(f"DELETE {url}")


router = Router()
