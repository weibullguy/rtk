# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkmechanism_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKMechanism module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMechanism


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mechanism_1 = RAMSTKMechanism()
    _mechanism_1.revision_id = 1
    _mechanism_1.mode_id = 6
    _mechanism_1.mechanism_id = 2
    _mechanism_1.description = 'Test Failure Mechanism #1'
    _mechanism_1.rpn = 100
    _mechanism_1.rpn_new = 100
    _mechanism_1.rpn_detection = 10
    _mechanism_1.rpn_detection_new = 10
    _mechanism_1.rpn_occurrence_new = 10
    _mechanism_1.rpn_occurrence = 10
    _mechanism_1.pof_include = 1

    _mechanism_2 = RAMSTKMechanism()
    _mechanism_2.revision_id = 1
    _mechanism_2.mode_id = 1
    _mechanism_2.mechanism_id = 3
    _mechanism_2.description = 'Test Failure Mechanism #2'
    _mechanism_2.rpn = 100
    _mechanism_2.rpn_new = 100
    _mechanism_2.rpn_detection = 10
    _mechanism_2.rpn_detection_new = 10
    _mechanism_2.rpn_occurrence_new = 10
    _mechanism_2.rpn_occurrence = 10
    _mechanism_2.pof_include = 1

    DAO = MockDAO()
    DAO.table = [
        _mechanism_1,
        _mechanism_2,
    ]

    yield DAO


ATTRIBUTES = {
    'rpn_new': 0,
    'rpn_occurrence_new': 2,
    'rpn_occurrence': 5,
    'description': 'Big Failure Mechanism',
    'rpn_detection_new': 3,
    'rpn_detection': 4,
    'rpn': 0,
    'pof_include': 0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKMechanism():
    """Class for testing the RAMSTKMechanism model."""
    @pytest.mark.unit
    def test_ramstkmechanism_create(self, mock_program_dao):
        """__init__() should create an RAMSTKMechanism model."""
        DUT = mock_program_dao.do_select_all(RAMSTKMechanism)[0]

        assert isinstance(DUT, RAMSTKMechanism)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mechanism'
        assert DUT.mode_id == 6
        assert DUT.mechanism_id == 2
        assert DUT.description == 'Test Failure Mechanism #1'
        assert DUT.pof_include == 1
        assert DUT.rpn == 100
        assert DUT.rpn_detection == 10
        assert DUT.rpn_detection_new == 10
        assert DUT.rpn_new == 100
        assert DUT.rpn_occurrence == 10
        assert DUT.rpn_occurrence_new == 10

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute:value pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKMechanism)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['mode_id'] == 6
        assert _attributes['mechanism_id'] == 2
        assert _attributes['description'] == 'Test Failure Mechanism #1'
        assert _attributes['pof_include'] == 1
        assert _attributes['rpn'] == 100
        assert _attributes['rpn_detection'] == 10
        assert _attributes['rpn_detection_new'] == 10
        assert _attributes['rpn_new'] == 100
        assert _attributes['rpn_occurrence'] == 10
        assert _attributes['rpn_occurrence_new'] == 10

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKMechanism)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.rpn_new == 0
        assert DUT.rpn_occurrence_new == 2
        assert DUT.rpn_occurrence == 5
        assert DUT.description == 'Big Failure Mechanism'
        assert DUT.rpn_detection_new == 3
        assert DUT.rpn_detection == 4
        assert DUT.rpn == 0
        assert DUT.pof_include == 0

    @pytest.mark.unit
    def test_set_attributes_set_default(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKMechanism)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKMechanism)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
