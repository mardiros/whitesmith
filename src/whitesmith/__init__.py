import pkg_resources

from .model import HTTPResponse, HTTPCollectionResponse
from .router import router

__version__ = pkg_resources.get_distribution("whitesmith").version

__all__ = ["HTTPResponse", "HTTPCollectionResponse", "router", "__version__"]
