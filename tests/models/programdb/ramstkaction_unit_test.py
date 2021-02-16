# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkaction_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKAction module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKAction


@pytest.fixture
def mock_program_dao(monkeypatch):
    _action_1 = RAMSTKAction()
    _action_1.revision_id = 1
    _action_1.cause_id = 1
    _action_1.action_id = 1
    _action_1.action_due_date = date(2019, 8, 20)
    _action_1.action_approve_date = date(2019, 8, 20)
    _action_1.action_status = ''
    _action_1.action_closed = 0
    _action_1.action_taken = ''
    _action_1.action_close_date = date(2019, 8, 20)
    _action_1.action_recommended = 'Test Action #1'
    _action_1.action_category = ''
    _action_1.action_owner = ''
    _action_1.action_approved = 0

    DAO = MockDAO()
    DAO.table = [
        _action_1,
    ]

    yield DAO


ATTRIBUTES = {
    'action_due_date': date(2019, 8, 20),
    'action_approve_date': date(2019, 8, 20),
    'action_status': '',
    'action_closed': 0,
    'action_taken': '',
    'action_close_date': date(2019, 8, 20),
    'action_recommended': 'Recommended action for Failure Cause #1',
    'action_category': '',
    'action_owner': '',
    'action_approved': 0,
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKAction:
    """Class for testing the RAMSTKAction model."""
    @pytest.mark.unit
    def test_ramstkaction_create(self, mock_program_dao):
        """__init__() should create an RAMSTKAction model."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        assert isinstance(DUT, RAMSTKAction)
        assert DUT.__tablename__ == 'ramstk_action'
        assert DUT.cause_id == 1
        assert DUT.action_id == 1
        assert DUT.action_recommended == 'Test Action #1'
        assert DUT.action_category == ''
        assert DUT.action_owner == ''
        assert DUT.action_due_date == date(2019, 8, 20)
        assert DUT.action_status == ''
        assert DUT.action_taken == ''
        assert DUT.action_approved == 0
        assert DUT.action_approve_date == date(2019, 8, 20)
        assert DUT.action_closed == 0
        assert DUT.action_close_date == date(2019, 8, 20)

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['cause_id'] == 1
        assert _attributes['action_id'] == 1
        assert _attributes['action_recommended'] == 'Test Action #1'
        assert _attributes['action_category'] == ''
        assert _attributes['action_owner'] == ''
        assert _attributes['action_due_date'] == date(2019, 8, 20)
        assert _attributes['action_status'] == ''
        assert _attributes['action_taken'] == ''
        assert _attributes['action_approved'] == 0
        assert _attributes['action_approve_date'] == date(2019, 8, 20)
        assert _attributes['action_closed'] == 0
        assert _attributes['action_close_date'] == date(2019, 8, 20)

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        ATTRIBUTES['action_status'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['action_recommended'] == (
            'Recommended action for Failure Cause #1')
        assert DUT.get_attributes()['action_status'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKAction)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
