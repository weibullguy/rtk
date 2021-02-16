# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.dao.programmdb.ramstkhardware_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing the RAMSTKHardware module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKHardware


@pytest.fixture
def mock_program_dao(monkeypatch):
    _hardware_1 = RAMSTKHardware()
    _hardware_1.revision_id = 1
    _hardware_1.hardware_id = 1
    _hardware_1.alt_part_number = ''
    _hardware_1.attachments = ''
    _hardware_1.cage_code = ''
    _hardware_1.category_id = 0
    _hardware_1.comp_ref_des = 'S1'
    _hardware_1.cost = 0.0
    _hardware_1.cost_failure = 0.0
    _hardware_1.cost_hour = 0.0
    _hardware_1.cost_type_id = 0
    _hardware_1.description = 'Test System'
    _hardware_1.duty_cycle = 100.0
    _hardware_1.figure_number = ''
    _hardware_1.lcn = ''
    _hardware_1.level = 0
    _hardware_1.manufacturer_id = 0
    _hardware_1.mission_time = 100.0
    _hardware_1.name = ''
    _hardware_1.nsn = ''
    _hardware_1.page_number = ''
    _hardware_1.parent_id = 0
    _hardware_1.part = 0
    _hardware_1.part_number = ''
    _hardware_1.quantity = 1
    _hardware_1.ref_des = 'S1'
    _hardware_1.remarks = ''
    _hardware_1.repairable = 0
    _hardware_1.specification_number = ''
    _hardware_1.subcategory_id = 0
    _hardware_1.tagged_part = 0
    _hardware_1.total_cost = 0.0
    _hardware_1.total_part_count = 0
    _hardware_1.total_power_dissipation = 0
    _hardware_1.year_of_manufacture = date.today().year

    DAO = MockDAO()
    DAO.table = [
        _hardware_1,
    ]

    yield DAO


ATTRIBUTES = {
    'alt_part_number': '',
    'attachments': '',
    'cage_code': '',
    'category_id': 0,
    'comp_ref_des': 'S1',
    'cost': 0.0,
    'cost_failure': 0.0,
    'cost_hour': 0.0,
    'cost_type_id': 0,
    'description': 'Test System',
    'duty_cycle': 100.0,
    'figure_number': '',
    'lcn': '',
    'level': 0,
    'manufacturer_id': 0,
    'mission_time': 100.0,
    'name': '',
    'nsn': '',
    'page_number': '',
    'parent_id': 0,
    'part': 0,
    'part_number': '',
    'quantity': 1,
    'ref_des': 'S1',
    'remarks': '',
    'repairable': 0,
    'specification_number': '',
    'subcategory_id': 0,
    'tagged_part': 0,
    'total_cost': 0.0,
    'total_part_count': 0,
    'total_power_dissipation': 0,
    'year_of_manufacture': date.today().year
}


@pytest.mark.usefixtures('mock_program_dao')
class TestRAMSTKHardware:
    """Class for testing the RAMSTKHardware model."""
    @pytest.mark.unit
    def test_ramstkhardware_create(self, mock_program_dao):
        """__init__() should create an RAMSTKHardware model."""
        DUT = mock_program_dao.do_select_all(RAMSTKHardware)[0]

        assert isinstance(DUT, RAMSTKHardware)
        assert DUT.__tablename__ == 'ramstk_hardware'
        assert DUT.revision_id == 1
        assert DUT.hardware_id == 1
        assert DUT.alt_part_number == ''
        assert DUT.attachments == ''
        assert DUT.cage_code == ''
        assert DUT.comp_ref_des == 'S1'
        assert DUT.category_id == 0
        assert DUT.cost == 0.0
        assert DUT.cost_failure == 0.0
        assert DUT.cost_hour == 0.0
        assert DUT.cost_type_id == 0
        assert DUT.description == 'Test System'
        assert DUT.duty_cycle == 100.0
        assert DUT.figure_number == ''
        assert DUT.lcn == ''
        assert DUT.level == 0
        assert DUT.manufacturer_id == 0
        assert DUT.mission_time == 100.0
        assert DUT.name == ''
        assert DUT.nsn == ''
        assert DUT.page_number == ''
        assert DUT.parent_id == 0
        assert DUT.part == 0
        assert DUT.part_number == ''
        assert DUT.quantity == 1
        assert DUT.ref_des == 'S1'
        assert DUT.remarks == ''
        assert DUT.repairable == 0
        assert DUT.specification_number == ''
        assert DUT.subcategory_id == 0
        assert DUT.tagged_part == 0
        assert DUT, total_cost == 0
        assert DUT.total_part_count == 0
        assert DUT.total_power_dissipation == 0.0
        assert DUT.year_of_manufacture == date.today().year

    @pytest.mark.unit
    def test_get_attributes(self, mock_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = mock_program_dao.do_select_all(RAMSTKHardware)[0]

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['alt_part_number'] == ''
        assert _attributes['attachments'] == ''
        assert _attributes['cage_code'] == ''
        assert _attributes['category_id'] == 0
        assert _attributes['comp_ref_des'] == 'S1'
        assert _attributes['cost'] == 0.0
        assert _attributes['cost_failure'] == 0.0
        assert _attributes['cost_hour'] == 0.0
        assert _attributes['cost_type_id'] == 0
        assert _attributes['description'] == 'Test System'
        assert _attributes['duty_cycle'] == 100.0
        assert _attributes['figure_number'] == ''
        assert _attributes['lcn'] == ''
        assert _attributes['level'] == 0
        assert _attributes['manufacturer_id'] == 0
        assert _attributes['mission_time'] == 100.0
        assert _attributes['name'] == ''
        assert _attributes['nsn'] == ''
        assert _attributes['page_number'] == ''
        assert _attributes['parent_id'] == 0
        assert _attributes['part'] == 0
        assert _attributes['part_number'] == ''
        assert _attributes['quantity'] == 1
        assert _attributes['ref_des'] == 'S1'
        assert _attributes['remarks'] == ''
        assert _attributes['repairable'] == 0
        assert _attributes['specification_number'] == ''
        assert _attributes['subcategory_id'] == 0
        assert _attributes['tagged_part'] == 0
        assert _attributes['total_cost'] == 0.0
        assert _attributes['total_part_count'] == 0
        assert _attributes['total_power_dissipation'] == 0.0
        assert _attributes['year_of_manufacture'] == date.today().year

    @pytest.mark.unit
    def test_set_attributes(self, mock_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = mock_program_dao.do_select_all(RAMSTKHardware)[0]

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.unit
    def test_set_attributes_none_value(self, mock_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = mock_program_dao.do_select_all(RAMSTKHardware)[0]

        ATTRIBUTES['nsn'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['nsn'] == ''

    @pytest.mark.unit
    def test_set_attributes_unknown_attributes(self, mock_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = mock_program_dao.do_select_all(RAMSTKHardware)[0]

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
