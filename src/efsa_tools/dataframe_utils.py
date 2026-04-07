import pandas as pd
import numpy as np

from efsa_tools._utils import _checks


def drop_empty(dataframe):
    """Drop empty lines and columns from the specified data frame.

    This function drops all the empty lines and columns from the specified data
    frame, i.e. all the rows and columns that contain only NAs.
    Since Pandas automatically converts integers to float64 when NaN are
    present, the function applies the convert_dtypes() function to the data
    frame in order to restore the original types. Even though types can be
    slightly adjusted, the data frame structure and values remain unchanged.

    Args:
        dataframe (pandas.DataFrame): The data frame from which to remove the
            empty lines and columns.

    Returns:
        pandas.DataFrame: The provided data frame without empty lines and
            columns and all the types transformed to string.

    Examples:
        >>> from efsa_tools import *

        >>> iris.iloc[0] = np.nan
        >>> iris = drop_empty(dataframe=iris)

        >>> iris["Species"] = np.nan
        >>> iris = drop_empty(dataframe=iris)
    """
    
    _checks._require_type(value=dataframe, expected_type=pd.DataFrame)

    dataframe = dataframe[dataframe.isna().sum(axis=1) != dataframe.shape[1]]
    dataframe = dataframe.loc[:, ~dataframe.isna().all()]

    dataframe = dataframe.convert_dtypes()
    dataframe = dataframe.astype(str)
    
    return dataframe


def remove_replicated_columns(dataframe, prefix):
    """Drop and merge replicated columns from the specified data frame.

    This function drops and merges all the replicated columns from the
    specified data frame. All the occurrences of "NA", "N/a", and empty strings
    (case-insensitive) inside the provided data frame are replaced with NAs of
    type character. Then, all and only the columns starting with the specified
    prefix are selected and united into a single column with name ending per
    "_deduplicated". All empty entries in the new deduplicated column are
    replaced with NAs. Finally, the new column is bound with the other columns
    of the initial dataframe.

    Args:
        dataframe (pandas.DataFrame): The data frame from which to drop the
            replicated columns.
        prefix (str): The prefix with which the name of the replicated columns
            starts.

    Returns:
        (pandas.DataFrame): The specified data frame with an additional
            deduplicated column and all the types transformed to string.

    Examples:
        >>> from efsa_tools import *

        >>> iris["Species_1"] = iris["Species"]
        >>> iris["Species_2"] = iris["Species"]
        >>> iris.drop("Species", axis=1, inplace=True)
        
        >>> deduplicated_dataframe_ = remove_replicated_columns(
        ...     dataframe=iris,
        ...     prefix="Species_"
        ... )
    """

    _checks._require_type(value=dataframe, expected_type=pd.DataFrame)
    _checks._require_type(value=prefix, expected_type=str)

    columns_ = [column_ for column_ in dataframe.columns
               if column_.startswith(prefix)]

    dataframe[columns_] = dataframe[columns_].astype(str)

    dataframe[columns_] = dataframe[columns_].replace(
        r"(?i)^\s*(n/a|na)?\s*$", np.nan, regex=True)

    deduplicated_column_name = f"{prefix}_deduplicated"

    dataframe[deduplicated_column_name] = dataframe[columns_].apply(
        lambda row_: ''.join(row_.dropna()), axis=1)

    dataframe[deduplicated_column_name] = (
        dataframe[deduplicated_column_name].replace('', np.nan))

    deduplicated_column = dataframe.pop(deduplicated_column_name)
    dataframe.insert(0, deduplicated_column_name, deduplicated_column)

    dataframe = dataframe.drop(columns=columns_)

    dataframe = dataframe.convert_dtypes()
    dataframe = dataframe.astype(str)

    return dataframe


def enrich(dataframe, catalogue, join_by, enriched_column_name):
    """Enrich a data frame with an EFSA catalogue.

    This function takes a data frame and joins it with an EFSA catalog. The
    EFSA catalog must be itself a data frame.

    Args:
        dataframe (pandas.DataFrame): The data frame to be enriched.
        catalogue (pandas.DataFrame): The data frame that contains the EFSA
            catalogue to be used for the enrichment. It must contain at least
            two columns, namely: NAME and CODE.
        join_by (str): The variable to be used as the join key.
        enriched_column_name (str): The name of the column added to the
            original data.

    Returns:
        pandas.DataFrame: The specified data frame enriched with the catalogue
            data.

    Examples:
        >>> from efsa_tools import *

        >>> # Assuming that 'dataframe' and 'catalogue' are already set up as
        >>> # Pandas DataFrames.
        >>> enriched_data = enrich(
        ...     dataframe=dataframe,
        ...     catalogue=catalogue,
        ...     join_by="CODE",
        ...     enriched_column_name="enrichedColumn"
        ... )
    """

    _checks._require_type(value=dataframe, expected_type=pd.DataFrame)
    _checks._require_type(value=catalogue, expected_type=pd.DataFrame)
    _checks._must_include(dataframe=catalogue, names=["NAME", "CODE"])
    _checks._require_type(value=join_by, expected_type=str)
    _checks._require_type(value=enriched_column_name, expected_type=str)

    catalogue = catalogue[["NAME", "CODE"]].copy()
    catalogue[join_by] = catalogue["CODE"]

    enriched_ = dataframe.merge(catalogue, how="left", on=join_by)
    enriched_ = enriched_.rename(columns={"NAME": enriched_column_name})

    columns_order_ = (
        [enriched_column_name] +
        [column_ for column_ in dataframe.columns]
    )
    enriched_ = enriched_[columns_order_]

    return enriched_
