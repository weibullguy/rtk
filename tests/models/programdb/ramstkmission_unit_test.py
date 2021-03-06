# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkmission.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMission module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMission


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_1 = RAMSTKMission()
    _mission_1.revision_id = 1
    _mission_1.mission_id = 1
    _mission_1.description = 'Test Mission #1'
    _mission_1.mission_time = 0.0
    _mission_1.time_units = 'hours'

    _mission_2 = RAMSTKMission()
    _mission_2.revision_id = 1
    _mission_2.mission_id = 1
    _mission_2.description = 'Test Mission #2'
    _mission_2.mission_time = 0.0
    _mission_2.time_units = 'hours'

    DAO = MockDAO()
    DAO.table = [
        _mission_1,
        _mission_2,
    ]

    yield DAO


ATTRIBUTES = {
    'description': 'Test Mission',
    'mission_time': 0.0,
    'time_units': 'hours'
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKMission:
    """Class for testing the RAMSTKMission model."""
    @pytest.mark.unit
    def test_ramstkmission_create(self, mock_program_dao):
        """__init__() should create an RAMSTKMission model."""
        DUT = mock_program_dao.do_select_all(RAMSTKMission)[0]

        assert isinstance(DUT, RAMSTKMission)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mission'
        assert DUT.revision_id == 1
        assert DUT.mission_id == 1
        assert DUT.description == 'Test Mission #1'
        assert DUT.mission_time == 0.0
        assert DUT.time_units == 'hours'

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKMission)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['description'] == 'Test Mission #1'
        assert _attributes['mission_time'] == 0.0
        assert _attributes['time_units'] == 'hours'

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKMission)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKMission)[0]

        ATTRIBUTES['mission_time'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['mission_time'] == 0.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKMission)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
