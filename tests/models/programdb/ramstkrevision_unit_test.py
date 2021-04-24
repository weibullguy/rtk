# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkrevision.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKRevision module algorithms and models."""

# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKRevision


@pytest.fixture
def mock_program_dao(monkeypatch):
    _revision_1 = RAMSTKRevision()
    _revision_1.revision_id = 1
    _revision_1.availability_logistics = 0.9986
    _revision_1.availability_mission = 0.99934
    _revision_1.cost = 12532.15
    _revision_1.cost_failure = 0.0000352
    _revision_1.cost_hour = 1.2532
    _revision_1.hazard_rate_active = 0.0
    _revision_1.hazard_rate_dormant = 0.0
    _revision_1.hazard_rate_logistics = 0.0
    _revision_1.hazard_rate_mission = 0.0
    _revision_1.hazard_rate_software = 0.0
    _revision_1.mmt = 0.0
    _revision_1.mcmt = 0.0
    _revision_1.mpmt = 0.0
    _revision_1.mtbf_logistics = 0.0
    _revision_1.mtbf_mission = 0.0
    _revision_1.mttr = 0.0
    _revision_1.name = 'Original Revision'
    _revision_1.reliability_logistics = 0.99986
    _revision_1.reliability_mission = 0.99992
    _revision_1.remarks = 'This is the original revision.'
    _revision_1.revision_code = 'Rev. -'
    _revision_1.program_time = 2562
    _revision_1.program_time_sd = 26.83
    _revision_1.program_cost = 26492.83
    _revision_1.program_cost_sd = 15.62

    _revision_2 = RAMSTKRevision()
    _revision_2.revision_id = 2
    _revision_2.availability_logistics = 1.0
    _revision_2.availability_mission = 1.0
    _revision_2.cost = 0.0
    _revision_2.cost_failure = 0.0
    _revision_2.cost_hour = 0.0
    _revision_2.hazard_rate_active = 0.0
    _revision_2.hazard_rate_dormant = 0.0
    _revision_2.hazard_rate_logistics = 0.0
    _revision_2.hazard_rate_mission = 0.0
    _revision_2.hazard_rate_software = 0.0
    _revision_2.mmt = 0.0
    _revision_2.mcmt = 0.0
    _revision_2.mpmt = 0.0
    _revision_2.mtbf_logistics = 0.0
    _revision_2.mtbf_mission = 0.0
    _revision_2.mttr = 0.0
    _revision_2.name = 'Revision A'
    _revision_2.reliability_logistics = 1.0
    _revision_2.reliability_mission = 1.0
    _revision_2.remarks = 'This is the second revision.'
    _revision_2.revision_code = 'Rev. A'
    _revision_2.program_time = 0
    _revision_2.program_time_sd = 0.0
    _revision_2.program_cost = 0.0
    _revision_2.program_cost_sd = 0.0

    DAO = MockDAO()
    DAO.table = [
        _revision_1,
        _revision_2,
    ]

    yield DAO


ATTRIBUTES = {
    'availability_logistics': 1.0,
    'availability_mission': 1.0,
    'cost': 0.0,
    'cost_failure': 0.0,
    'cost_hour': 0.0,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_software': 0.0,
    'mmt': 0.0,
    'mcmt': 0.0,
    'mpmt': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mttr': 0.0,
    'name': 'Test Revision',
    'reliability_logistics': 1.0,
    'reliability_mission': 1.0,
    'remarks': '',
    'total_part_count': 1,
    'revision_code': '',
    'program_time': 0.0,
    'program_time_sd': 0.0,
    'program_cost': 0.0,
    'program_cost_sd': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKRevision():
    """Class for testing the RAMSTKRevision model."""
    @pytest.mark.unit
    def test_ramstkrevision_create(self, mock_program_dao):
        """__init__() should create an RAMSTKRevision model."""
        DUT = mock_program_dao.do_select_all(RAMSTKRevision)[0]

        assert isinstance(DUT, RAMSTKRevision)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_revision'
        assert DUT.revision_id == 1
        assert DUT.availability_logistics == 0.9986
        assert DUT.availability_mission == 0.99934
        assert DUT.cost == 12532.15
        assert DUT.cost_failure == 0.0000352
        assert DUT.cost_hour == 1.2532
        assert DUT.hazard_rate_active == 0.0
        assert DUT.hazard_rate_dormant == 0.0
        assert DUT.hazard_rate_logistics == 0.0
        assert DUT.hazard_rate_mission == 0.0
        assert DUT.hazard_rate_software == 0.0
        assert DUT.mmt == 0.0
        assert DUT.mcmt == 0.0
        assert DUT.mpmt == 0.0
        assert DUT.mtbf_logistics == 0.0
        assert DUT.mtbf_mission == 0.0
        assert DUT.mttr == 0.0
        assert DUT.name == 'Original Revision'
        assert DUT.reliability_logistics == 0.99986
        assert DUT.reliability_mission == 0.99992
        assert DUT.remarks == 'This is the original revision.'
        assert DUT.revision_code == 'Rev. -'
        assert DUT.program_time == 2562
        assert DUT.program_time_sd == 26.83
        assert DUT.program_cost == 26492.83
        assert DUT.program_cost_sd == 15.62

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of {attr name:attr value}
        pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKRevision)[0]

        _attributes = DUT.get_attributes()

        assert _attributes['availability_logistics'] == 0.9986
        assert _attributes['availability_mission'] == 0.99934
        assert _attributes['cost'] == 12532.15
        assert _attributes['cost_failure'] == 0.0000352
        assert _attributes['cost_hour'] == 1.2532
        assert _attributes['hazard_rate_active'] == 0.0
        assert _attributes['hazard_rate_dormant'] == 0.0
        assert _attributes['hazard_rate_logistics'] == 0.0
        assert _attributes['hazard_rate_mission'] == 0.0
        assert _attributes['hazard_rate_software'] == 0.0
        assert _attributes['mmt'] == 0.0
        assert _attributes['mcmt'] == 0.0
        assert _attributes['mpmt'] == 0.0
        assert _attributes['mtbf_logistics'] == 0.0
        assert _attributes['mtbf_mission'] == 0.0
        assert _attributes['mttr'] == 0.0
        assert _attributes['name'] == 'Original Revision'
        assert _attributes['reliability_logistics'] == 0.99986
        assert _attributes['reliability_mission'] == 0.99992
        assert _attributes['remarks'] == 'This is the original revision.'
        assert _attributes['revision_code'] == 'Rev. -'
        assert _attributes['program_time'] == 2562
        assert _attributes['program_time_sd'] == 26.83
        assert _attributes['program_cost'] == 26492.83
        assert _attributes['program_cost_sd'] == 15.62

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKRevision)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKRevision)[0]

        ATTRIBUTES['mttr'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['mttr'] == 0.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKRevision)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
