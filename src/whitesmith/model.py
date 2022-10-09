from typing import Generic, Mapping, Optional, TypeVar

from blacksmith import HTTPResponse as BMResponse
from pydantic import BaseModel

T_co = TypeVar("T_co", bound=BaseModel, covariant=True)


class HTTPResponse(Generic[T_co]):
    status_code: int
    headers: Mapping[str, str]
    body: Optional[T_co]

    def __init__(
        self,
        body: Optional[T_co] = None,
        status_code: int = 200,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body

    def build(self) -> BMResponse:
        return BMResponse(
            status_code=self.status_code,
            headers=self.headers,
            json=(None if self.body is None else self.body.dict()),
        )
