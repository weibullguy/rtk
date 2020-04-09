# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_requirement.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRequirement, mmRequirement
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRequirement

MOCK_REQUIREMENTS = {
    1: {
        'derived': 0,
        'description': '',
        'figure_number': '',
        'owner': '',
        'page_number': '',
        'parent_id': 0,
        'priority': 0,
        'requirement_code': 'REL.1',
        'specification': '',
        'requirement_type': '',
        'validated': 0,
        'validated_date': date.today(),
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
        'q_verifiable_5': 0
    },
    2: {
        'derived': 1,
        'description': 'Derived requirement #1 for base requirement #1.',
        'figure_number': '',
        'owner': '',
        'page_number': '',
        'parent_id': 1,
        'priority': 0,
        'requirement_code': 'REL.1.1',
        'specification': '',
        'requirement_type': '',
        'validated': 0,
        'validated_date': date.today(),
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
        'q_verifiable_5': 0
    }
}


class MockDao:
    _all = []

    def do_delete(self, item):
        for _idx, _requirement in enumerate(self._all):
            try:
                if _requirement.requirement_id == item.requirement_id:
                    self._all.pop(_idx)
            except AttributeError:
                raise DataAccessError('')

    def do_insert(self, record):
        self._all.append(record)

    def do_select_all(self, table, key, value):
        if table == RAMSTKRequirement:
            self._all = []
            for _key in MOCK_REQUIREMENTS:
                _record = table()
                _record.revision_id = value
                _record.requirement_id = _key
                _record.set_attributes(MOCK_REQUIREMENTS[_key])
                self._all.append(_record)

        return self._all

    def do_update(self, record):
        for _key in MOCK_REQUIREMENTS:
            if _key == record.requirement_id:
                MOCK_REQUIREMENTS[_key]['derived'] = record.derived
                MOCK_REQUIREMENTS[_key]['description'] = record.description
                MOCK_REQUIREMENTS[_key]['figure_number'] = record.figure_number
                MOCK_REQUIREMENTS[_key]['owner'] = record.owner
                MOCK_REQUIREMENTS[_key]['page_number'] = record.page_number
                MOCK_REQUIREMENTS[_key]['parent_id'] = record.parent_id
                MOCK_REQUIREMENTS[_key]['priority'] = record.priority
                MOCK_REQUIREMENTS[_key]['requirement_code'] = \
                    record.requirement_code
                MOCK_REQUIREMENTS[_key]['specification'] = record.specification
                MOCK_REQUIREMENTS[_key]['requirement_type'] = \
                    record.requirement_type
                MOCK_REQUIREMENTS[_key]['validated'] = record.validate
                MOCK_REQUIREMENTS[_key][
                    'validated_date'] = record.validated_date


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Requirement data manager."""
        DUT = dmRequirement()

        assert isinstance(DUT, dmRequirement)
        assert isinstance(DUT.tree, Tree)
        assert DUT.dao is None
        assert DUT._tag == 'requirement'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'succeed_select_revision')
        assert pub.isSubscribed(DUT._do_delete_requirement,
                                'request_delete_requirement')
        assert pub.isSubscribed(DUT.do_insert_requirement,
                                'request_insert_requirement')
        assert pub.isSubscribed(DUT.do_update_requirement,
                                'request_update_requirement')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_requirements')
        assert pub.isSubscribed(DUT._do_get_attributes,
                                'request_get_requirement_attributes')
        assert pub.isSubscribed(DUT.do_get_all_attributes,
                                'request_get_all_requirement_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_requirement_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_requirement_attributes')
        assert pub.isSubscribed(DUT.do_set_all_attributes,
                                'request_set_all_requirement_attributes')

    @pytest.mark.unit
    def test_matrix_manager_create(self):
        """__init__() should create an instance of the requirement matrix manager."""
        DUT = mmRequirement()

        assert isinstance(DUT, mmRequirement)
        assert isinstance(DUT._column_tables, dict)
        assert isinstance(DUT._col_tree, Tree)
        assert isinstance(DUT._row_tree, Tree)
        assert DUT.dic_matrices == {}
        assert DUT.n_row == 1
        assert DUT.n_col == 1
        assert pub.isSubscribed(DUT._do_create, 'succeed_retrieve_requirements')
        assert pub.isSubscribed(DUT._do_delete_hardware,
                                'succeed_delete_hardware')
        assert pub.isSubscribed(DUT._do_delete_validation,
                                'succeed_delete_validation')
        assert pub.isSubscribed(DUT.do_delete_row,
                                'succeed_delete_requirement')
        assert pub.isSubscribed(DUT.do_insert_row,
                                'succeed_insert_requirement')
        assert pub.isSubscribed(DUT._do_insert_hardware,
                                'succeed_insert_hardware')
        assert pub.isSubscribed(DUT._do_insert_validation,
                                'succeed_insert_validation')
        assert pub.isSubscribed(DUT.do_update,
                                'request_update_requirement_matrix')
        assert pub.isSubscribed(DUT._on_get_tree,
                                'succeed_get_requirement_tree')
        assert pub.isSubscribed(DUT._on_get_tree, 'succeed_get_hardware_tree')
        assert pub.isSubscribed(DUT._on_get_tree,
                                'succeed_get_validation_tree')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_requirements(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_retrieve_requirements topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all(1) should return a Tree() object populated with RAMSTKRequirement instances on success."""
        pub.subscribe(self.on_succeed_retrieve_requirements,
                      'succeed_retrieve_requirements')
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.tree.get_node(1).data, dict)
        assert isinstance(
            DUT.tree.get_node(1).data['requirement'], RAMSTKRequirement)

        pub.unsubscribe(self.on_succeed_retrieve_requirements,
                        'succeed_retrieve_requirements')

    @pytest.mark.unit
    def test_do_select_requirement(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKRequirement on success."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        _requirement = DUT.do_select(1, table='requirement')

        assert isinstance(_requirement, RAMSTKRequirement)
        assert _requirement.description == ''
        assert _requirement.priority == 0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is requested."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Requirement ID is requested."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        assert DUT.do_select(100, table='requirement') is None

    @pytest.mark.skip
    def test_do_create_matrix(self, test_program_dao):
        """_do_create() should create an instance of the hardware matrix manager."""
        DATAMGR = dmRequirement()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(1)
        DUT = mmRequirement()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS3',
                                  identifier=4,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS4',
                                  identifier=5,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A1',
                                  identifier=6,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2',
                                  identifier=7,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2:C1',
                                  identifier=8,
                                  parent=0,
                                  data=None)

        DUT._do_create(1)

        assert DUT.do_select('rqrmnt_hrdwr', 1, 0) == 'S1'
        assert DUT.do_select('rqrmnt_hrdwr', 2, 0) == 'S1:SS1'
        assert DUT.do_select('rqrmnt_hrdwr', 3, 0) == 'S1:SS2'
        assert DUT.do_select('rqrmnt_hrdwr', 1, 1) == 0


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_requirement(self, node_id):
        assert node_id == 2
        print("\033[36m\nsucceed_delete_requirement topic was broadcast.")

    def on_fail_delete_requirement(self, error_message):
        assert error_message == (
            'Attempted to delete non-existent requirement ID '
            '300.')
        print("\033[35m\nfail_delete_requirement topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_requirement(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree."""
        pub.subscribe(self.on_succeed_delete_requirement,
                      'succeed_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT._do_delete_requirement(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_requirement,
                        'succeed_delete_requirement')

    @pytest.mark.unit
    def test_do_delete_requirement_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete a non-existent requirement."""
        pub.subscribe(self.on_fail_delete_requirement,
                      'fail_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT._do_delete_requirement(300)

    @pytest.mark.skip
    def test_do_delete_matrix_column(self, test_program_dao):
        """do_delete_column() should remove the appropriate column from the requested requirement matrix."""
        DATAMGR = dmRequirement()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmRequirement()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS3',
                                  identifier=4,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS4',
                                  identifier=5,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A1',
                                  identifier=6,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2',
                                  identifier=7,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2:C1',
                                  identifier=8,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('rqrmnt_hrdwr', 1, 1) == 0

        pub.sendMessage('succeed_delete_hardware', node_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('rqrmnt_hrdwr', 1, 1)

    @pytest.mark.skip
    def test_do_delete_matrix_row(self, test_program_dao):
        """do_delete_row() should remove the appropriate row from the requirement matrices."""
        DATAMGR = dmRequirement()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmRequirement()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS3',
                                  identifier=4,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS4',
                                  identifier=5,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A1',
                                  identifier=6,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2',
                                  identifier=7,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2:C1',
                                  identifier=8,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        assert DUT.do_select('rqrmnt_hrdwr', 1, 2) == 0

        pub.sendMessage('succeed_delete_requirement', node_id=2)

        with pytest.raises(KeyError):
            DUT.do_select('rqrmnt_hrdwr', 1, 2)


class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_requirement_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['requirement_id'] == 1
        assert attributes['description'] == ''
        assert attributes['priority'] == 0
        print(
            "\033[36m\nsucceed_get_requirement_attributes topic was broadcast")

    def on_succeed_get_all_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['requirement_id'] == 1
        assert attributes['description'] == ''
        assert attributes['priority'] == 0
        print(
            "\033[36m\nsucceed_get_all_requirement_attributes topic was broadcast"
        )

    def on_succeed_get_requirement_tree(self, dmtree):
        assert isinstance(dmtree, Tree)
        assert isinstance(dmtree.get_node(1).data, dict)
        assert isinstance(
            dmtree.get_node(1).data['requirement'], RAMSTKRequirement)
        print("\033[36m\nsucceed_get_requirement_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_requirement(self, mock_program_dao):
        """_do_get_attributes() should return a dict of requirement attributes on success."""
        pub.subscribe(self.on_succeed_get_requirement_attrs,
                      'succeed_get_requirement_attributes')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT._do_get_attributes(1, 'requirement')

    @pytest.mark.unit
    def test_do_get_all_attributes_data_manager(self, mock_program_dao):
        """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
        pub.subscribe(self.on_succeed_get_all_attrs,
                      'succeed_get_all_requirement_attributes')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT.do_get_all_attributes(1)

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        pub.sendMessage('request_set_requirement_attributes',
                        node_id=1,
                        key='requirement_code',
                        value='FUNC-0001')
        assert DUT.do_select(
            1, table='requirement').requirement_code == 'FUNC-0001'

    @pytest.mark.unit
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        pub.sendMessage('request_set_all_requirement_attributes',
                        attributes={
                            'requirement_id': 1,
                            'requirement_code': 'PERF-0021',
                            'description':
                            'This is a description added by a test.',
                            'priority': 2
                        })
        assert DUT.do_select(
            1, table='requirement').requirement_code == 'PERF-0021'
        assert DUT.do_select(
            1, table='requirement'
        ).description == 'This is a description added by a test.'
        assert DUT.do_select(1, table='requirement').priority == 2

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the requirement treelib Tree."""
        pub.subscribe(self.on_succeed_get_requirement_tree,
                      'succeed_get_requirement_tree')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_requirement_tree,
                        'succeed_get_requirement_tree')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_requirement(self, node_id):
        assert node_id == 3
        print("\033[36m\nsucceed_insert_requirement topic was broadcast")

    def on_fail_insert_requirement(self, error_message):
        assert error_message == ('Attempting to add child requirement to '
                                 'non-existent requirement 32.')
        print("\033[35m\nfail_insert_requirement topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_sibling_requirement(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new top-level requirement."""
        pub.subscribe(self.on_succeed_insert_requirement,
                      'succeed_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT.do_insert_requirement(parent_id=0)

        assert isinstance(
            DUT.tree.get_node(3).data['requirement'], RAMSTKRequirement)
        assert DUT.tree.get_node(3).data['requirement'].requirement_id == 3
        assert DUT.tree.get_node(
            3).data['requirement'].description == 'New Requirement'

        pub.unsubscribe(self.on_succeed_insert_requirement,
                        'succeed_insert_requirement')

    @pytest.mark.unit
    def test_do_insert_child_requirement(self, mock_program_dao):
        """do_insert() should send the success message after successfully inserting a new child requirement."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT.do_insert_requirement(parent_id=1)

        assert isinstance(
            DUT.tree.get_node(3).data['requirement'], RAMSTKRequirement)
        assert DUT.tree.get_node(3).data['requirement'].parent_id == 1
        assert DUT.tree.get_node(3).data['requirement'].requirement_id == 3
        assert DUT.tree.get_node(
            3).data['requirement'].description == 'New Requirement'

    @pytest.mark.unit
    def test_do_insert_child_requirement_non_existent_id(
            self, mock_program_dao):
        """do_insert() should send the fail message attempting to add a child to a non-existent requirement."""
        pub.subscribe(self.on_fail_insert_requirement,
                      'fail_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT.do_insert_requirement(parent_id=32)

    @pytest.mark.skip
    def test_do_insert_matrix_column(self, test_program_dao):
        """do_insert_column() should add a column to the right of the requested requirement matrix."""
        DATAMGR = dmRequirement()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmRequirement()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS3',
                                  identifier=4,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS4',
                                  identifier=5,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A1',
                                  identifier=6,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2',
                                  identifier=7,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2:C1',
                                  identifier=8,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('rqrmnt_hrdwr', 9, 1)

        pub.sendMessage('succeed_insert_hardware', node_id=9)

        assert DUT.do_select('rqrmnt_hrdwr', 9, 1) == 0

    @pytest.mark.skip
    def test_do_insert_matrix_row(self, test_program_dao):
        """do_insert_row() should add a row to the end of each requirement matrix."""
        DATAMGR = dmRequirement()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmRequirement()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS3',
                                  identifier=4,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS4',
                                  identifier=5,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A1',
                                  identifier=6,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2',
                                  identifier=7,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2:C1',
                                  identifier=8,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        with pytest.raises(KeyError):
            DUT.do_select('rqrmnt_hrdwr', 1, 10)

        pub.sendMessage('succeed_insert_requirement', node_id=5)
        assert DUT.do_select('rqrmnt_hrdwr', 1, 5) == 0
        assert DUT.do_select('rqrmnt_hrdwr', 2, 5) == 0
        assert DUT.do_select('rqrmnt_hrdwr', 3, 5) == 0


class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_requirement(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_requirement topic was broadcast")

    def on_fail_update_requirement(self, error_message):
        assert error_message == (
            'Attempted to save non-existent requirement with requirement ID 100.'
        )
        print("\033[35m\nfail_update_requirement topic was broadcast")

    def on_succeed_update_matrix(self):
        assert True
        print("\033[36m\nsucceed_update_matrix topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """ do_update() should return a zero error code on success. """
        pub.subscribe(self.on_succeed_update_requirement,
                      'succeed_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)

        _requirement = DUT.do_select(1, table='requirement')
        _requirement.description = 'Test Requirement'
        DUT.do_update_requirement(1)

        DUT.do_select_all(1)
        _requirement = DUT.do_select(1, table='requirement')

        assert _requirement.description == 'Test Requirement'

        pub.unsubscribe(self.on_succeed_update_requirement,
                        'succeed_update_requirement')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """ do_update() should return a non-zero error code when passed a Requirement ID that doesn't exist. """
        pub.subscribe(self.on_fail_update_requirement,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(1)
        DUT.do_update_requirement(100)

    @pytest.mark.integration
    def test_do_update_matrix_manager(self, test_program_dao):
        """do_update() should send the success message when the matrix is updated successfully."""
        pub.subscribe(self.on_succeed_update_matrix, 'succeed_update_matrix')

        DATAMGR = dmRequirement()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(revision_id=1)
        DUT = mmRequirement()
        DUT._col_tree.create_node(tag='hardware',
                                  identifier=0,
                                  parent=None,
                                  data=None)
        DUT._col_tree.create_node(tag='S1', identifier=1, parent=0, data=None)
        DUT._col_tree.create_node(tag='S1:SS1',
                                  identifier=2,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS2',
                                  identifier=3,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS3',
                                  identifier=4,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS4',
                                  identifier=5,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A1',
                                  identifier=6,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2',
                                  identifier=7,
                                  parent=0,
                                  data=None)
        DUT._col_tree.create_node(tag='S1:SS1:A2:C1',
                                  identifier=8,
                                  parent=0,
                                  data=None)

        pub.sendMessage('succeed_select_revision', revision_id=1)

        DUT.dic_matrices['rqrmnt_hrdwr'][1][2] = 1
        DUT.dic_matrices['rqrmnt_hrdwr'][1][3] = 2
        DUT.dic_matrices['rqrmnt_hrdwr'][2][2] = 2
        DUT.dic_matrices['rqrmnt_hrdwr'][3][5] = 1

        pub.sendMessage('request_update_requirement_matrix',
                        revision_id=1,
                        matrix_type='rqrmnt_hrdwr')

        pub.unsubscribe(self.on_succeed_update_matrix, 'succeed_update_matrix')
