# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.requirement.requirement_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRequirement
from ramstk.db.base import BaseDatabase
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
    _requirement_1.requirement_code = 'REL.1'
    _requirement_1.specification = ''
    _requirement_1.requirement_type = 0
    _requirement_1.validated = 0
    _requirement_1.validated_date = date.today()
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

    _requirement_2 = RAMSTKRequirement()
    _requirement_2.revision_id = 1
    _requirement_2.requirement_id = 2
    _requirement_2.derived = 1
    _requirement_2.description = ('Derived requirement #1 for base '
                                  'requirement #1.')
    _requirement_2.figure_number = ''
    _requirement_2.owner = 0
    _requirement_2.page_number = ''
    _requirement_2.parent_id = 1
    _requirement_2.priority = 0
    _requirement_2.requirement_code = 'REL.1.1'
    _requirement_2.specification = ''
    _requirement_2.requirement_type = 0
    _requirement_2.validated = 0
    _requirement_2.validated_date = date.today()
    _requirement_2.q_clarity_0 = 0
    _requirement_2.q_clarity_1 = 0
    _requirement_2.q_clarity_2 = 0
    _requirement_2.q_clarity_3 = 0
    _requirement_2.q_clarity_4 = 0
    _requirement_2.q_clarity_5 = 0
    _requirement_2.q_clarity_6 = 0
    _requirement_2.q_clarity_7 = 0
    _requirement_2.q_clarity_8 = 0
    _requirement_2.q_complete_0 = 0
    _requirement_2.q_complete_1 = 0
    _requirement_2.q_complete_2 = 0
    _requirement_2.q_complete_3 = 0
    _requirement_2.q_complete_4 = 0
    _requirement_2.q_complete_5 = 0
    _requirement_2.q_complete_6 = 0
    _requirement_2.q_complete_7 = 0
    _requirement_2.q_complete_8 = 0
    _requirement_2.q_complete_9 = 0
    _requirement_2.q_consistent_0 = 0
    _requirement_2.q_consistent_1 = 0
    _requirement_2.q_consistent_2 = 0
    _requirement_2.q_consistent_3 = 0
    _requirement_2.q_consistent_4 = 0
    _requirement_2.q_consistent_5 = 0
    _requirement_2.q_consistent_6 = 0
    _requirement_2.q_consistent_7 = 0
    _requirement_2.q_consistent_8 = 0
    _requirement_2.q_verifiable_0 = 0
    _requirement_2.q_verifiable_1 = 0
    _requirement_2.q_verifiable_2 = 0
    _requirement_2.q_verifiable_3 = 0
    _requirement_2.q_verifiable_4 = 0
    _requirement_2.q_verifiable_5 = 0

    DAO = MockDAO()
    DAO.table = [
        _requirement_1,
        _requirement_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Requirement data manager."""
        DUT = dmRequirement()

        assert isinstance(DUT, dmRequirement)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'requirements'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_requirement')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_requirements')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_requirement_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_requirements_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_requirement_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'wvw_editing_requirement')
        assert pub.isSubscribed(DUT.do_create_code,
                                'request_create_requirement_code')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_requirement')
        assert pub.isSubscribed(DUT._do_insert_requirement,
                                'request_insert_requirement')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(
            tree.get_node(1).data['requirement'], RAMSTKRequirement)

        print("\033[36m\nsucceed_retrieve_requirements topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree object populated with
        RAMSTKRequirement instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_requirements')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_requirements')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear the existing Tree when a new group of
        requirements is selected."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_requirements')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_requirements')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKRequirement on
        success."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _requirement = DUT.do_select(1, table='requirement')

        assert isinstance(_requirement, RAMSTKRequirement)
        assert _requirement.description == ''
        assert _requirement.priority == 0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Requirement ID is
        requested."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='requirement') is None


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_requirement topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent requirement ID 300.')
        print("\033[35m\nfail_delete_requirement topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent requirement ID 2.')
        print("\033[35m\nfail_delete_requirement topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_requirement')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a non-existent requirement."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_requirement')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree,
                      'fail_delete_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree,
                        'fail_delete_requirement')


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['requirement_id'] == 1
        assert attributes['description'] == ''
        assert attributes['priority'] == 0
        print(
            "\033[36m\nsucceed_get_requirement_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(
            tree.get_node(1).data['requirement'], RAMSTKRequirement)
        print("\033[36m\nsucceed_get_requirement_tree topic was broadcast")

    def on_succeed_create_code(self, requirement_code):
        assert requirement_code == 'DOYLE-0001'
        print("\033[36m\nsucceed_create_requirement_code topic was "
              "broadcast")

    def on_fail_create_code_non_existent_id(self, error_message):
        assert error_message == ('do_create_code: No data package found for '
                                 'requirement ID 10.')
        print("\033[36m\nfail_create_requirement_code topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return a dict of requirement attributes
        on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_requirement_attributes')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'requirement')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_requirement_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(node_id=[1, -1],
                              package={'requirement_code': 'REQ-0001'})
        assert DUT.do_select(
            1, table='requirement').requirement_code == 'REQ-0001'

    @pytest.mark.unit
    def test_do_set_attributes_default(self, mock_program_dao):
        """do_set_attributes() should set validation date to today() if no
        value is passed."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_requirement_attributes',
                        node_id=[1, -1],
                        package={'validated_date': None})
        assert DUT.do_select(
            1, table='requirement').validated_date == date.today()

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the requirement treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_requirements_tree')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_requirements_tree')

    @pytest.mark.unit
    def test_do_create_code(self, mock_program_dao):
        """do_create_requirement_code() should return."""
        pub.subscribe(self.on_succeed_create_code,
                      'succeed_create_requirement_code')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_create_requirement_code',
                        node_id=1,
                        prefix="DOYLE")

        pub.unsubscribe(self.on_succeed_create_code,
                        'succeed_create_requirement_code')

    @pytest.mark.unit
    def test_do_create_code_non_existent_id(self, mock_program_dao):
        """do_create_requirement_code() should send the fail message when there
        is no node in the tree for the passed Requirement ID."""
        pub.subscribe(self.on_fail_create_code_non_existent_id,
                      'fail_create_requirement_code')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_create_requirement_code',
                        node_id=10,
                        prefix="DOYLE")

        pub.unsubscribe(self.on_fail_create_code_non_existent_id,
                        'fail_create_requirement_code')

    @pytest.mark.unit
    def test_do_create_all_codes(self, mock_program_dao):
        """do_create_requirement_code() should return."""
        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_create_all_requirement_codes', prefix="DOYLE")

        assert DUT.tree.get_node(
            2).data['requirement'].requirement_code == 'DOYLE-0002'


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(3).data['requirement'], RAMSTKRequirement)
        assert tree.get_node(3).data['requirement'].requirement_id == 3
        assert tree.get_node(
            3).data['requirement'].description == 'New Requirement'

        print("\033[36m\nsucceed_insert_requirement topic was broadcast")

    def on_succeed_insert_child(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(3).data['requirement'], RAMSTKRequirement)
        assert tree.get_node(3).data['requirement'].parent_id == 1
        assert tree.get_node(3).data['requirement'].requirement_id == 3
        assert tree.get_node(
            3).data['requirement'].description == 'New Requirement'
        print("\033[36m\nsucceed_insert_requirement topic was broadcast")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            '_do_insert_requirement: Attempted to insert child requirement '
            'under non-existent requirement ID 32.')
        print("\033[35m\nfail_insert_requirement topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new top-level requirement."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=0)

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_requirement')

    @pytest.mark.unit
    def test_do_insert_child(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new child requirement."""
        pub.subscribe(self.on_succeed_insert_child,
                      'succeed_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=1)

        pub.unsubscribe(self.on_succeed_insert_child,
                        'succeed_insert_requirement')

    @pytest.mark.unit
    def test_do_insert_no_parent(self, mock_program_dao):
        """do_insert() should send the fail message attempting to add a child
        to a non-existent requirement."""
        pub.subscribe(self.on_fail_insert_no_parent, 'fail_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_requirement(parent_id=32)

        pub.unsubscribe(self.on_fail_insert_no_parent,
                        'fail_insert_requirement')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent requirement with '
            'requirement ID 100.')
        print("\033[35m\nfail_update_requirement topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for requirement ID 1.')
        print("\033[35m\nfail_update_requirement topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(100, table='requirement')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_requirement')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should send the fail_update_requirement message when
        there is no data package attached to the node."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('requirement')
        DUT.do_update(1, table='requirement')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_requirement')
