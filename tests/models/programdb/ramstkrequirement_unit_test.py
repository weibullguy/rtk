# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkrequirement_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing RAMSTKRequirement module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKRequirement


@pytest.fixture
def mock_program_dao(monkeypatch):
    _requirement_1 = RAMSTKRequirement()
    _requirement_1.revision_id = 1
    _requirement_1.requirement_id = 1
    _requirement_1.derived = 0
    _requirement_1.description = ''
    _requirement_1.figure_number = ''
    _requirement_1.owner = 0
    _requirement_1.page_number = ''
    _requirement_1.parent_id = 0
    _requirement_1.priority = 0
    _requirement_1.q_clarity_0 = 0
    _requirement_1.q_clarity_1 = 0
    _requirement_1.q_clarity_2 = 0
    _requirement_1.q_clarity_3 = 0
    _requirement_1.q_clarity_4 = 0
    _requirement_1.q_clarity_5 = 0
    _requirement_1.q_clarity_6 = 0
    _requirement_1.q_clarity_7 = 0
    _requirement_1.q_clarity_8 = 0
    _requirement_1.q_complete_0 = 0
    _requirement_1.q_complete_1 = 0
    _requirement_1.q_complete_2 = 0
    _requirement_1.q_complete_3 = 0
    _requirement_1.q_complete_4 = 0
    _requirement_1.q_complete_5 = 0
    _requirement_1.q_complete_6 = 0
    _requirement_1.q_complete_7 = 0
    _requirement_1.q_complete_8 = 0
    _requirement_1.q_complete_9 = 0
    _requirement_1.q_consistent_0 = 0
    _requirement_1.q_consistent_1 = 0
    _requirement_1.q_consistent_2 = 0
    _requirement_1.q_consistent_3 = 0
    _requirement_1.q_consistent_4 = 0
    _requirement_1.q_consistent_5 = 0
    _requirement_1.q_consistent_6 = 0
    _requirement_1.q_consistent_7 = 0
    _requirement_1.q_consistent_8 = 0
    _requirement_1.q_verifiable_0 = 0
    _requirement_1.q_verifiable_1 = 0
    _requirement_1.q_verifiable_2 = 0
    _requirement_1.q_verifiable_3 = 0
    _requirement_1.q_verifiable_4 = 0
    _requirement_1.q_verifiable_5 = 0
    _requirement_1.requirement_code = 'REL-0001'
    _requirement_1.requirement_type = 0
    _requirement_1.specification = ''
    _requirement_1.validated = 0
    _requirement_1.validated_date = date.today()

    DAO = MockDAO()
    DAO.table = [
        _requirement_1,
    ]

    yield DAO


ATTRIBUTES = {
    'derived': 0,
    'description': '',
    'figure_number': '',
    'owner': 0,
    'page_number': '',
    'parent_id': 0,
    'priority': 0,
    'q_clarity_0': 0,
    'q_clarity_1': 0,
    'q_clarity_2': 0,
    'q_clarity_3': 0,
    'q_clarity_4': 0,
    'q_clarity_5': 0,
    'q_clarity_6': 0,
    'q_clarity_7': 0,
    'q_clarity_8': 0,
    'q_complete_0': 0,
    'q_complete_1': 0,
    'q_complete_2': 0,
    'q_complete_3': 0,
    'q_complete_4': 0,
    'q_complete_5': 0,
    'q_complete_6': 0,
    'q_complete_7': 0,
    'q_complete_8': 0,
    'q_complete_9': 0,
    'q_consistent_0': 0,
    'q_consistent_1': 0,
    'q_consistent_2': 0,
    'q_consistent_3': 0,
    'q_consistent_4': 0,
    'q_consistent_5': 0,
    'q_consistent_6': 0,
    'q_consistent_7': 0,
    'q_consistent_8': 0,
    'q_verifiable_0': 0,
    'q_verifiable_1': 0,
    'q_verifiable_2': 0,
    'q_verifiable_3': 0,
    'q_verifiable_4': 0,
    'q_verifiable_5': 0,
    'requirement_code': 'REL-0001',
    'requirement_type': 0,
    'specification': '',
    'validated': 0,
    'validated_date': date.today()
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKRequirement:
    """Class for testing the RAMSTKRequirement model."""
    @pytest.mark.unit
    def test_ramstkrequirement_create(self, mock_program_dao):
        """__init__() should create an RAMSTKRequirement model."""
        DUT = mock_program_dao.do_select_all(RAMSTKRequirement)[0]

        assert isinstance(DUT, RAMSTKRequirement)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_requirement'
        assert DUT.revision_id == 1
        assert DUT.requirement_id == 1
        assert DUT.derived == 0
        assert DUT.description == ''
        assert DUT.figure_number == ''
        assert DUT.owner == 0
        assert DUT.page_number == ''
        assert DUT.parent_id == 0
        assert DUT.priority == 0
        assert DUT.requirement_code == 'REL-0001'
        assert DUT.specification == ''
        assert DUT.requirement_type == 0
        assert DUT.validated == 0
        assert DUT.validated_date == date.today()
        assert DUT.q_clarity_0 == 0
        assert DUT.q_clarity_1 == 0
        assert DUT.q_clarity_2 == 0
        assert DUT.q_clarity_3 == 0
        assert DUT.q_clarity_4 == 0
        assert DUT.q_clarity_5 == 0
        assert DUT.q_clarity_6 == 0
        assert DUT.q_clarity_7 == 0
        assert DUT.q_clarity_8 == 0
        assert DUT.q_complete_0 == 0
        assert DUT.q_complete_1 == 0
        assert DUT.q_complete_2 == 0
        assert DUT.q_complete_3 == 0
        assert DUT.q_complete_4 == 0
        assert DUT.q_complete_5 == 0
        assert DUT.q_complete_6 == 0
        assert DUT.q_complete_7 == 0
        assert DUT.q_complete_8 == 0
        assert DUT.q_complete_9 == 0
        assert DUT.q_consistent_0 == 0
        assert DUT.q_consistent_1 == 0
        assert DUT.q_consistent_2 == 0
        assert DUT.q_consistent_3 == 0
        assert DUT.q_consistent_4 == 0
        assert DUT.q_consistent_5 == 0
        assert DUT.q_consistent_6 == 0
        assert DUT.q_consistent_7 == 0
        assert DUT.q_consistent_8 == 0
        assert DUT.q_verifiable_0 == 0
        assert DUT.q_verifiable_1 == 0
        assert DUT.q_verifiable_2 == 0
        assert DUT.q_verifiable_3 == 0
        assert DUT.q_verifiable_4 == 0
        assert DUT.q_verifiable_5 == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKRequirement)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['requirement_id'] == 1
        assert _attributes['derived'] == 0
        assert _attributes['description'] == ''
        assert _attributes['figure_number'] == ''
        assert _attributes['owner'] == 0
        assert _attributes['page_number'] == ''
        assert _attributes['parent_id'] == 0
        assert _attributes['priority'] == 0
        assert _attributes['requirement_code'] == 'REL-0001'
        assert _attributes['specification'] == ''
        assert _attributes['requirement_type'] == 0
        assert _attributes['validated'] == 0
        assert _attributes['validated_date'] == date.today()
        assert _attributes['q_clarity_0'] == 0
        assert _attributes['q_clarity_1'] == 0
        assert _attributes['q_clarity_2'] == 0
        assert _attributes['q_clarity_3'] == 0
        assert _attributes['q_clarity_4'] == 0
        assert _attributes['q_clarity_5'] == 0
        assert _attributes['q_clarity_6'] == 0
        assert _attributes['q_clarity_7'] == 0
        assert _attributes['q_clarity_8'] == 0
        assert _attributes['q_complete_0'] == 0
        assert _attributes['q_complete_1'] == 0
        assert _attributes['q_complete_2'] == 0
        assert _attributes['q_complete_3'] == 0
        assert _attributes['q_complete_4'] == 0
        assert _attributes['q_complete_5'] == 0
        assert _attributes['q_complete_6'] == 0
        assert _attributes['q_complete_7'] == 0
        assert _attributes['q_complete_8'] == 0
        assert _attributes['q_complete_9'] == 0
        assert _attributes['q_consistent_0'] == 0
        assert _attributes['q_consistent_1'] == 0
        assert _attributes['q_consistent_2'] == 0
        assert _attributes['q_consistent_3'] == 0
        assert _attributes['q_consistent_4'] == 0
        assert _attributes['q_consistent_5'] == 0
        assert _attributes['q_consistent_6'] == 0
        assert _attributes['q_consistent_7'] == 0
        assert _attributes['q_consistent_8'] == 0
        assert _attributes['q_verifiable_0'] == 0
        assert _attributes['q_verifiable_1'] == 0
        assert _attributes['q_verifiable_2'] == 0
        assert _attributes['q_verifiable_3'] == 0
        assert _attributes['q_verifiable_4'] == 0
        assert _attributes['q_verifiable_5'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKRequirement)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKRequirement)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKRequirement)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})

    @pytest.mark.unit
    def test_create_code(self, mock_program_dao):
        """create_code() should return False on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKRequirement)[0]

        assert not DUT.create_code('PERF')
        assert DUT.requirement_code == 'PERF-0001'
