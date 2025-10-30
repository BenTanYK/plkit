"""Validation testing that all orders have been included"""

import pandas as _pd

from ..read_orders import read_order


def _count_initial_order(df_orders: _pd.DataFrame) -> int:
    """Internal function to count the total number of orders
    Some code is repeated in _count_initial_back_personalisations
    and _count_initial_sleeve_personalisations but cba to change it"""
    item_count = 0

    # Check that names column exists
    if "Name" not in df_orders.columns:
        raise LookupError("Name column not found in input DataFrame")
    else:
        names = df_orders["Name"].to_list()

    for name in names:
        if isinstance(name, str):
            order = read_order(df_orders, name)

            for item in order.items:
                if isinstance(item, str):
                    item_count += 1

        else:
            raise ValueError(f"Non-string name {name} detected!")

    return int(item_count)


def _count_initial_back_personalisations(df_orders: _pd.DataFrame) -> int:
    """Internal function to count the total
    number of back name personalisations"""
    item_count = 0

    # Check that names column exists
    if "Name" not in df_orders.columns:
        raise LookupError("Name column not found in input DataFrame")
    else:
        names = df_orders["Name"].to_list()

    for name in names:
        if isinstance(name, str):
            order = read_order(df_orders, name)

            for item in order.back_names:
                if isinstance(item, str):
                    item_count += 1

        else:
            raise ValueError(f"Non-string name {name} detected!")

    return int(item_count)


def _count_initial_sleeve_personalisations(df_orders: _pd.DataFrame) -> int:
    """Internal function to count the total number of orders"""
    item_count = 0

    # Check that names column exists
    if "Name" not in df_orders.columns:
        raise LookupError("Name column not found in input DataFrame")
    else:
        names = df_orders["Name"].to_list()

    for name in names:
        if isinstance(name, str):
            order = read_order(df_orders, name)

            for item in order.sleeve_names:
                if isinstance(item, str):
                    item_count += 1

        else:
            raise ValueError(f"Non-string name {name} detected!")

    return int(item_count)


def _count_processed_order(df_products: _pd.DataFrame) -> int:
    """Internal function to count the total number of items in a
    processed order form - could make this a bit simpler actually"""

    # Check that names column exists
    if "Product Name" not in df_products.columns:
        raise LookupError("Product column not found in input DataFrame")
    else:
        products = df_products["Product Name"].to_list()
        # Drop NaN rows
        products = [product for product in products if isinstance(product, str)]

    # Sum over all size cells that contain item counts
    sum = df_products.iloc[0 : len(products), 3:-2].sum(axis=1)

    return int(sum.sum())

def _count_processed_back_personalisations(df_personal: _pd.DataFrame) -> int:
    """Internal function to count the total number of requested back
    name personalisations"""

    back_names = df_personal["Name (back personalisation)"].to_list()
    # Remove NaN rows
    back_names = [back_name for back_name in back_names if isinstance(back_name, str)]

    return len(back_names)


def _count_processed_sleeve_personalisations(df_personal: _pd.DataFrame) -> int:
    """Internal function to count the total number of requested back
    name personalisations"""

    sleeve_names = df_personal["Initials (sleeve personalisation)"].to_list()
    # Remove NaN rows
    sleeve_names = [
        sleeve_name for sleeve_name in sleeve_names if isinstance(sleeve_name, str)
    ]

    return len(sleeve_names)


def assert_order_count(df_orders: _pd.DataFrame, df_products: _pd.DataFrame) -> None:
    """
    Assert that the item count in the DataFrame of
    products to order matches
    the total number of items in the initial order.

    Parameters
    ----------
    df_orders: _pd.DataFrame
        The order details converted to a pandas DataFrame
    df_products: _pd.DataFrame
        Full order details for every product,
        completed with the orders contained in df_orders

    Returns
    -------
    None
    """
    initial_count = int(_count_initial_order(df_orders))
    processed_count = int(_count_processed_order(df_products))

    assert initial_count == processed_count


def assert_back_personalisations(
    df_orders: _pd.DataFrame, df_personal: _pd.DataFrame
) -> None:
    """
    Assert that the back name personalisations count in the
    DataFrame of products to order matches
    the total number of personalisations in the initial order.

    Parameters
    ----------
    df_orders: _pd.DataFrame
        The order details converted to a pandas DataFrame
    df_personal: __pd.DataFrame
        Full personalisation details for every product,
        completed with the orders contained in df_orders

    Returns
    -------
    None
    """
    initial_count = _count_initial_back_personalisations(df_orders)
    processed_count = _count_processed_back_personalisations(df_personal)

    assert initial_count == processed_count


def assert_sleeve_personalisations(
    df_orders: _pd.DataFrame, df_personal: _pd.DataFrame
) -> None:
    """
    Assert that the sleeve name personalisations count in the
    DataFrame of products to order matches
    the total number of personalisations in the initial order.

    Parameters
    ----------
    df_orders: _pd.DataFrame
        The order details converted to a pandas DataFrame
    df_personal: __pd.DataFrame
        Full personalisation details for every product,
        completed with the orders contained in df_orders

    Returns
    -------
    None
    """
    initial_count = _count_initial_sleeve_personalisations(df_orders)
    processed_count = _count_processed_sleeve_personalisations(df_personal)

    assert initial_count == processed_count
