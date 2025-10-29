"""A package for automating EUBC PlayerLayer kit orders"""

import importlib.metadata

from .read_orders import read_order, extract_orders
from .generate_order_form import (
    generate_product_order,
    generate_product_personalisations
)

try:
    __version__ = importlib.metadata.version("plkit")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0+unknown"

__all__ = [
    "__version__",
    "read_order",
    "extract_orders",
    "generate_product_order",
    "generate_product_personalisations",
]
