"""A package for automating EUBC PlayerLayer kit orders"""

import importlib.metadata

from .read_orders import read_order, extract_orders
from .generate_order_form import (
    generate_product_order,
    generate_product_personalisations
)
from .validate import (
    assert_order_count,
    assert_back_personalisations,
    assert_sleeve_personalisations,
    count_initial_order,
    count_initial_back_personalisations,
    count_initial_sleeve_personalisations,
    count_processed_order,
    count_processed_back_personalisations,
    count_processed_sleeve_personalisations
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
    "assert_order_count",
    "assert_back_personalisations",
    "assert_sleeve_personalisations",
    "count_initial_order",
    "count_initial_back_personalisations",
    "count_initial_sleeve_personalisations",
    "count_processed_order",
    "count_processed_back_personalisations",
    "count_processed_sleeve_personalisations",
]
