import pandas as pd
import datetime

from efsa_tools._utils import _checks


def _activate(dataframe):
    """Activate the records of the specified data frame.

    This helper function is used in the context of a Slowly Changing Dimension
    (SCD) to mark new records of a data frame as active with a start date.

    Args:
        dataframe (pandas.DataFrame): The data frame to activate.

    Returns:
        pandas.DataFrame: The specified data frame with ACTIVE set to True,
            START_DATE set to current time, and END_DATE set to NaT.
    """

    _checks._require_type(value=dataframe, expected_type=pd.DataFrame)

    activated_dataframe_ = dataframe.assign(
        IS_ACTIVE=True,
        START_DATE=datetime.datetime.now(),
        END_DATE=pd.NaT)

    return activated_dataframe_


def _deactivate(dataframe):
    """Deactivate the records of the specified data frame.

    This helper function is used in the context of a Slowly Changing Dimension
    (SCD) to mark active records of a data frame as not active with an end
    date.

    Args:
        dataframe (pandas.DataFrame): The data frame to deactivate.

    Returns:
        pandas.DataFrame: The specified data frame with IS_ACTIVE set to False
            and END_DATE set to current time.
    """

    _checks._require_type(value=dataframe, expected_type=pd.DataFrame)

    deactivated_dataframe_ = dataframe.assign(
        IS_ACTIVE=False,
        END_DATE=datetime.datetime.now())

    return deactivated_dataframe_


def sscd2(new_data, current_data):
    """Implement a "Simple" Slowly Changing Dimension Type 2.

    This function implements a Simplified version of Slowly Changing Dimension
    Type 2 to merge new and current data while maintaining historical records.
    The function deactivates all the old records and activates new ones,
    ensuring a history-preserving update strategy. The difference between a
    standard SCD2 is that this simplified version applies no checks on the
    data, deactivating all the old records and activating the new ones, even if
    some of the old records are still active.

    Args:
        new_data (pandas.DataFrame): The data frame containing new records.
        current_data (pandas.DataFrame): The data frame containing existing
            records.

    Returns:
        pandas.DataFrame: A combined data frame with all old data marked as not
            active and new data marked as active.

    Examples:
        >>> from efsa_tools import *

        >>> merged_data = sscd2(new_data=new_dataset, current_data=old_dataset)
    """

    _checks._require_type(value=new_data, expected_type=pd.DataFrame)
    _checks._require_type(value=current_data, expected_type=pd.DataFrame)

    merged_data_ = pd.concat([
        _deactivate(dataframe=current_data),
        _activate(dataframe=new_data)
    ], ignore_index=True)

    return merged_data_


def scd2(new_data, current_data, key=None):
    """Implement a Slowly Changing Dimension Type 2.

    This function implements a Slowly Changing Dimension Type 2 to merge new
    and current data while maintaining historical records. The function
    deactivates all the old records and activates new ones, ensuring a
    history-preserving update strategy. Only the changing records are marked as
    not active and replaced by new active ones.

    Args:
        new_data (pandas.DataFrame): The data frame containing new records.
        current_data (pandas.DataFrame): The data frame containing existing
            records.
        key (list, optional): The columns to be used as key. Defaults to None.

    Returns:
        pandas.DataFrame: A combined data frame with old data marked as not
        active and new data marked as active.

    Examples:
        >>> from efsa_tools import *

        >>> merged_data = scd2(new_data=new_dataset, current_data=old_dataset)
    """

    _checks._require_type(value=new_data, expected_type=pd.DataFrame)
    _checks._require_type(value=current_data, expected_type=pd.DataFrame)
    if key is not None:
        _checks._require_type(value=key, expected_type=list)

    if key is None:
        key = list(new_data.columns)

    current_inactive_data_ = current_data[current_data["IS_ACTIVE"] == False]
    current_active_data_ = current_data[current_data["IS_ACTIVE"] == True]

    still_active_data_ = (
        current_active_data_.drop_duplicates()
        .merge(new_data.drop_duplicates(), on=key, how="inner")
    )

    newly_active_data_ = new_data.merge(
        current_active_data_[key], on=key, how="left", indicator=True)
    newly_active_data_ = newly_active_data_[
        newly_active_data_["_merge"] == "left_only"].drop(columns="_merge")
    newly_active_data_ = _activate(newly_active_data_)

    deactivated_data_ = current_active_data_.merge(
        new_data[key], on=key, how="left", indicator=True)
    deactivated_data_ = deactivated_data_[
        deactivated_data_["_merge"] == "left_only"].drop(columns="_merge")
    deactivated_data_ = _deactivate(deactivated_data_)

    merged_data_ = pd.concat([
        still_active_data_,
        newly_active_data_,
        deactivated_data_,
        current_inactive_data_
    ], ignore_index=True)

    return merged_data_
