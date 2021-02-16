# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkfunction_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKFunction module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKFunction


@pytest.fixture
def mock_program_dao(monkeypatch):
    _function_1 = RAMSTKFunction()
    _function_1.revision_id = 1
    _function_1.function_id = 1
    _function_1.availability_logistics = 1.0
    _function_1.availability_mission = 1.0
    _function_1.cost = 0.0
    _function_1.function_code = 'PRESS-001'
    _function_1.hazard_rate_logistics = 0.0
    _function_1.hazard_rate_mission = 0.0
    _function_1.level = 0
    _function_1.mcmt = 0.0
    _function_1.mmt = 0.0
    _function_1.mpmt = 0.0
    _function_1.mtbf_logistics = 0.0
    _function_1.mtbf_mission = 0.0
    _function_1.mttr = 0.0
    _function_1.name = 'Function Name'
    _function_1.parent_id = 0
    _function_1.remarks = ''
    _function_1.safety_critical = 0
    _function_1.total_mode_count = 0
    _function_1.total_part_count = 0
    _function_1.type_id = 0

    _function_2 = RAMSTKFunction()
    _function_2.revision_id = 1
    _function_2.function_id = 2
    _function_2.availability_logistics = 1.0
    _function_2.availability_mission = 1.0
    _function_2.cost = 0.0
    _function_2.function_code = 'PRESS-001'
    _function_2.hazard_rate_logistics = 0.0
    _function_2.hazard_rate_mission = 0.0
    _function_2.level = 0
    _function_2.mcmt = 0.0
    _function_2.mmt = 0.0
    _function_2.mpmt = 0.0
    _function_2.mtbf_logistics = 0.0
    _function_2.mtbf_mission = 0.0
    _function_2.mttr = 0.0
    _function_2.name = 'Function Name'
    _function_2.parent_id = 0
    _function_2.remarks = ''
    _function_2.safety_critical = 0
    _function_2.total_mode_count = 0
    _function_2.total_part_count = 0
    _function_2.type_id = 0

    DAO = MockDAO()
    DAO.table = [
        _function_1,
        _function_2,
    ]

    yield DAO


ATTRIBUTES = {
    'availability_logistics': 1.0,
    'availability_mission': 1.0,
    'cost': 0.0,
    'function_code': 'FUNC-0001',
    'hazard_rate_logistics': 0.0,
    'hazard_rate_mission': 0.0,
    'level': 0,
    'mcmt': 0.0,
    'mmt': 0.0,
    'mpmt': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mttr': 0.0,
    'name': 'Function Name',
    'parent_id': 0,
    'remarks': b'',
    'safety_critical': 0,
    'total_part_count': 0,
    'total_mode_count': 0,
    'type_id': 0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKFunction():
    """Class for testing the RAMSTKFunction model."""
    @pytest.mark.unit
    def test_ramstkfunction_create(self, mock_program_dao):
        """__init__() should create an RAMSTKFunction model."""
        DUT = mock_program_dao.do_select_all(RAMSTKFunction)[0]

        assert isinstance(DUT, RAMSTKFunction)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_function'
        assert DUT.revision_id == 1
        assert DUT.function_id == 1
        assert DUT.availability_logistics == 1.0
        assert DUT.availability_mission == 1.0
        assert DUT.cost == 0.0
        assert DUT.function_code == 'PRESS-001'
        assert DUT.hazard_rate_logistics == 0.0
        assert DUT.hazard_rate_mission == 0.0
        assert DUT.level == 0
        assert DUT.mmt == 0.0
        assert DUT.mcmt == 0.0
        assert DUT.mpmt == 0.0
        assert DUT.mtbf_logistics == 0.0
        assert DUT.mtbf_mission == 0.0
        assert DUT.mttr == 0.0
        assert DUT.name == 'Function Name'
        assert DUT.parent_id == 0
        assert DUT.remarks == ''
        assert DUT.safety_critical == 0
        assert DUT.total_mode_count == 0
        assert DUT.total_part_count == 0
        assert DUT.type_id == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of {attribute name:attribute
        value} pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKFunction)[0]

        _attributes = DUT.get_attributes()

        assert _attributes['revision_id'] == 1
        assert _attributes['function_id'] == 1
        assert _attributes['availability_logistics'] == 1.0
        assert _attributes['availability_mission'] == 1.0
        assert _attributes['cost'] == 0.0
        assert _attributes['function_code'] == 'PRESS-001'
        assert _attributes['hazard_rate_logistics'] == 0.0
        assert _attributes['hazard_rate_mission'] == 0.0
        assert _attributes['level'] == 0
        assert _attributes['mmt'] == 0.0
        assert _attributes['mcmt'] == 0.0
        assert _attributes['mpmt'] == 0.0
        assert _attributes['mtbf_logistics'] == 0.0
        assert _attributes['mtbf_mission'] == 0.0
        assert _attributes['mttr'] == 0.0
        assert _attributes['name'] == 'Function Name'
        assert _attributes['parent_id'] == 0
        assert _attributes['remarks'] == ''
        assert _attributes['safety_critical'] == 0
        assert _attributes['total_mode_count'] == 0
        assert _attributes['total_part_count'] == 0
        assert _attributes['type_id'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKFunction)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['function_code'] == 'FUNC-0001'

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKFunction)[0]

        ATTRIBUTES['total_mode_count'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['total_mode_count'] == 0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKFunction)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
