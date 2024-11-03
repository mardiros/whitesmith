from collections.abc import Sequence

from blacksmith import PostBodyField, Request, register
from pydantic import BaseModel, Field
from typing_extensions import Literal


class Recipient(BaseModel):
    channel: Literal["email", "sms"] = Field(...)
    address: str = Field(...)
    lang: str = Field(...)


class CreateNotification(Request):
    template: str = PostBodyField()
    recipients: Sequence[Recipient] = PostBodyField()
    params: dict[str, str] = PostBodyField()


register(
    client_name="notif",
    resource="notifications",
    service="notif",
    version="v2",
    collection_path="/notifications",
    collection_contract={
        "POST": (CreateNotification, None),
    },
)
