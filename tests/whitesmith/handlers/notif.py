from typing import Any
from blacksmith import HTTPRequest
from whitesmith import router, HTTPResponse





@router.register("POST http://notif.v2/notifications")
def notif_notifications_collection_post(req: HTTPRequest) -> HTTPResponse[Any]:
    return HTTPResponse()