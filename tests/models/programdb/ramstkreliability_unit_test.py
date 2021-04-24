# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkreliability_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKReliability module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKReliability


@pytest.fixture
def mock_program_dao(monkeypatch):
    _reliability_1 = RAMSTKReliability()
    _reliability_1.revision_id = 1
    _reliability_1.hardware_id = 1
    _reliability_1.add_adj_factor = 0.0
    _reliability_1.availability_logistics = 1.0
    _reliability_1.availability_mission = 1.0
    _reliability_1.avail_log_variance = 0.0
    _reliability_1.avail_mis_variance = 0.0
    _reliability_1.failure_distribution_id = 0
    _reliability_1.hazard_rate_active = 0.0
    _reliability_1.hazard_rate_dormant = 0.0
    _reliability_1.hazard_rate_logistics = 0.0
    _reliability_1.hazard_rate_method_id = 0
    _reliability_1.hazard_rate_mission = 0.0
    _reliability_1.hazard_rate_model = ''
    _reliability_1.hazard_rate_percent = 0.0
    _reliability_1.hazard_rate_software = 0.0
    _reliability_1.hazard_rate_specified = 0.0
    _reliability_1.hazard_rate_type_id = 0
    _reliability_1.hr_active_variance = 0.0
    _reliability_1.hr_logistics_variance = 0.0
    _reliability_1.hr_dormant_variance = 0.0
    _reliability_1.hr_mission_variance = 0.0
    _reliability_1.hr_specified_variance = 0.0
    _reliability_1.lambda_b = 0.0
    _reliability_1.location_parameter = 0.0
    _reliability_1.mtbf_logistics = 0.0
    _reliability_1.mtbf_mission = 0.0
    _reliability_1.mtbf_specified = 0.0
    _reliability_1.mtbf_logistics_variance = 0.0
    _reliability_1.mtbf_mission_variance = 0.0
    _reliability_1.mtbf_specified_variance = 0.0
    _reliability_1.mult_adj_factor = 1.0
    _reliability_1.quality_id = 0
    _reliability_1.reliability_mission = 1.0
    _reliability_1.reliability_goal_measure_id = 0
    _reliability_1.reliability_goal = 0.0
    _reliability_1.reliability_logistics = 1.0
    _reliability_1.reliability_log_variance = 0.0
    _reliability_1.reliability_miss_variance = 0.0
    _reliability_1.scale_parameter = 0.0
    _reliability_1.shape_parameter = 0.0
    _reliability_1.survival_analysis_id = 0

    DAO = MockDAO()
    DAO.table = [
        _reliability_1,
    ]

    yield DAO


ATTRIBUTES = {
    'add_adj_factor': 0.0,
    'availability_logistics': 1.0,
    'availability_mission': 1.0,
    'avail_log_variance': 0.0,
    'avail_mis_variance': 0.0,
    'failure_distribution_id': 0,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_method_id': 0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_model': '',
    'hazard_rate_percent': 0.0,
    'hazard_rate_software': 0.0,
    'hazard_rate_specified': 0.0,
    'hazard_rate_type_id': 0,
    'hr_active_variance': 0.0,
    'hr_logistics_variance': 0.0,
    'hr_dormant_variance': 0.0,
    'hr_mission_variance': 0.0,
    'hr_specified_variance': 0.0,
    'lambda_b': 0.0,
    'location_parameter': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mtbf_specified': 0.0,
    'mtbf_logistics_variance': 0.0,
    'mtbf_mission_variance': 0.0,
    'mtbf_specified_variance': 0.0,
    'mult_adj_factor': 1.0,
    'quality_id': 0,
    'reliability_mission': 1.0,
    'reliability_goal_measure_id': 0,
    'reliability_goal': 0.0,
    'reliability_logistics': 1.0,
    'reliability_log_variance': 0.0,
    'reliability_miss_variance': 0.0,
    'scale_parameter': 0.0,
    'shape_parameter': 0.0,
    'survival_analysis_id': 0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKReliability:
    """Class for testing the RAMSTKReliability model."""
    @pytest.mark.unit
    def test_ramstkreliability_create(self, mock_program_dao):
        """__init__() should create an RAMSTKReliability model."""
        DUT = mock_program_dao.do_select_all(RAMSTKReliability)[0]

        assert isinstance(DUT, RAMSTKReliability)
        assert DUT.__tablename__ == 'ramstk_reliability'
        assert DUT.hardware_id == 1
        assert DUT.add_adj_factor == 0.0
        assert DUT.availability_logistics == 1.0
        assert DUT.availability_mission == 1.0
        assert DUT.avail_log_variance == 0.0
        assert DUT.avail_mis_variance == 0.0
        assert DUT.failure_distribution_id == 0
        assert DUT.hazard_rate_active == 0.0
        assert DUT.hazard_rate_dormant == 0.0
        assert DUT.hazard_rate_logistics == 0.0
        assert DUT.hazard_rate_method_id == 0
        assert DUT.hazard_rate_mission == 0.0
        assert DUT.hazard_rate_model == ''
        assert DUT.hazard_rate_percent == 0.0
        assert DUT.hazard_rate_software == 0.0
        assert DUT.hazard_rate_specified == 0.0
        assert DUT.hazard_rate_type_id == 0
        assert DUT.hr_active_variance == 0.0
        assert DUT.hr_dormant_variance == 0.0
        assert DUT.hr_logistics_variance == 0.0
        assert DUT.hr_mission_variance == 0.0
        assert DUT.hr_specified_variance == 0.0
        assert DUT.location_parameter == 0.0
        assert DUT.mtbf_logistics == 0.0
        assert DUT.mtbf_mission == 0.0
        assert DUT.mtbf_specified == 0.0
        assert DUT.mtbf_logistics_variance == 0.0
        assert DUT.mtbf_mission_variance == 0.0
        assert DUT.mtbf_specified_variance == 0.0
        assert DUT.mult_adj_factor == 1.0
        assert DUT.quality_id == 0
        assert DUT.reliability_goal == 0.0
        assert DUT.reliability_goal_measure_id == 0
        assert DUT.reliability_logistics == 1.0
        assert DUT.reliability_mission == 1.0
        assert DUT.reliability_log_variance == 0.0
        assert DUT.reliability_miss_variance == 0.0
        assert DUT.scale_parameter == 0.0
        assert DUT.shape_parameter == 0.0
        assert DUT.survival_analysis_id == 0
        assert DUT.lambda_b == 0.0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute key:value
        pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKReliability)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['hardware_id'] == 1
        assert _attributes['add_adj_factor'] == 0.0
        assert _attributes['availability_logistics'] == 1.0
        assert _attributes['availability_mission'] == 1.0
        assert _attributes['avail_log_variance'] == 0.0
        assert _attributes['avail_mis_variance'] == 0.0
        assert _attributes['failure_distribution_id'] == 0
        assert _attributes['hazard_rate_active'] == 0.0
        assert _attributes['hazard_rate_dormant'] == 0.0
        assert _attributes['hazard_rate_logistics'] == 0.0
        assert _attributes['hazard_rate_method_id'] == 0
        assert _attributes['hazard_rate_mission'] == 0.0
        assert _attributes['hazard_rate_model'] == ''
        assert _attributes['hazard_rate_percent'] == 0.0
        assert _attributes['hazard_rate_software'] == 0.0
        assert _attributes['hazard_rate_specified'] == 0.0
        assert _attributes['hazard_rate_type_id'] == 0
        assert _attributes['hr_active_variance'] == 0.0
        assert _attributes['hr_dormant_variance'] == 0.0
        assert _attributes['hr_logistics_variance'] == 0.0
        assert _attributes['hr_mission_variance'] == 0.0
        assert _attributes['hr_specified_variance'] == 0.0
        assert _attributes['lambda_b'] == 0.0
        assert _attributes['location_parameter'] == 0.0
        assert _attributes['mtbf_logistics'] == 0.0
        assert _attributes['mtbf_mission'] == 0.0
        assert _attributes['mtbf_specified'] == 0.0
        assert _attributes['mtbf_logistics_variance'] == 0.0
        assert _attributes['mtbf_mission_variance'] == 0.0
        assert _attributes['mtbf_specified_variance'] == 0.0
        assert _attributes['mult_adj_factor'] == 1.0
        assert _attributes['quality_id'] == 0
        assert _attributes['reliability_goal'] == 0.0
        assert _attributes['reliability_goal_measure_id'] == 0
        assert _attributes['reliability_logistics'] == 1.0
        assert _attributes['reliability_mission'] == 1.0
        assert _attributes['reliability_log_variance'] == 0.0
        assert _attributes['reliability_miss_variance'] == 0.0
        assert _attributes['scale_parameter'] == 0.0
        assert _attributes['shape_parameter'] == 0.0
        assert _attributes['survival_analysis_id'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKReliability)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKReliability)[0]

        ATTRIBUTES['add_adj_factor'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['add_adj_factor'] == 0.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKReliability)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
