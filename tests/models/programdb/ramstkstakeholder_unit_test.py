# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkstakeholder_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKStakeholder module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKStakeholder


@pytest.fixture
def mock_program_dao(monkeypatch):
    _stakeholder_1 = RAMSTKStakeholder()
    _stakeholder_1.revision_id = 1
    _stakeholder_1.requirement_id = 1
    _stakeholder_1.stakeholder_id = 1
    _stakeholder_1.customer_rank = 1
    _stakeholder_1.description = 'Test Stakeholder Input'
    _stakeholder_1.group = ''
    _stakeholder_1.improvement = 0.0
    _stakeholder_1.overall_weight = 0.0
    _stakeholder_1.planned_rank = 1
    _stakeholder_1.priority = 1
    _stakeholder_1.stakeholder = ''
    _stakeholder_1.user_float_1 = 1.0
    _stakeholder_1.user_float_2 = 1.0
    _stakeholder_1.user_float_3 = 1.0
    _stakeholder_1.user_float_4 = 1.0
    _stakeholder_1.user_float_5 = 1.0

    DAO = MockDAO()
    DAO.table = [
        _stakeholder_1,
    ]

    yield DAO


ATTRIBUTES = {
    'customer_rank': 1,
    'description': 'Test Stakeholder Input',
    'group': '',
    'improvement': 0.0,
    'overall_weight': 0.0,
    'planned_rank': 1,
    'priority': 1,
    'requirement_id': 0,
    'stakeholder': '',
    'user_float_1': 1.0,
    'user_float_2': 1.0,
    'user_float_3': 1.0,
    'user_float_4': 1.0,
    'user_float_5': 1.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKStakeholder():
    """Class for testing the RAMSTKStakeholder model."""
    @pytest.mark.unit
    def test_ramstkstakeholder_create(self, mock_program_dao):
        """__init__() should create an RAMSTKStakeholder model."""
        DUT = mock_program_dao.do_select_all(RAMSTKStakeholder)[0]

        assert isinstance(DUT, RAMSTKStakeholder)
        assert DUT.__tablename__ == 'ramstk_stakeholder'
        assert DUT.revision_id == 1
        assert DUT.stakeholder_id == 1
        assert DUT.customer_rank == 1
        assert DUT.description == 'Test Stakeholder Input'
        assert DUT.group == ''
        assert DUT.improvement == 0.0
        assert DUT.overall_weight == 0.0
        assert DUT.planned_rank == 1
        assert DUT.priority == 1
        assert DUT.requirement_id == 1
        assert DUT.stakeholder == ''
        assert DUT.user_float_1 == 1.0
        assert DUT.user_float_2 == 1.0
        assert DUT.user_float_3 == 1.0
        assert DUT.user_float_4 == 1.0
        assert DUT.user_float_5 == 1.0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKStakeholder)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['stakeholder_id'] == 1
        assert _attributes['customer_rank'] == 1
        assert _attributes['description'] == 'Test Stakeholder Input'
        assert _attributes['group'] == ''
        assert _attributes['improvement'] == 0.0
        assert _attributes['overall_weight'] == 0.0
        assert _attributes['planned_rank'] == 1
        assert _attributes['priority'] == 1
        assert _attributes['requirement_id'] == 1
        assert _attributes['stakeholder'] == ''
        assert _attributes['user_float_1'] == 1.0
        assert _attributes['user_float_2'] == 1.0
        assert _attributes['user_float_3'] == 1.0
        assert _attributes['user_float_4'] == 1.0
        assert _attributes['user_float_5'] == 1.0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKStakeholder)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKStakeholder)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Stakeholder Input'

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKStakeholder)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
