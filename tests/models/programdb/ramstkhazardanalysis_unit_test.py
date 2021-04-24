# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.ramstkhazardanalysis_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing RAMSTKHazardAnalysis module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKHazardAnalysis


@pytest.fixture
def mock_program_dao(monkeypatch):
    _hazard_1 = RAMSTKHazardAnalysis()
    _hazard_1.revision_id = 1
    _hazard_1.function_id = 1
    _hazard_1.hazard_id = 1
    _hazard_1.user_blob_3 = ''
    _hazard_1.user_blob_2 = ''
    _hazard_1.user_blob_1 = ''
    _hazard_1.system_severity = 'Medium'
    _hazard_1.result_2 = 0.0
    _hazard_1.result_3 = 0.0
    _hazard_1.assembly_probability = 'Level A - Frequent'
    _hazard_1.system_probability = 'Level A - Frequent'
    _hazard_1.system_probability_f = 'Level A - Frequent'
    _hazard_1.assembly_hri = 20
    _hazard_1.system_hri = 20
    _hazard_1.system_effect = ''
    _hazard_1.user_int_1 = 0
    _hazard_1.user_float_3 = 0.0
    _hazard_1.result_4 = 0.0
    _hazard_1.user_float_1 = 0.0
    _hazard_1.potential_hazard = ''
    _hazard_1.remarks = ''
    _hazard_1.system_hri_f = 20
    _hazard_1.result_5 = 0.0
    _hazard_1.assembly_severity = 'Medium'
    _hazard_1.assembly_probability_f = 'Level A - Frequent'
    _hazard_1.assembly_hri_f = 4
    _hazard_1.assembly_effect = ''
    _hazard_1.function_4 = ''
    _hazard_1.potential_cause = ''
    _hazard_1.system_mitigation = ''
    _hazard_1.function_3 = ''
    _hazard_1.function_2 = ''
    _hazard_1.function_1 = ''
    _hazard_1.user_int_3 = 0
    _hazard_1.user_int_2 = 0
    _hazard_1.assembly_severity_f = 'Medium'
    _hazard_1.system_severity_f = 'Medium'
    _hazard_1.assembly_mitigation = ''
    _hazard_1.function_5 = ''
    _hazard_1.result_1 = 0.0
    _hazard_1.user_float_2 = 0.0

    DAO = MockDAO()
    DAO.table = [
        _hazard_1,
    ]

    yield DAO


ATTRIBUTES = {
    'user_blob_3': '',
    'user_blob_2': '',
    'user_blob_1': '',
    'system_severity': 'Medium',
    'result_2': 0.0,
    'result_3': 0.0,
    'assembly_probability': 'Level A - Frequent',
    'system_probability': 'Level A - Frequent',
    'system_probability_f': 'Level A - Frequent',
    'assembly_hri': 20,
    'system_hri': 20,
    'system_effect': '',
    'user_int_1': 0,
    'user_float_3': 0.0,
    'result_4': 0.0,
    'user_float_1': 0.0,
    'potential_hazard': '',
    'remarks': '',
    'system_hri_f': 20,
    'result_5': 0.0,
    'assembly_severity': 'Medium',
    'assembly_probability_f': 'Level A - Frequent',
    'assembly_hri_f': 4,
    'assembly_effect': '',
    'function_4': '',
    'potential_cause': '',
    'system_mitigation': '',
    'function_3': '',
    'function_2': '',
    'function_1': '',
    'user_int_3': 0,
    'user_int_2': 0,
    'assembly_severity_f': 'Medium',
    'system_severity_f': 'Medium',
    'assembly_mitigation': '',
    'function_5': '',
    'result_1': 0.0,
    'user_float_2': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKHazardAnalysis:
    """Class for testing the RAMSTKHazardAnalysis model."""
    @pytest.mark.unit
    def test_ramstkallocation_create(self, mock_program_dao):
        """__init__() should create an RAMSTKHazardAnalysis model."""
        DUT = mock_program_dao.do_select_all(RAMSTKHazardAnalysis)[0]

        assert isinstance(DUT, RAMSTKHazardAnalysis)
        assert DUT.__tablename__ == 'ramstk_hazard_analysis'
        assert DUT.revision_id == 1
        assert DUT.function_id == 1
        assert DUT.hazard_id == 1
        assert DUT.potential_hazard == ''
        assert DUT.potential_cause == ''
        assert DUT.assembly_effect == ''
        assert DUT.assembly_severity == 'Medium'
        assert DUT.assembly_probability == 'Level A - Frequent'
        assert DUT.assembly_hri == 20
        assert DUT.assembly_mitigation == ''
        assert DUT.assembly_severity_f == 'Medium'
        assert DUT.assembly_probability_f == 'Level A - Frequent'
        assert DUT.assembly_hri_f == 4
        assert DUT.function_1 == ''
        assert DUT.function_2 == ''
        assert DUT.function_3 == ''
        assert DUT.function_4 == ''
        assert DUT.function_5 == ''
        assert DUT.remarks == ''
        assert DUT.result_1 == 0.0
        assert DUT.result_2 == 0.0
        assert DUT.result_3 == 0.0
        assert DUT.result_4 == 0.0
        assert DUT.result_5 == 0.0
        assert DUT.system_effect == ''
        assert DUT.system_severity == 'Medium'
        assert DUT.system_probability == 'Level A - Frequent'
        assert DUT.system_hri == 20
        assert DUT.system_mitigation == ''
        assert DUT.system_severity_f == 'Medium'
        assert DUT.system_probability_f == 'Level A - Frequent'
        assert DUT.system_hri_f == 20
        assert DUT.user_blob_1 == ''
        assert DUT.user_blob_2 == ''
        assert DUT.user_blob_3 == ''
        assert DUT.user_float_1 == 0.0
        assert DUT.user_float_2 == 0.0
        assert DUT.user_float_3 == 0.0
        assert DUT.user_int_1 == 0
        assert DUT.user_int_2 == 0
        assert DUT.user_int_3 == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKHazardAnalysis)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['revision_id'] == 1
        assert _attributes['function_id'] == 1
        assert _attributes['hazard_id'] == 1
        assert _attributes['potential_hazard'] == ''
        assert _attributes['potential_cause'] == ''
        assert _attributes['assembly_effect'] == ''
        assert _attributes['assembly_severity'] == 'Medium'
        assert _attributes['assembly_probability'] == 'Level A - Frequent'
        assert _attributes['assembly_hri'] == 20
        assert _attributes['assembly_mitigation'] == ''
        assert _attributes['assembly_severity_f'] == 'Medium'
        assert _attributes['assembly_probability_f'] == 'Level A - Frequent'
        assert _attributes['assembly_hri_f'] == 4
        assert _attributes['function_1'] == ''
        assert _attributes['function_2'] == ''
        assert _attributes['function_3'] == ''
        assert _attributes['function_4'] == ''
        assert _attributes['function_5'] == ''
        assert _attributes['remarks'] == ''
        assert _attributes['result_1'] == 0.0
        assert _attributes['result_2'] == 0.0
        assert _attributes['result_3'] == 0.0
        assert _attributes['result_4'] == 0.0
        assert _attributes['result_5'] == 0.0
        assert _attributes['system_effect'] == ''
        assert _attributes['system_severity'] == 'Medium'
        assert _attributes['system_probability'] == 'Level A - Frequent'
        assert _attributes['system_hri'] == 20
        assert _attributes['system_mitigation'] == ''
        assert _attributes['system_severity_f'] == 'Medium'
        assert _attributes['system_probability_f'] == 'Level A - Frequent'
        assert _attributes['system_hri_f'] == 20
        assert _attributes['user_blob_1'] == ''
        assert _attributes['user_blob_2'] == ''
        assert _attributes['user_blob_3'] == ''
        assert _attributes['user_float_1'] == 0.0
        assert _attributes['user_float_2'] == 0.0
        assert _attributes['user_float_3'] == 0.0
        assert _attributes['user_int_1'] == 0
        assert _attributes['user_int_2'] == 0
        assert _attributes['user_int_3'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKHazardAnalysis)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKHazardAnalysis)[0]

        ATTRIBUTES['remarks'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['remarks'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKHazardAnalysis)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
