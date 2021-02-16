# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstksimilaritem_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing RAMSTKSimilarItem module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKSimilarItem


@pytest.fixture
def mock_program_dao(monkeypatch):
    _similar_item_1 = RAMSTKSimilarItem()
    _similar_item_1.revision_id = 1
    _similar_item_1.hardware_id = 1
    _similar_item_1.similar_item_method_id = 1
    _similar_item_1.quality_to_id = 0
    _similar_item_1.parent_id = 0
    _similar_item_1.change_factor_4 = 1.0
    _similar_item_1.change_factor_5 = 1.0
    _similar_item_1.change_factor_6 = 1.0
    _similar_item_1.change_factor_7 = 1.0
    _similar_item_1.change_factor_1 = 1.0
    _similar_item_1.change_factor_2 = 1.0
    _similar_item_1.change_factor_3 = 1.0
    _similar_item_1.change_factor_8 = 1.0
    _similar_item_1.change_factor_9 = 1.0
    _similar_item_1.function_5 = '0'
    _similar_item_1.function_4 = '0'
    _similar_item_1.function_3 = '0'
    _similar_item_1.function_2 = '0'
    _similar_item_1.function_1 = '0'
    _similar_item_1.quality_from_id = 0
    _similar_item_1.change_factor_10 = 1.0
    _similar_item_1.user_blob_3 = ''
    _similar_item_1.environment_from_id = 0
    _similar_item_1.change_description_7 = ''
    _similar_item_1.environment_to_id = 0
    _similar_item_1.result_3 = 0.0
    _similar_item_1.temperature_to = 30.0
    _similar_item_1.user_blob_2 = ''
    _similar_item_1.user_blob_1 = ''
    _similar_item_1.user_blob_5 = ''
    _similar_item_1.user_blob_4 = ''
    _similar_item_1.result_2 = 0.0
    _similar_item_1.change_description_10 = ''
    _similar_item_1.result_1 = 0.0
    _similar_item_1.result_4 = 0.0
    _similar_item_1.result_5 = 0.0
    _similar_item_1.user_float_5 = 0.0
    _similar_item_1.user_float_4 = 0.0
    _similar_item_1.user_float_3 = 0.0
    _similar_item_1.user_float_2 = 0.0
    _similar_item_1.user_float_1 = 0.0
    _similar_item_1.user_int_4 = 0
    _similar_item_1.user_int_5 = 0
    _similar_item_1.user_int_1 = 0
    _similar_item_1.user_int_2 = 0
    _similar_item_1.user_int_3 = 0
    _similar_item_1.change_description_6 = ''
    _similar_item_1.temperature_from = 30.0
    _similar_item_1.change_description_4 = ''
    _similar_item_1.change_description_5 = ''
    _similar_item_1.change_description_2 = ''
    _similar_item_1.change_description_3 = ''
    _similar_item_1.change_description_1 = ''
    _similar_item_1.change_description_8 = ''
    _similar_item_1.change_description_9 = ''

    DAO = MockDAO()
    DAO.table = [
        _similar_item_1,
    ]

    yield DAO


ATTRIBUTES = {
    'similar_item_method_id': 0,
    'quality_to_id': 0,
    'parent_id': 0,
    'change_factor_4': 1.0,
    'change_factor_5': 1.0,
    'change_factor_6': 1.0,
    'change_factor_7': 1.0,
    'change_factor_1': 1.0,
    'change_factor_2': 1.0,
    'change_factor_3': 1.0,
    'change_factor_8': 1.0,
    'change_factor_9': 1.0,
    'function_5': '0',
    'function_4': '0',
    'function_3': '0',
    'function_2': '0',
    'function_1': '0',
    'quality_from_id': 0,
    'change_factor_10': 1.0,
    'user_blob_3': '',
    'environment_from_id': 0,
    'change_description_7': '',
    'environment_to_id': 0,
    'result_3': 0.0,
    'temperature_to': 30.0,
    'user_blob_2': '',
    'user_blob_1': '',
    'user_blob_5': '',
    'user_blob_4': '',
    'result_2': 0.0,
    'change_description_10': '',
    'result_1': 0.0,
    'result_4': 0.0,
    'result_5': 0.0,
    'user_float_5': 0.0,
    'user_float_4': 0.0,
    'user_float_3': 0.0,
    'user_float_2': 0.0,
    'user_float_1': 0.0,
    'user_int_4': 0,
    'user_int_5': 0,
    'user_int_1': 0,
    'user_int_2': 0,
    'user_int_3': 0,
    'change_description_6': '',
    'temperature_from': 30.0,
    'change_description_4': '',
    'change_description_5': '',
    'change_description_2': '',
    'change_description_3': '',
    'change_description_1': '',
    'change_description_8': '',
    'change_description_9': ''
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKSimilarItem:
    """Class for testing the RAMSTKSimilarItem model."""
    @pytest.mark.unit
    def test_ramstksimilaritem_create(self, mock_program_dao):
        """__init__() should create an RAMSTKSimilarItem model."""
        DUT = mock_program_dao.do_select_all(RAMSTKSimilarItem)[0]

        assert isinstance(DUT, RAMSTKSimilarItem)
        assert DUT.__tablename__ == 'ramstk_similar_item'
        assert DUT.revision_id == 1
        assert DUT.hardware_id == 1
        assert DUT.change_description_1 == ''
        assert DUT.change_description_2 == ''
        assert DUT.change_description_3 == ''
        assert DUT.change_description_4 == ''
        assert DUT.change_description_5 == ''
        assert DUT.change_description_6 == ''
        assert DUT.change_description_7 == ''
        assert DUT.change_description_8 == ''
        assert DUT.change_description_9 == ''
        assert DUT.change_description_10 == ''
        assert DUT.change_factor_1 == 1.0
        assert DUT.change_factor_2 == 1.0
        assert DUT.change_factor_3 == 1.0
        assert DUT.change_factor_4 == 1.0
        assert DUT.change_factor_5 == 1.0
        assert DUT.change_factor_6 == 1.0
        assert DUT.change_factor_7 == 1.0
        assert DUT.change_factor_8 == 1.0
        assert DUT.change_factor_9 == 1.0
        assert DUT.change_factor_10 == 1.0
        assert DUT.environment_from_id == 0
        assert DUT.environment_to_id == 0
        assert DUT.function_1 == '0'
        assert DUT.function_2 == '0'
        assert DUT.function_3 == '0'
        assert DUT.function_4 == '0'
        assert DUT.function_5 == '0'
        assert DUT.similar_item_method_id == 1
        assert DUT.parent_id == 0
        assert DUT.quality_from_id == 0
        assert DUT.quality_to_id == 0
        assert DUT.result_1 == 0.0
        assert DUT.result_2 == 0.0
        assert DUT.result_3 == 0.0
        assert DUT.result_4 == 0.0
        assert DUT.result_5 == 0.0
        assert DUT.temperature_from == 30.0
        assert DUT.temperature_to == 30.0
        assert DUT.user_blob_1 == ''
        assert DUT.user_blob_2 == ''
        assert DUT.user_blob_3 == ''
        assert DUT.user_blob_4 == ''
        assert DUT.user_blob_5 == ''
        assert DUT.user_float_1 == 0.0
        assert DUT.user_float_2 == 0.0
        assert DUT.user_float_3 == 0.0
        assert DUT.user_float_4 == 0.0
        assert DUT.user_float_5 == 0.0
        assert DUT.user_int_1 == 0
        assert DUT.user_int_2 == 0
        assert DUT.user_int_3 == 0
        assert DUT.user_int_4 == 0
        assert DUT.user_int_5 == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKSimilarItem)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['hardware_id'] == 1
        assert _attributes['change_description_1'] == ''
        assert _attributes['change_description_2'] == ''
        assert _attributes['change_description_3'] == ''
        assert _attributes['change_description_4'] == ''
        assert _attributes['change_description_5'] == ''
        assert _attributes['change_description_6'] == ''
        assert _attributes['change_description_7'] == ''
        assert _attributes['change_description_8'] == ''
        assert _attributes['change_description_9'] == ''
        assert _attributes['change_description_10'] == ''
        assert _attributes['change_factor_1'] == 1.0
        assert _attributes['change_factor_2'] == 1.0
        assert _attributes['change_factor_3'] == 1.0
        assert _attributes['change_factor_4'] == 1.0
        assert _attributes['change_factor_5'] == 1.0
        assert _attributes['change_factor_6'] == 1.0
        assert _attributes['change_factor_7'] == 1.0
        assert _attributes['change_factor_8'] == 1.0
        assert _attributes['change_factor_9'] == 1.0
        assert _attributes['change_factor_10'] == 1.0
        assert _attributes['environment_from_id'] == 0
        assert _attributes['environment_to_id'] == 0
        assert _attributes['function_1'] == '0'
        assert _attributes['function_2'] == '0'
        assert _attributes['function_3'] == '0'
        assert _attributes['function_4'] == '0'
        assert _attributes['function_5'] == '0'
        assert _attributes['similar_item_method_id'] == 1
        assert _attributes['parent_id'] == 0
        assert _attributes['quality_from_id'] == 0
        assert _attributes['quality_to_id'] == 0
        assert _attributes['result_1'] == 0.0
        assert _attributes['result_2'] == 0.0
        assert _attributes['result_3'] == 0.0
        assert _attributes['result_4'] == 0.0
        assert _attributes['result_5'] == 0.0
        assert _attributes['temperature_from'] == 30.0
        assert _attributes['temperature_to'] == 30.0
        assert _attributes['user_blob_1'] == ''
        assert _attributes['user_blob_2'] == ''
        assert _attributes['user_blob_3'] == ''
        assert _attributes['user_blob_4'] == ''
        assert _attributes['user_blob_5'] == ''
        assert _attributes['user_float_1'] == 0.0
        assert _attributes['user_float_2'] == 0.0
        assert _attributes['user_float_3'] == 0.0
        assert _attributes['user_float_4'] == 0.0
        assert _attributes['user_float_5'] == 0.0
        assert _attributes['user_int_1'] == 0
        assert _attributes['user_int_2'] == 0
        assert _attributes['user_int_3'] == 0
        assert _attributes['user_int_4'] == 0
        assert _attributes['user_int_5'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return None on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKSimilarItem)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKSimilarItem)[0]

        ATTRIBUTES['change_factor_3'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['change_factor_3'] == 1.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKSimilarItem)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
