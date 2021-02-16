# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkopstress_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKOpStress module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKOpStress


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opstress_1 = RAMSTKOpStress()
    _opstress_1.revision_id = 1
    _opstress_1.mechanism_id = 1
    _opstress_1.load_id = 1
    _opstress_1.stress_id = 1
    _opstress_1.description = 'Test Operating Stress #1'
    _opstress_1.load_history = 'Waterfall histogram'
    _opstress_1.measurable_parameter = ''
    _opstress_1.remarks = ''

    DAO = MockDAO()
    DAO.table = [
        _opstress_1,
    ]

    yield DAO


ATTRIBUTES = {
    'description': 'Big Operating Stress',
    'load_history': '',
    'measurable_parameter': '',
    'remarks': '',
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKOpStress():
    """Class for testing the RAMSTKOpStress model."""
    @pytest.mark.unit
    def test_ramstkopstress_create(self, mock_program_dao):
        """__init__() should create an RAMSTKOpStress model."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpStress)[0]

        assert isinstance(DUT, RAMSTKOpStress)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_op_stress'
        assert DUT.load_id == 1
        assert DUT.stress_id == 1
        assert DUT.description == 'Test Operating Stress #1'
        assert DUT.measurable_parameter == ''
        assert DUT.load_history == 'Waterfall histogram'
        assert DUT.remarks == ''

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpStress)[0]

        _attributes = DUT.get_attributes()

        assert _attributes['load_id'] == 1
        assert _attributes['stress_id'] == 1
        assert _attributes['description'] == 'Test Operating Stress #1'
        assert _attributes['measurable_parameter'] == ''
        assert _attributes['load_history'] == 'Waterfall histogram'
        assert _attributes['remarks'] == ''

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpStress)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.description == 'Big Operating Stress'

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpStress)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpStress)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
