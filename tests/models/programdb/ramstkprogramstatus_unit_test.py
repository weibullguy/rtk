# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkprogramstatus_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing RAMSTKProgramStatus module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKProgramStatus


@pytest.fixture
def mock_program_dao(monkeypatch):
    _status_1 = RAMSTKProgramStatus()
    _status_1.revision_id = 1
    _status_1.status_id = 1
    _status_1.cost_remaining = 500.0
    _status_1.date_status = date.today()
    _status_1.time_remaining = 10.0

    _status_2 = RAMSTKProgramStatus()
    _status_2.revision_id = 1
    _status_2.status_id = 1
    _status_2.cost_remaining = 550.0
    _status_2.date_status = date.today() - timedelta(1)
    _status_2.time_remaining = 18.0

    DAO = MockDAO()
    DAO.table = [
        _status_1,
    ]

    yield DAO


ATTRIBUTES = {
    'cost_remaining': 0.0,
    'date_status': date.today() + timedelta(7),
    'time_remaining': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKProgramStatus:
    """Class for testing the RAMSTKProgramStatus model."""
    @pytest.mark.unit
    def test_ramstkprogramstatus_create(self, mock_program_dao):
        """__init__() should create an RAMSTKProgramStatus model."""
        DUT = mock_program_dao.do_select_all(RAMSTKProgramStatus)[0]

        assert isinstance(DUT, RAMSTKProgramStatus)
        assert DUT.__tablename__ == 'ramstk_program_status'
        assert DUT.revision_id == 1
        assert DUT.status_id == 1
        assert DUT.cost_remaining == 500.0
        assert DUT.date_status == date.today()
        assert DUT.time_remaining == 10.0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKProgramStatus)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['status_id'] == 1
        assert _attributes['cost_remaining'] == 500.0
        assert _attributes['date_status'] == date.today()
        assert _attributes['time_remaining'] == 10.0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKProgramStatus)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.cost_remaining == 0.0
        assert DUT.date_status == date.today() + timedelta(7)
        assert DUT.time_remaining == 0.0

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKProgramStatus)[0]

        ATTRIBUTES['time_remaining'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['time_remaining'] == 0.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKProgramStatus)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
