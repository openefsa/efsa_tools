"""This module contains internal functions for performing type and data checks.
"""

import pandas as pd


def _require_type(value, expected_type):
    """Check that a value is of the expected type.

    Args:
        value: The value to check.
        expected_type: The expected type.

    Raises:
        TypeError: If the value is not of the expected type.

    Returns:
        None: The function returns nothing if the check passes.
    """

    if not isinstance(value, expected_type):
        raise TypeError(f"Expected type {expected_type}, got {type(value)}")


def _must_include(dataframe, names):
    """Check if a dataframe includes the specified column names.

    Args:
        dataframe: The dataframe to check.
        names: The names of the columns to check.

    Raises:
        ValueError: If the dataframe does not include the specified column
            names.

    Returns:
        None: The function returns nothing if the check passes.
    """

    _require_type(value=dataframe, expected_type=pd.DataFrame)
    _require_type(value=names, expected_type=list)

    if not all(name_ in dataframe.columns for name_ in names):
        raise ValueError("Expected data frame with columns: {}".format(names))
