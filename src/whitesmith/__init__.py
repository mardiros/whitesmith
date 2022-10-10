import pkg_resources

from .model import HTTPResponse
from .router import router

__version__ = pkg_resources.get_distribution("whitesmith").version

__all__ = ["HTTPResponse", "router", "__version__"]
