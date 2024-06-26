from importlib import metadata


from .model import HTTPCollectionResponse, HTTPResponse
from .router import router

__version__ = metadata.version("whitesmith")
__all__ = ["HTTPResponse", "HTTPCollectionResponse", "router", "__version__"]
