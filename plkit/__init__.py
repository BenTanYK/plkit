"""A package for automating EUBC PlayerLayer kit orders"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("plkit")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0+unknown"

__all__ = ["__version__"]
