# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstktestmethod_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKTestMethod module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKTestMethod


@pytest.fixture
def mock_program_dao(monkeypatch):
    _testmethod_1 = RAMSTKTestMethod()
    _testmethod_1.revision_id = 1
    _testmethod_1.load_id = 1
    _testmethod_1.test_id = 1
    _testmethod_1.boundary_conditions = 'Big boundary conditions'
    _testmethod_1.description = 'Test Test Method #1'
    _testmethod_1.remarks = 'Doyle Rowland'

    DAO = MockDAO()
    DAO.table = [
        _testmethod_1,
    ]

    yield DAO


ATTRIBUTES = {
    'remarks': '',
    'boundary_conditions': '',
    'description': 'Big Test Method'
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKTestMethod():
    @pytest.mark.unit
    def test_ramstkopstress_create(self, mock_program_dao):
        """__init__() should create an RAMSTKTestMethod model."""
        DUT = mock_program_dao.do_select_all(RAMSTKTestMethod)[0]

        assert isinstance(DUT, RAMSTKTestMethod)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_test_method'
        assert DUT.load_id == 1
        assert DUT.test_id == 1
        assert DUT.description == 'Test Test Method #1'
        assert DUT.boundary_conditions == 'Big boundary conditions'
        assert DUT.remarks == 'Doyle Rowland'

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKTestMethod)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['load_id'] == 1
        assert _attributes['test_id'] == 1
        assert _attributes['description'] == 'Test Test Method #1'
        assert _attributes['boundary_conditions'] == 'Big boundary conditions'
        assert _attributes['remarks'] == 'Doyle Rowland'

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKTestMethod)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.boundary_conditions == ''
        assert DUT.description == 'Big Test Method'
        assert DUT.remarks == ''

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKTestMethod)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKTestMethod)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
