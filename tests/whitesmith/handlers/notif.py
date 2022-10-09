from blacksmith import HTTPRequest

from whitesmith import HTTPResponse, router


@router.register("POST http://notif.v2/notifications")
def notif_notifications_collection_post(req: HTTPRequest) -> HTTPResponse[None]:
    return HTTPResponse()
