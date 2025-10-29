"""
Functions and classes for reading in order information from the excel sheet
containing responses from the Microsoft form
"""

import os as _os
from typing import List as _List

import numpy as _np
import pandas as _pd



def extract_orders(filename: str = "responses.xlsx") -> _pd.DataFrame:
    """
    Read in the order response form as a pandas DataFrame.

    Parameters
    ----------
    filename : str, optional
        The name of the responses form saved from Microsoft forms

    Returns
    -------
    df_orders : pd.DataFrame
        The order details converted to a pandas DataFrame
    """

    if not filename.endswith(".xlsx"):
        raise ValueError("Input must be an Excel File")

    if not _os.path.isfile(filename):
        raise FileNotFoundError(f"File {filename} does not exist")

    try:
        df_orders = _pd.read_excel(filename)
    except _pd.errors.EmptyDataError as e:
        raise _pd.errors.EmptyDataError(f"The file {filename} is empty") from e
    except Exception as e:
        raise Exception(f"An error occurred: {e}") from e

    return df_orders


class Order:
    """Class to hold information about a single specific order"""

    def __init__(
        self,
        email: str,
        name: str,
        items: _List[str],
        sizings: _List[str],
        back_names: _List[str],
        sleeve_names: _List[str],
    ) -> None:
        """
        Initialise the Order class

        Parameters
        ----------
        email : str
            Email address of person placing the order
        name : str
            Name of the person placing the order
        items : list
            Ordered items
        sizings : list
            Sizing information (XS, S, .., 4XL)
        back_names : list
            Personalisations to be printed on the back of the item
        sleeve_names : list
            Initials to be printed on the sleeve

        Returns
        -------
        None
        """
        self.email = email
        self.name = name
        self.items = items
        self.sizings = sizings
        self.back_names = back_names
        self.sleeve_names = sleeve_names
        self.products = [
            _np.nan
        ] * 5  # Product information is empty, extract with function identify_products()

        if not (len(items) == len(sizings) == len(back_names) == len(sleeve_names)):
            raise ValueError("Mismatch in items input!")

        # List to store number of personalisations
        n_personalisations = [_np.nan] * 5

        for n in range(len(items)):
            if isinstance(items[n], str):
                n_personalisations[n] = 0

        for n in range(len(back_names)):
            if isinstance(back_names[n], str):
                n_personalisations[n] += 1

        for n in range(len(sleeve_names)):
            if isinstance(sleeve_names[n], str):
                n_personalisations[n] += 1

        self.n_personalisations = n_personalisations

    def __str__(self) -> str:
        return self.__class__.__name__

    def identify_products(self) -> None:
        """
        Assign a product name to each item in the order
        """

        products = [_np.nan] * len(self.items)

        for n in range(len(self.items)):
            item = self.items[n]

            if isinstance(item, str):
                # Extract how many personalisations an item has
                n_personal = self.n_personalisations[n]

                if n_personal == 0:
                    products[n] = item

                if n_personal == 1:
                    products[n] = item + "- 1 Personalisation"

                if n_personal == 2:
                    products[n] = item + "- 2 Personalisations"

        # Replace 'Green' with 'Forest'
        products = [
            product.replace("Green", "Forest") if isinstance(product, str) else product
            for product in products
        ]

        # Move colour to the end of the product name
        for i, product in enumerate(products):
            if isinstance(product, str):
                for colour in ["Forest", "Navy"]:
                    if f"({colour})" in product:
                        products[i] = (
                            product.replace(f"({colour})", "").strip() + f" ({colour})"
                        )

        self.products = [
            product.strip() if isinstance(product, str) else product
            for product in products
        ]


def _extract_items(df_orders: _pd.DataFrame, idx: int):
    """Internal function to extract the item information as a list"""

    items = []

    for n_item in ["First", "Second", "Third", "Fourth", "Fifth"]:
        column_name = f"{n_item} kit item"

        # Check that all item columns exist
        if column_name not in df_orders.columns:
            raise LookupError(f"item column not found for {n_item} item")

        items.append(df_orders.iloc[idx][column_name].iloc[0])

    # Strip string entries
    items = [item.strip() if isinstance(item, str) else item for item in items]

    return items


def _extract_sizings(df_orders: _pd.DataFrame, idx: int):
    """Internal function to extract the sizing information as a list"""

    sizings = []

    for n_item in ["first", "second", "third", "fourth", "fifth"]:
        column_name = (
        f"Sizing for {n_item} kit item (note that "
        "for women's tee, XS=size 6, S=size 8, ... , 4XL=20)"
        )

        # Check that all sizing columns exist
        if column_name not in df_orders.columns:
            raise LookupError(f"Sizing column not found for {n_item} item")

        sizings.append(df_orders.iloc[idx][column_name].iloc[0])

    # Strip string entries
    sizings = [
        sizing.strip().upper() if isinstance(sizing, str) else sizing
        for sizing in sizings
    ]

    return sizings


def _extract_sleeve_names(df_orders: _pd.DataFrame, idx: int):
    """Internal function to extract the sleeve_name information as a list"""

    sleeve_names = []

    for n_item in ["First", "Second", "Third", "Fourth", "Fifth"]:
        column_name = (
            f"{n_item} item - personalisation for initials (optional, max two letters)"
        )

        # Check that all sleeve_name columns exist
        if column_name not in df_orders.columns:
            raise LookupError(f"sleeve_name column not found for {n_item} item")

        sleeve_names.append(df_orders.iloc[idx][column_name].iloc[0])

    # Strip string entries
    sleeve_names = [
        name.strip() if isinstance(name, str) else name for name in sleeve_names
    ]

    return sleeve_names


def _extract_back_names(df_orders: _pd.DataFrame, idx: int):
    """Internal function to extract the back_name information as a list"""

    back_names = []

    for n_item in ["First", "Second", "Third", "Fourth", "Fifth"]:
        column_name = f"{n_item} item - name personalisation for back (optional)"

        # Check that all back_name columns exist
        if column_name not in df_orders.columns:
            raise LookupError(f"back_name column not found for {n_item} item")

        back_names.append(df_orders.iloc[idx][column_name].iloc[0])

    # Strip string entries
    back_names = [
        name.strip() if isinstance(name, str) else name for name in back_names
    ]

    return back_names


def read_order(df_orders: _pd.DataFrame, name: str, email: str = None):
    """
    Obtain the order information for a specific person

    Parameters
    ----------
    df_orders: pd.DataFrame
        The pandas DataFrame containing all the order information
    name : str
        The name of the person placing the order
    email : str, optional
        The email address of the person placing the order

    Returns
    -------
    order : class
        Instance of the Order class for the specified name
    """
    name = name.strip()

    # Check that names column exists
    if "Name" not in df_orders.columns:
        raise LookupError("Name column not found in input DataFrame")
    else:
        names = df_orders["Name"].to_list()

    # Check that email column exists
    if "Email" not in df_orders.columns:
        raise LookupError("Email column not found in input DataFrame")

    # Extract email if not specified
    if isinstance(email, str):
        email = email.strip()
    else:
        email = df_orders.loc[df_orders["Name"] == name, "Email"].iloc[0]

    name_count = names.count(name)

    if name_count == 0:
        raise LookupError(f"Name {name} not found!")
    elif name_count == 1:
        idx = df_orders[
            df_orders["Name"] == name
        ].index  # Only use email unless if are two identical names
    else:
        idx = df_orders[
            (df_orders["Name"] == name) & (df_orders["Email"] == email)
        ].index

    # Initialise class
    order_info = Order(
        email=email,
        name=name,
        items=_extract_items(df_orders, idx),
        sizings=_extract_sizings(df_orders, idx),
        back_names=_extract_back_names(df_orders, idx),
        sleeve_names=_extract_sleeve_names(df_orders, idx),
    )

    return order_info
