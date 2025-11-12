"""
Functions and classes for generating order forms given order information
packaged as a DataFrame extracted using plkit.extract_orders()
"""

import numpy as _np
import pandas as _pd
from .read_orders import read_order

class Product:
    """Class to hold information about a specific product"""

    def __init__(self, name: str) -> None:
        """
        Initialise an empty instance of the product class

        Parameters
        ----------
        name : str
            Name of the particular product

        Returns
        -------
        None
        """

        # Internal dictionary to store the pricing of individual items
        self.pricing = {
            "Unisex EcoLayer Hoodie": 38.40,  # pounds
            "Unisex EcoLayer Hoodie - 1 Personalisation": 42.60,
            "Unisex EcoLayer Hoodie - 2 Personalisations": 46.80,
            "Unisex Shield Performance Sweatshirt": 36.0,
            "Unisex Shield Performance Sweatshirt - 1 Personalisation": 40.20,
            "Unisex Shield Performance Sweatshirt - 2 Personalisations": 44.40,
            "Men's EcoLayer Tee (Navy)": 18.60,
            "Men's EcoLayer Tee - 1 Personalisation (Navy)": 22.80,
            "Men's EcoLayer Tee - 2 Personalisations (Navy)": 27.0,
            "Men's EcoLayer Tee (Forest)": 18.60,
            "Men's EcoLayer Tee - 1 Personalisation (Forest)": 22.80,
            "Men's EcoLayer Tee - 2 Personalisations (Forest)": 27.0,
            "Women's EcoLayer Tee (Navy)": 18.60,
            "Women's EcoLayer Tee - 1 Personalisation (Navy)": 22.80,
            "Women's EcoLayer Tee - 2 Personalisations (Navy)": 27.0,
            "Women's EcoLayer Tee (Forest)": 18.60,
            "Women's EcoLayer Tee - 1 Personalisation (Forest)": 22.80,
            "Women's EcoLayer Tee - 2 Personalisations (Forest)": 27.0,
            "Men's Sublimated Tee (Navy)": 25.62,
            "Men's Sublimated Tee - 1 Personalisation (Navy)": 25.62,
            "Men's Sublimated Tee - 2 Personalisations (Navy)": 25.62,
            "Men's Sublimated Tee (Forest)": 25.62,
            "Men's Sublimated Tee - 1 Personalisation (Forest)": 25.62,
            "Men's Sublimated Tee - 2 Personalisations (Forest)": 25.62,
            "Women's Sublimated Tee (Navy)": 25.62,
            "Women's Sublimated Tee - 1 Personalisation (Navy)": 25.62,
            "Women's Sublimated Tee - 2 Personalisations (Navy)": 25.62,
            "Women's Sublimated Tee (Forest)": 25.62,
            "Women's Sublimated Tee - 1 Personalisation (Forest)": 25.62,
            "Women's Sublimated Tee - 2 Personalisations (Forest)": 25.62
        }

        if name not in self.pricing:
            raise LookupError(f"Item {name} not found.")

        self.name = name
        self.colour = "Forest" if "Forest" in self.name else "Navy"
        self.sizings = {
            "XS": 0,
            "S": 0,
            "M": 0,
            "L": 0,
            "XL": 0,
            "2XL": 0,
            "3XL": 0,
            "4XL": 0,
            "5XL": 0,
        }
        self.total_quantity = 0
        self.unit_price = self.pricing[name]
        self.total_price = 0

    def __str__(self) -> str:
        return self.__class__.__name__

    def update_count(self, sizing, quantity=1) -> None:
        """
        Update the product count given a specific sizing

        Parameters
        ----------
        sizing : str
            Sizing for which to update the count
        quantity : int, optional
            Item count to update

        Returns
        -------
        None
        """
        if sizing not in self.sizings:
            raise LookupError(
                f"""Sizing {sizing} not found,
                select a sizing from {list(self.sizings.keys())}"""
            )

        self.sizings[sizing] += quantity
        self.total_quantity += quantity
        self.total_price = self.unit_price * self.total_quantity

    def update_product(self, order) -> None:
        """
        Update the product specifications given a specific order

        Parameters
        ----------
        order : class
            Instance of the Order class which is used to update the product information

        Returns
        -------
        None
        """

        # Update product names
        order.identify_products()

        # Loop over every item stored in order and update where appropriate
        for n in range(len(order.items)):
            product_name = order.products[n]
            sizing = order.sizings[n]

            # Check for valid product name and sizing
            if isinstance(product_name, str) and product_name.strip() == self.name:
                if isinstance(sizing, str) and sizing.strip() in self.sizings:
                    self.update_count(sizing.strip())


def _update_df_products(df_products, product) -> _pd.DataFrame:
    """Internal function to add a new row to df_products with the
    information in an updated instance of the Product class"""

    womens_sizing = {
        "XS": 6,
        "S": 8,
        "M": 10,
        "L": 12,
        "XL": 14,
        "2XL": 16,
        "3XL": 18,
        "4XL": 20,
        "5XL": 22,
    }

    product_name = product.name.replace("(Forest)", "").replace("(Navy)", "").strip()

    new_row = {
        "Product Name": product_name,
        "Colour": product.colour,
        "Total Quantity": product.total_quantity,
        "Unit Price (£)": product.unit_price,
        "Total Price (£)": product.total_price,
    }

    for sizing in ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]:
        size_key = womens_sizing[sizing] if "Women's" in product_name else sizing
        new_row[size_key] = product.sizings.get(sizing, 0)

    return _pd.concat([df_products, _pd.DataFrame([new_row])], ignore_index=True)


def generate_product_order(df_orders: _pd.DataFrame) -> _pd.DataFrame:
    """
    Generate a DataFrame of product-specific order information,
    given a DataFrame of orders

    Parameters
    ----------
    df_orders: _pd.DataFrame
        The order details converted to a pandas DataFrame

    Returns
    -------
    df_products: _pd.DataFrame
        Full order details for every product,
        completed with the orders contained in df_orders
    """

    # List of all products - women's sizing is different
    items = [
        "Unisex EcoLayer Hoodie",
        "Unisex EcoLayer Hoodie - 1 Personalisation",
        "Unisex EcoLayer Hoodie - 2 Personalisations",
        "Unisex Shield Performance Sweatshirt",
        "Unisex Shield Performance Sweatshirt - 1 Personalisation",
        "Unisex Shield Performance Sweatshirt - 2 Personalisations",
        "Men's EcoLayer Tee (Navy)",
        "Men's EcoLayer Tee - 1 Personalisation (Navy)",
        "Men's EcoLayer Tee - 2 Personalisations (Navy)",
        "Men's EcoLayer Tee (Forest)",
        "Men's EcoLayer Tee - 1 Personalisation (Forest)",
        "Men's EcoLayer Tee - 2 Personalisations (Forest)",
        "Women's EcoLayer Tee (Navy)",
        "Women's EcoLayer Tee - 1 Personalisation (Navy)",
        "Women's EcoLayer Tee - 2 Personalisations (Navy)",
        "Women's EcoLayer Tee (Forest)",
        "Women's EcoLayer Tee - 1 Personalisation (Forest)",
        "Women's EcoLayer Tee - 2 Personalisations (Forest)",
        "Men's Sublimated Tee (Navy)",
        "Men's Sublimated Tee - 1 Personalisation (Navy)",
        "Men's Sublimated Tee - 2 Personalisations (Navy)",
        "Men's Sublimated Tee (Forest)",
        "Men's Sublimated Tee - 1 Personalisation (Forest)",
        "Men's Sublimated Tee - 2 Personalisations (Forest)",
        "Women's Sublimated Tee (Navy)",
        "Women's Sublimated Tee - 1 Personalisation (Navy)",
        "Women's Sublimated Tee - 2 Personalisations (Navy)",
        "Women's Sublimated Tee (Forest)",
        "Women's Sublimated Tee - 1 Personalisation (Forest)",
        "Women's Sublimated Tee - 2 Personalisations (Forest)"
    ]

    # Names of all people who submitted an order
    names = df_orders["Name"].to_list()

    # Empty df to store product order info
    columns = [
        "Product Name",
        "Colour",
        "Total Quantity",
        "XS",
        "S",
        "M",
        "L",
        "XL",
        "2XL",
        "3XL",
        "4XL",
        "5XL",
        6,
        8,
        10,
        12,
        14,
        16,
        18,
        20,
        22,
        "Unit Price (£)",
        "Total Price (£)",
    ]
    df_products = _pd.DataFrame(columns=columns)

    for item in items:
        product = Product(item)  # Initialise empty class

        for name in names:  # Populate product with the info from all orders
            order = read_order(df_orders, name)
            order.identify_products()
            product.update_product(order)

        df_products = _update_df_products(df_products, product)

    # Add total pricing row
    count_all_items = _np.sum(df_products["Total Quantity"].to_numpy())
    total_price = _np.sum(df_products["Total Price (£)"].to_numpy())

    new_row = [_np.nan] * len(columns)
    new_row[2] = count_all_items
    new_row[-1] = total_price
    df_products.loc[len(df_products)] = new_row
    df_products.iloc[-1, -2] = "Total"  # Add label for total

    # Add label for club name
    new_row = [_np.nan] * len(columns)
    df_products.loc[len(df_products)] = new_row
    df_products.iloc[-1, 1] = "Club Name"
    df_products.iloc[-1, 2] = "Badminton"

    return df_products


def generate_product_personalisations(df_orders: _pd.DataFrame) -> _pd.DataFrame:
    """
    Generate a DataFrame of product-specific order personalisations,
    given a DataFrame of orders

    Parameters
    ----------
    df_orders: _pd.DataFrame
        The order details converted to a pandas DataFrame

    Returns
    -------
    df_personal: _pd.DataFrame
        Full personalisation details for every product,
        completed with the orders contained in df_orders
    """

    womens_sizing = {
        "XS": 6,
        "S": 8,
        "M": 10,
        "L": 12,
        "XL": 14,
        "2XL": 16,
        "3XL": 18,
        "4XL": 20,
        "5XL": 22,
    }

    # Names of all people who submitted an order
    names = df_orders["Name"].to_list()

    # Empty df to store product order info
    columns = [
        "Product Name",
        "Size",
        "Colour",
        "Initials (sleeve personalisation)",
        "Name (back personalisation)",
    ]

    df_personal = _pd.DataFrame(columns=columns)

    for name in names:  # Populate product with the info from all orders
        order = read_order(df_orders, name)
        order.identify_products()

        for n in range(len(order.items)):
            product_name = order.products[n]

            if isinstance(product_name, str):
                product_name = product_name.strip()
                sizing = order.sizings[n]

                new_row = {
                    "Product Name": product_name,
                    "Size": womens_sizing.get(sizing, sizing)
                    if "Women's" in product_name
                    else sizing,
                    "Colour": "Forest" if "Forest" in product_name else "Navy",
                    "Initials (sleeve personalisation)": order.sleeve_names[n],
                    "Name (back personalisation)": order.back_names[n],
                }

                # Only add column for personalised item
                if isinstance(order.sleeve_names[n], str) or isinstance(
                    order.back_names[n], str
                ):
                    df_personal = _pd.concat(
                        [df_personal, _pd.DataFrame([new_row])], ignore_index=True
                    )

    return df_personal
