import unittest
import pandas as pd

from efsa_tools._utils._checks import _require_type, _must_include


class TestChecks(unittest.TestCase):

    ###################
    # _require_type() #
    ###################

    def test__require_type_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _require_type, value=123,
                          expected_type=str)

    def test__require_type_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_require_type(value=123, expected_type=int))

    ###################
    # _must_include() #
    ###################

    def test__must_include_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _must_include, dataframe=123, names=[])
        self.assertRaises(TypeError, _must_include, dataframe=pd.DataFrame(),
                          names=123)

    def test__must_include_output(self):
        """Test the behaviour for valid data."""
        self.assertIsNone(_must_include(
            dataframe=pd.DataFrame({'a': [1], 'b': [2]}),
            names=['a']))

    def test__must_include_wrong(self):
        """Test the behaviour for valid data."""
        self.assertRaises(ValueError, _must_include,
            dataframe=pd.DataFrame({'a': [1], 'b': [2]}), names=['c'])
