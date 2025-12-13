from blacksmith import (
    AsyncAbstractTransport,
    HTTPError,
    HTTPRequest,
    HTTPResponse,
    HTTPTimeout,
    SyncAbstractTransport,
)

from .router import Router


class SyncFakeTransport(SyncAbstractTransport):
    def __init__(self, router: Router):
        super().__init__()
        self.router = router

    def __call__(
        self,
        req: HTTPRequest,
        client_name: str,
        path: str,
        timeout: HTTPTimeout,
    ) -> HTTPResponse:
        """Process the HTTP request."""
        key = f"{req.method} {req.url.format(**req.path)}"

        resp = self.router.handle(req)

        if resp.status_code >= 400:
            raise HTTPError(
                f"{resp.status_code} FAKE FAIL {key}",
                req,
                resp,
            )

        return resp


class AsyncFakeTransport(AsyncAbstractTransport):
    def __init__(self, router: Router) -> None:
        super().__init__()
        self._fake_transport = SyncFakeTransport(router)

    async def __call__(
        self,
        req: HTTPRequest,
        client_name: str,
        path: str,
        timeout: HTTPTimeout,
    ) -> HTTPResponse:
        """Process the HTTP request."""
        ret = self._fake_transport(req, client_name, path, timeout)
        return ret
