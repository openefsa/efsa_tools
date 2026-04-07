import unittest
import pandas as pd

from efsa_tools.scd import _activate, _deactivate, sscd2, scd2


class TestSCD2(unittest.TestCase):

    ###############
    # _activate() #
    ###############

    def test__activate_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _activate, dataframe=123)

    def test__activate_output_1(self):
        """Test the behaviour for valid data."""
        dataframe_ = pd.DataFrame({'a': [1]})
        self.assertIsInstance(_activate(dataframe=dataframe_), pd.DataFrame)

    def test__activate_output_2(self):
        """Test the presence of the START_DATE column."""
        dataframe_ = pd.DataFrame({'a': [1]})
        dataframe_ = _activate(dataframe=dataframe_)
        self.assertTrue("START_DATE" in dataframe_.columns)
        self.assertTrue(all(dataframe_["START_DATE"].notnull()))

    def test__activate_output_3(self):
        """Test the presence of the END_DATE column."""
        dataframe_ = pd.DataFrame({'a': [1]})
        dataframe_ = _activate(dataframe=dataframe_)
        self.assertTrue("END_DATE" in dataframe_.columns)
        self.assertTrue(all(dataframe_["END_DATE"].isnull()))

    def test__activate_output_4(self):
        """Test the presence of the IS_ACTIVE column."""
        dataframe_ = pd.DataFrame({'a': [1]})
        dataframe_ = _activate(dataframe=dataframe_)
        self.assertTrue("IS_ACTIVE" in dataframe_.columns)
        self.assertTrue(all(dataframe_["IS_ACTIVE"]))

    #################
    # _deactivate() #
    #################

    def test__deactivate_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, _deactivate, dataframe=123)

    def test__deactivate_output_1(self):
        """Test the behaviour for valid data."""
        dataframe_ = pd.DataFrame({'a': [1]})
        dataframe_ = _activate(dataframe=dataframe_)
        self.assertIsInstance(_deactivate(dataframe=dataframe_), pd.DataFrame)

    def test__deactivate_output_2(self):
        """Test the presence of the END_DATE column."""
        dataframe_ = pd.DataFrame({'a': [1]})
        dataframe_ = _activate(dataframe=dataframe_)
        dataframe_ = _deactivate(dataframe=dataframe_)
        self.assertTrue("END_DATE" in dataframe_.columns)
        self.assertTrue(all(dataframe_["END_DATE"].notnull()))

    def test__deactivate_output_3(self):
        """Test the presence of the IS_ACTIVE column."""
        dataframe_ = pd.DataFrame({'a': [1]})
        dataframe_ = _activate(dataframe=dataframe_)
        dataframe_ = _deactivate(dataframe=dataframe_)
        self.assertTrue("IS_ACTIVE" in dataframe_.columns)
        self.assertTrue(not all(dataframe_["IS_ACTIVE"]))

    ############
    # _sscd2() #
    ############

    def test_sscd2_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, sscd2, new_data=123,
                          current_data=pd.DataFrame())
        self.assertRaises(TypeError, sscd2, new_data=pd.DataFrame(),
                          current_data=123)

    def test_sscd2_output(self):
        """The function must output as expected."""
        current_data_ = pd.DataFrame({
            "id": [1, 2, 3],
            "colA": ["a1", "a2", "a3"],
            "colB": ["b1", "b2", "b3"],
            "colC": ["c1", "c2", "c3"]
        })
        current_data_ = _activate(dataframe=current_data_)

        new_data_ = pd.DataFrame({
            "id": [1, 2, 3],
            "colA": ["a1", "a2", "a4"],
            "colB": ["b1", "b2", "b4"],
            "colC": ["c1", "c20", "c4"]
        })

        merged_data_ = sscd2(new_data=new_data_, current_data=current_data_)

        expected_result_ = pd.DataFrame({
            "id": [1, 2, 3, 1, 2, 3],
            "colA": ["a1", "a2", "a3", "a1", "a2", "a4"],
            "colB": ["b1", "b2", "b3", "b1", "b2", "b4"],
            "colC": ["c1", "c2", "c3", "c1", "c20", "c4"],
            "IS_ACTIVE": [False, False, False, True, True, True]
        }).sort_values("id")

        merged_data_ = merged_data_.drop(
            columns=merged_data_.filter(
                regex="DATE$").columns).sort_values("id")

        self.assertTrue(merged_data_.equals(expected_result_))

    ###########
    # _scd2() #
    ###########

    def test_scd2_invalid(self):
        """Test the behaviour for invalid data."""
        self.assertRaises(TypeError, scd2, new_data=123,
                          current_data=pd.DataFrame())
        self.assertRaises(TypeError, scd2, new_data=pd.DataFrame(),
                          current_data=123)
        self.assertRaises(TypeError, scd2, new_data=pd.DataFrame(),
                          current_data=pd.DataFrame(), key=123)

    def test_scd2_output(self):
        """The function must output as expected."""
        current_data_ = pd.DataFrame({
            "id": [1, 2, 3],
            "colA": ["a1", "a2", "a3"],
            "colB": ["b1", "b2", "b3"],
            "colC": ["c1", "c2", "c3"]
        })
        current_data_ = _activate(dataframe=current_data_)

        new_data_ = pd.DataFrame({
            "id": [1, 2, 3],
            "colA": ["a1", "a2", "a4"],
            "colB": ["b1", "b2", "b4"],
            "colC": ["c1", "c20", "c4"]
        })

        merged_data_ = scd2(new_data=new_data_, current_data=current_data_)

        expected_result_ = pd.DataFrame({
            "id": [1, 2, 3, 2, 3],
            "colA": ["a1", "a2", "a4", "a2", "a3"],
            "colB": ["b1", "b2", "b4", "b2", "b3"],
            "colC": ["c1", "c20", "c4", "c2", "c3"],
            "IS_ACTIVE": [True, True, True, False, False]
        }).sort_values("id")

        merged_data_ = merged_data_.drop(
            columns=merged_data_.filter(
                regex="DATE$").columns).sort_values("id")

        self.assertTrue(merged_data_.equals(expected_result_))
