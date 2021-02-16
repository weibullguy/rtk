# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.ramstkmode_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKMode module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMode


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mode_1 = RAMSTKMode()
    _mode_1.revision_id = 1
    _mode_1.hardware_id = 1
    _mode_1.mode_id = 1
    _mode_1.effect_local = ''
    _mode_1.mission = 'Default Mission'
    _mode_1.other_indications = ''
    _mode_1.mode_criticality = 0.0
    _mode_1.single_point = 0
    _mode_1.design_provisions = ''
    _mode_1.type_id = 0
    _mode_1.rpn_severity_new = 1
    _mode_1.effect_next = ''
    _mode_1.detection_method = ''
    _mode_1.operator_actions = ''
    _mode_1.critical_item = 0
    _mode_1.hazard_rate_source = ''
    _mode_1.severity_class = ''
    _mode_1.description = 'Test Failure Mode #1'
    _mode_1.mission_phase = ''
    _mode_1.mode_probability = ''
    _mode_1.remarks = ''
    _mode_1.mode_ratio = 0.0
    _mode_1.mode_hazard_rate = 0.0
    _mode_1.rpn_severity = 1
    _mode_1.isolation_method = ''
    _mode_1.effect_end = ''
    _mode_1.mode_op_time = 0.0
    _mode_1.effect_probability = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mode_1,
    ]

    yield DAO


ATTRIBUTES = {
    'effect_local': '',
    'mission': 'Big Mission',
    'other_indications': '',
    'mode_criticality': 0.0,
    'single_point': 0,
    'design_provisions': '',
    'type_id': 0,
    'rpn_severity_new': 1,
    'effect_next': '',
    'detection_method': '',
    'operator_actions': '',
    'critical_item': 0,
    'hazard_rate_source': '',
    'severity_class': '',
    'description': 'Big Failure Mode',
    'mission_phase': '',
    'mode_probability': '',
    'remarks': '',
    'mode_ratio': 0.0,
    'mode_hazard_rate': 0.0,
    'rpn_severity': 1,
    'isolation_method': '',
    'effect_end': '',
    'mode_op_time': 0.0,
    'effect_probability': 0.0
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKMode:
    """Class for testing the RAMSTKMode model."""
    @pytest.mark.unit
    def test_ramstkmode_create(self, mock_program_dao):
        """__init__() should create an RAMSTKMode model."""
        DUT = mock_program_dao.do_select_all(RAMSTKMode)[0]

        assert isinstance(DUT, RAMSTKMode)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mode'
        assert DUT.revision_id == 1
        assert DUT.hardware_id == 1
        assert DUT.mode_id == 1
        assert DUT.critical_item == 0
        assert DUT.description == 'Test Failure Mode #1'
        assert DUT.design_provisions == ''
        assert DUT.detection_method == ''
        assert DUT.effect_end == ''
        assert DUT.effect_local == ''
        assert DUT.effect_next == ''
        assert DUT.effect_probability == 0.0
        assert DUT.hazard_rate_source == ''
        assert DUT.isolation_method == ''
        assert DUT.mission == 'Default Mission'
        assert DUT.mission_phase == ''
        assert DUT.mode_criticality == 0.0
        assert DUT.mode_hazard_rate == 0.0
        assert DUT.mode_op_time == 0.0
        assert DUT.mode_probability == ''
        assert DUT.mode_ratio == 0.0
        assert DUT.operator_actions == ''
        assert DUT.other_indications == ''
        assert DUT.remarks == ''
        assert DUT.rpn_severity == 1
        assert DUT.rpn_severity_new == 1
        assert DUT.severity_class == ''
        assert DUT.single_point == 0
        assert DUT.type_id == 0

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute name:value
        pairs."""
        DUT = mock_program_dao.do_select_all(RAMSTKMode)[0]

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['hardware_id'] == 1
        assert _attributes['mode_id'] == 1
        assert _attributes['critical_item'] == 0
        assert _attributes['description'] == 'Test Failure Mode #1'
        assert _attributes['design_provisions'] == ''
        assert _attributes['detection_method'] == ''
        assert _attributes['effect_end'] == ''
        assert _attributes['effect_local'] == ''
        assert _attributes['effect_next'] == ''
        assert _attributes['effect_probability'] == 0.0
        assert _attributes['hazard_rate_source'] == ''
        assert _attributes['isolation_method'] == ''
        assert _attributes['mission'] == 'Default Mission'
        assert _attributes['mission_phase'] == ''
        assert _attributes['mode_criticality'] == 0.0
        assert _attributes['mode_hazard_rate'] == 0.0
        assert _attributes['mode_op_time'] == 0.0
        assert _attributes['mode_probability'] == ''
        assert _attributes['mode_ratio'] == 0.0
        assert _attributes['operator_actions'] == ''
        assert _attributes['other_indications'] == ''
        assert _attributes['remarks'] == ''
        assert _attributes['rpn_severity'] == 1
        assert _attributes['rpn_severity_new'] == 1
        assert _attributes['severity_class'] == ''
        assert _attributes['single_point'] == 0
        assert _attributes['type_id'] == 0

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKMode)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.mission == 'Big Mission'
        assert DUT.description == 'Big Failure Mode'

    @pytest.mark.unit
    def test_set_attributes_set_default(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKMode)[0]

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKMode)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
