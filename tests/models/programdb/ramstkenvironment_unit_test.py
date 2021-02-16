# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkenvironment.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKEnvironment module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKEnvironment


@pytest.fixture
def mock_program_dao(monkeypatch):
    _environment_1 = RAMSTKEnvironment()
    _environment_1.phase_id = 1
    _environment_1.environment_id = 1
    _environment_1.name = 'Condition Name'
    _environment_1.units = 'Units'
    _environment_1.minimum = 0.0
    _environment_1.maximum = 0.0
    _environment_1.mean = 0.0
    _environment_1.variance = 0.0
    _environment_1.ramp_rate = 0.0
    _environment_1.low_dwell_time = 0.0
    _environment_1.high_dwell_time = 0.0

    _environment_2 = RAMSTKEnvironment()
    _environment_2.phase_id = 1
    _environment_2.environment_id = 2
    _environment_2.name = 'Condition Name'
    _environment_2.units = 'Units'
    _environment_2.minimum = 0.0
    _environment_2.maximum = 0.0
    _environment_2.mean = 0.0
    _environment_2.variance = 0.0
    _environment_2.ramp_rate = 0.0
    _environment_2.low_dwell_time = 0.0
    _environment_2.high_dwell_time = 0.0

    _environment_3 = RAMSTKEnvironment()
    _environment_3.phase_id = 1
    _environment_3.environment_id = 3
    _environment_3.name = 'Condition Name'
    _environment_3.units = 'Units'
    _environment_3.minimum = 0.0
    _environment_3.maximum = 0.0
    _environment_3.mean = 0.0
    _environment_3.variance = 0.0
    _environment_3.ramp_rate = 0.0
    _environment_3.low_dwell_time = 0.0
    _environment_3.high_dwell_time = 0.0

    DAO = MockDAO()
    DAO.table = [
        _environment_1,
        _environment_2,
        _environment_3,
    ]

    yield DAO


ATTRIBUTES = {
    'high_dwell_time': 0.0,
    'low_dwell_time': 0.0,
    'maximum': 0.0,
    'mean': 0.0,
    'minimum': 0.0,
    'name': 'Condition Name',
    'ramp_rate': 0.0,
    'units': 'Units',
    'variance': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKEnvironment:
    """Class for testing the RAMSTKEnvironment model."""
    @pytest.mark.unit
    def test_ramstkenvironment_create(self, mock_program_dao):
        """__init__() should create an RAMSTKEnvironment model."""
        DUT = mock_program_dao.do_select_all(RAMSTKEnvironment)[0]

        assert isinstance(DUT, RAMSTKEnvironment)
        assert DUT.__tablename__ == 'ramstk_environment'
        assert DUT.phase_id == 1
        assert DUT.environment_id == 1
        assert DUT.name == 'Condition Name'
        assert DUT.units == 'Units'
        assert DUT.minimum == 0.0
        assert DUT.maximum == 0.0
        assert DUT.mean == 0.0
        assert DUT.variance == 0.0
        assert DUT.ramp_rate == 0.0
        assert DUT.low_dwell_time == 0.0
        assert DUT.high_dwell_time == 0.0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKEnvironment)[0]

        _attributes = DUT.get_attributes()

        assert _attributes['high_dwell_time'] == 0.0
        assert _attributes['low_dwell_time'] == 0.0
        assert _attributes['maximum'] == 0.0
        assert _attributes['mean'] == 0.0
        assert _attributes['minimum'] == 0.0
        assert _attributes['name'] == 'Condition Name'
        assert _attributes['ramp_rate'] == 0.0
        assert _attributes['units'] == 'Units'
        assert _attributes['variance'] == 0.0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKEnvironment)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_set_default(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKEnvironment)[0]

        ATTRIBUTES['mean'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['mean'] == 0.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKEnvironment)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
