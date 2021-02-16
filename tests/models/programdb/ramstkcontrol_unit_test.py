# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkcontrol_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKControl module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKControl


@pytest.fixture
def mock_program_dao(monkeypatch):
    _control_1 = RAMSTKControl()
    _control_1.revision_id = 1
    _control_1.mode_id = 5
    _control_1.mechanism_id = 1
    _control_1.cause_id = 1
    _control_1.control_id = 1
    _control_1.description = 'Test Control #1'
    _control_1.type_id = 'Detection'

    _control_2 = RAMSTKControl()
    _control_2.revision_id = 1
    _control_2.mode_id = 5
    _control_2.mechanism_id = 1
    _control_2.cause_id = 1
    _control_2.control_id = 2
    _control_2.description = 'Test Control #2'
    _control_2.type_id = 'Prevention'

    DAO = MockDAO()
    DAO.table = [
        _control_1,
        _control_2,
    ]

    yield DAO


ATTRIBUTES = {'description': 'Big Test Control', 'type_id': 'Good Type'}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKControl():
    """Class for testing the RAMSTKControl model."""
    @pytest.mark.unit
    def test_ramstkcontrol_create(self, mock_program_dao):
        """__init__() should create an RAMSTKControl model."""
        DUT = mock_program_dao.do_select_all(RAMSTKControl)[0]

        assert isinstance(DUT, RAMSTKControl)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_control'
        assert DUT.cause_id == 1
        assert DUT.control_id == 1
        assert DUT.description == 'Test Control #1'
        assert DUT.type_id == 'Detection'

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dictionary of attribute key:value
        pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKControl)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['cause_id'] == 1
        assert _attributes['control_id'] == 1
        assert _attributes['description'] == 'Test Control #1'
        assert _attributes['type_id'] == 'Detection'

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKControl)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.description == 'Big Test Control'
        assert DUT.type_id == 'Good Type'

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKControl)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKControl)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
