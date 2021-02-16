# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkopload_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKOpLoad module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKOpLoad


@pytest.fixture
def mock_program_dao(monkeypatch):
    _opload_1 = RAMSTKOpLoad()
    _opload_1.revision_id = 1
    _opload_1.mechanism_id = 1
    _opload_1.load_id = 1
    _opload_1.damage_model = ''
    _opload_1.description = 'Test Operating Load'
    _opload_1.priority_id = 0

    DAO = MockDAO()
    DAO.table = [
        _opload_1,
    ]

    yield DAO


ATTRIBUTES = {
    'damage_model': 'Big Math Model',
    'description': 'Big Operating Load',
    'priority_id': 0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKOpLoad:
    """Class for testing the RAMSTKOpLoad model."""
    @pytest.mark.unit
    def test_ramstkopload_create(self, mock_program_dao):
        """__init__() should create an RAMSTKOpLoad model."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpLoad)[0]

        assert isinstance(DUT, RAMSTKOpLoad)
        assert DUT.__tablename__ == 'ramstk_op_load'
        assert DUT.mechanism_id == 1
        assert DUT.load_id == 1
        assert DUT.description == 'Test Operating Load'
        assert DUT.damage_model == ''
        assert DUT.priority_id == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpLoad)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['mechanism_id'] == 1
        assert _attributes['load_id'] == 1
        assert _attributes['description'] == 'Test Operating Load'
        assert _attributes['damage_model'] == ''
        assert _attributes['priority_id'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpLoad)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.description == 'Big Operating Load'
        assert DUT.damage_model == 'Big Math Model'
        assert DUT.priority_id == 0

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpLoad)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKOpLoad)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
