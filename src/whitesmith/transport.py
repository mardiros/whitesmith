from blacksmith import (
    AsyncAbstractTransport,
    HTTPError,
    HTTPRequest,
    HTTPResponse,
    HTTPTimeout,
    SyncAbstractTransport,
)

from .router import router


class SyncFakeTransport(SyncAbstractTransport):
    def __call__(
        self,
        req: HTTPRequest,
        client_name: str,
        path: str,
        timeout: HTTPTimeout,
    ) -> HTTPResponse:
        """Process the HTTP request."""
        key = f"{req.method} {req.url.format(**req.path)}"

        resp = router.handle(req)

        if resp.status_code >= 400:
            raise HTTPError(
                f"{resp.status_code} FAKE FAIL {key}",
                req,
                resp,
            )

        return resp


class AsyncFakeTransport(AsyncAbstractTransport):
    def __init__(self) -> None:
        super().__init__()
        self._fake_transport = SyncFakeTransport()

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
