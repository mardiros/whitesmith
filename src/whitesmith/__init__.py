from importlib import metadata

from .model import HTTPCollectionResponse, HTTPResponse
from .router import Router, router

__version__ = metadata.version("whitesmith")
__all__ = ["HTTPResponse", "HTTPCollectionResponse", "Router", "router", "__version__"]
