# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkallocation_unit_test.py is part of The
#       RAMSTK
#       Project
#
# All rights reserved.
"""Class for testing RAMSTKAllocation module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKAllocation


@pytest.fixture
def mock_program_dao(monkeypatch):
    _allocation_1 = RAMSTKAllocation()
    _allocation_1.revision_id = 1
    _allocation_1.hardware_id = 1
    _allocation_1.availability_alloc = 0.9998
    _allocation_1.duty_cycle = 100.0
    _allocation_1.env_factor = 6
    _allocation_1.goal_measure_id = 1
    _allocation_1.hazard_rate_alloc = 0.0
    _allocation_1.hazard_rate_goal = 0.0
    _allocation_1.included = 1
    _allocation_1.int_factor = 3
    _allocation_1.allocation_method_id = 1
    _allocation_1.mission_time = 100.0
    _allocation_1.mtbf_alloc = 0.0
    _allocation_1.mtbf_goal = 0.0
    _allocation_1.n_sub_systems = 3
    _allocation_1.n_sub_elements = 3
    _allocation_1.parent_id = 1
    _allocation_1.percent_weight_factor = 0.8
    _allocation_1.reliability_alloc = 0.99975
    _allocation_1.reliability_goal = 0.999
    _allocation_1.op_time_factor = 5
    _allocation_1.soa_factor = 2
    _allocation_1.weight_factor = 1

    DAO = MockDAO()
    DAO.table = [
        _allocation_1,
    ]

    yield DAO


ATTRIBUTES = {
    'availability_alloc': 0.9998,
    'duty_cycle': 100.0,
    'env_factor': 6,
    'goal_measure_id': 1,
    'hazard_rate_alloc': 0.0,
    'hazard_rate_goal': 0.0,
    'included': 1,
    'int_factor': 3,
    'allocation_method_id': 1,
    'mission_time': 100.0,
    'mtbf_alloc': 0.0,
    'mtbf_goal': 0.0,
    'n_sub_systems': 3,
    'n_sub_elements': 3,
    'parent_id': 1,
    'percent_weight_factor': 0.8,
    'reliability_alloc': 0.99975,
    'reliability_goal': 0.999,
    'op_time_factor': 5,
    'soa_factor': 2,
    'weight_factor': 1
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKAllocation():
    """Class for testing the RAMSTKAllocation model."""
    @pytest.mark.unit
    def test_ramstkallocation_create(self, mock_program_dao):
        """__init__() should create an RAMSTKAllocation model."""
        DUT = mock_program_dao.do_select_all(RAMSTKAllocation)[0]

        assert isinstance(DUT, RAMSTKAllocation)
        assert DUT.__tablename__ == 'ramstk_allocation'
        assert DUT.revision_id == 1
        assert DUT.hardware_id == 1
        assert DUT.availability_alloc == 0.9998
        assert DUT.duty_cycle == 100.0
        assert DUT.env_factor == 6
        assert DUT.goal_measure_id == 1
        assert DUT.hazard_rate_alloc == 0.0
        assert DUT.hazard_rate_goal == 0.0
        assert DUT.included == 1
        assert DUT.int_factor == 3
        assert DUT.allocation_method_id == 1
        assert DUT.mission_time == 100.0
        assert DUT.mtbf_alloc == 0.0
        assert DUT.mtbf_goal == 0.0
        assert DUT.n_sub_systems == 3
        assert DUT.n_sub_elements == 3
        assert DUT.parent_id == 1
        assert DUT.percent_weight_factor == 0.8
        assert DUT.reliability_alloc == 0.99975
        assert DUT.reliability_goal == 0.999
        assert DUT.op_time_factor == 5
        assert DUT.soa_factor == 2
        assert DUT.weight_factor == 1

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKAllocation)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['hardware_id'] == 1
        assert _attributes['availability_alloc'] == 0.9998
        assert _attributes['duty_cycle'] == 100.0
        assert _attributes['env_factor'] == 6
        assert _attributes['goal_measure_id'] == 1
        assert _attributes['hazard_rate_alloc'] == 0.0
        assert _attributes['hazard_rate_goal'] == 0.0
        assert _attributes['included'] == 1
        assert _attributes['int_factor'] == 3
        assert _attributes['allocation_method_id'] == 1
        assert _attributes['mission_time'] == 100.0
        assert _attributes['mtbf_alloc'] == 0.0
        assert _attributes['mtbf_goal'] == 0.0
        assert _attributes['n_sub_systems'] == 3
        assert _attributes['n_sub_elements'] == 3
        assert _attributes['parent_id'] == 1
        assert _attributes['percent_weight_factor'] == 0.8
        assert _attributes['reliability_alloc'] == 0.99975
        assert _attributes['reliability_goal'] == 0.999
        assert _attributes['op_time_factor'] == 5
        assert _attributes['soa_factor'] == 2
        assert _attributes['weight_factor'] == 1

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return None on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKAllocation)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKAllocation)[0]

        ATTRIBUTES['reliability_alloc'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['reliability_alloc'] == 1.0

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKAllocation)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
