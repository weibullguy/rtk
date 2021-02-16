# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkcause_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKCause module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKCause


@pytest.fixture
def mock_program_dao(monkeypatch):
    _cause_1 = RAMSTKCause()
    _cause_1.revision_id = 1
    _cause_1.mode_id = 5
    _cause_1.mechanism_id = 1
    _cause_1.cause_id = 1
    _cause_1.rpn_detection = 4
    _cause_1.rpn_detection_new = 3
    _cause_1.description = 'Test Failure Cause #1'
    _cause_1.rpn_occurrence = 4
    _cause_1.rpn_occurrence_new = 3
    _cause_1.rpn = 0
    _cause_1.rpn_new = 0

    _cause_2 = RAMSTKCause()
    _cause_2.revision_id = 1
    _cause_1.mode_id = 5
    _cause_1.mechanism_id = 1
    _cause_2.cause_id = 2
    _cause_2.rpn_new = 0
    _cause_2.rpn_occurrence_new = 10
    _cause_2.description = 'Test Failure Cause #2'
    _cause_2.rpn_occurrence = 10
    _cause_2.rpn_detection_new = 10
    _cause_2.rpn_detection = 10
    _cause_2.rpn = 0

    _cause_3 = RAMSTKCause()
    _cause_3.revision_id = 1
    _cause_1.mode_id = 5
    _cause_1.mechanism_id = 1
    _cause_3.cause_id = 3
    _cause_3.rpn_new = 0
    _cause_3.rpn_occurrence_new = 10
    _cause_3.description = 'Test Failure Cause #3'
    _cause_3.rpn_occurrence = 10
    _cause_3.rpn_detection_new = 10
    _cause_3.rpn_detection = 10
    _cause_3.rpn = 0

    DAO = MockDAO()
    DAO.table = [
        _cause_1,
        _cause_2,
        _cause_3,
    ]

    yield DAO


ATTRIBUTES = {
    'rpn_new': 0,
    'rpn_occurrence_new': 10,
    'description': 'Test Failure Cause #1',
    'rpn_occurrence': 10,
    'rpn_detection_new': 10,
    'rpn_detection': 10,
    'rpn': 0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKCause:
    """Class for testing the RAMSTKCause model."""
    @pytest.mark.unit
    def test_ramstkcause_create(self, mock_program_dao):
        """__init__() should create an RAMSTKCause model."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        assert isinstance(DUT, RAMSTKCause)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_cause'
        assert DUT.mode_id == 5
        assert DUT.mechanism_id == 1
        assert DUT.cause_id == 1
        assert DUT.description == 'Test Failure Cause #1'
        assert DUT.rpn == 0
        assert DUT.rpn_detection == 4
        assert DUT.rpn_detection_new == 3
        assert DUT.rpn_new == 0
        assert DUT.rpn_occurrence == 4
        assert DUT.rpn_occurrence_new == 3

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a tuple of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['mode_id'] == 5
        assert _attributes['mechanism_id'] == 1
        assert _attributes['cause_id'] == 1
        assert _attributes['description'] == ('Test Failure Cause #1')
        assert _attributes['rpn'] == 0
        assert _attributes['rpn_detection'] == 4
        assert _attributes['rpn_detection_new'] == 3
        assert _attributes['rpn_new'] == 0
        assert _attributes['rpn_occurrence'] == 4
        assert _attributes['rpn_occurrence_new'] == 3

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKCause)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
