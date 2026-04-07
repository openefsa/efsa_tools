import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

from efsa_tools.dataframe_utils import (drop_empty, remove_replicated_columns,
                                        enrich)


class TestDataframeUtils(unittest.TestCase):

    ################
    # drop_empty() #
    ################

    def test_drop_empty_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, drop_empty, dataframe=123)

    def test_drop_empty_output(self):
        """Test the behaviour for valid data."""
        dataframe_ = pd.DataFrame({
            'a': [1, 2, np.nan],
            'b': [3, 4, np.nan],
            'c': [np.nan, np.nan, np.nan]
        })
        expected_result_ = pd.DataFrame({
            'a': ['1', '2'],
            'b': ['3', '4']
        })
        result_ = drop_empty(dataframe=dataframe_)
        self.assertIsInstance(result_, pd.DataFrame)
        assert_frame_equal(result_, expected_result_)

    ###############################
    # remove_replicated_columns() #
    ###############################

    def test_remove_replicated_columns_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, remove_replicated_columns, dataframe=123,
                          prefix="")
        self.assertRaises(TypeError, remove_replicated_columns,
                          dataframe=pd.DataFrame(), prefix=123)

    def test_remove_replicated_columns_output(self):
        """Test the behaviour for valid data."""
        dataframe_ = pd.DataFrame({
            "prefix_1": [1, "NA", np.nan],
            "prefix_2": [np.nan, 2, "N/a"],
            "prefix_3": ['', np.nan, 3],
            "another_col": [np.nan, np.nan, 3]
        })
        expected_result_ = pd.DataFrame({
            "prefix_deduplicated": ['1', '2', '3'],
            "another_col": [np.nan, np.nan, '3']
        })
        result_ = remove_replicated_columns(
            dataframe=dataframe_,
            prefix="prefix"
        )
        self.assertIsInstance(result_, pd.DataFrame)
        assert_frame_equal(result_, expected_result_)

    ############
    # enrich() #
    ############

    def test_enrich_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, enrich, dataframe=123,
                          catalogue=pd.DataFrame(), join_by="",
                          enriched_column_name="")
        self.assertRaises(TypeError, enrich, dataframe=pd.DataFrame(),
                          catalogue=123, join_by="", enriched_column_name="")
        self.assertRaises(ValueError, enrich, dataframe=pd.DataFrame(),
                          catalogue=pd.DataFrame(), join_by="",
                          enriched_column_name="")
        self.assertRaises(TypeError, enrich, dataframe=pd.DataFrame(),
                          catalogue=pd.DataFrame({"NAME": [1], "CODE": [2]}),
                          join_by=123, enriched_column_name="")
        self.assertRaises(TypeError, enrich, dataframe=pd.DataFrame(),
                          catalogue=pd.DataFrame({"NAME": [1], "CODE": [2]}),
                          join_by="", enriched_column_name=123)

    def test_enrich_output(self):
        """Test the behaviour for valid data."""
        dataframe_ = pd.DataFrame({
            "CODE": [1, 2, 3]
        })
        catalogue_ = pd.DataFrame({
            "CODE": [1, 2, 3],
            "NAME": ['a', 'b', 'c']
        })
        expected_result_ = pd.DataFrame({
            "enriched_column": ['a', 'b', 'c'],
            "CODE": [1, 2, 3]
        })
        result_ = enrich(
            dataframe=dataframe_,
            catalogue=catalogue_,
            join_by="CODE",
            enriched_column_name="enriched_column"
        )
        self.assertIsInstance(result_, pd.DataFrame)
        assert_frame_equal(result_, expected_result_)
