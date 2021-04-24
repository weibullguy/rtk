# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.failure_definition.unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure definition module algorithms and models."""

# Third Party Imports
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFailureDefinition
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKFailureDefinition


@pytest.fixture
def mock_program_dao(monkeypatch):
    _definition_1 = RAMSTKFailureDefinition()
    _definition_1.revision_id = 1
    _definition_1.definition_id = 1
    _definition_1.definition = 'Mock Failure Definition 1'

    _definition_2 = RAMSTKFailureDefinition()
    _definition_2.revision_id = 1
    _definition_2.definition_id = 2
    _definition_2.definition = 'Mock Failure Definition 2'

    DAO = MockDAO()
    DAO.table = [
        _definition_1,
        _definition_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Revision data manager."""
        DUT = dmFailureDefinition()

        assert isinstance(DUT, dmFailureDefinition)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'failure_definitions'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_failure_definition_attributes')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update,
                                'request_update_failure_definition')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_failure_definitions')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_failure_definition_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_failure_definition_attributes')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'lvw_editing_failure_definition')
        assert pub.isSubscribed(DUT._do_delete,
                                'request_delete_failure_definitions')
        assert pub.isSubscribed(DUT._do_insert_failure_definition,
                                'request_insert_failure_definitions')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFailureDefinition instances on success."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFailureDefinition instances on success when there is already a
        tree of definitions."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of RAMSTKFailureDefinition on
        success."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _failure_definition = DUT.do_select(1, table='failure_definition')

        assert isinstance(_failure_definition, RAMSTKFailureDefinition)
        assert _failure_definition.definition == 'Mock Failure Definition 1'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='failure_definition') is None


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_failure_definition topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent failure '
            'definition ID 10.')
        print("\033[35m\nfail_delete_failure_definition topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete_failure_definition() should send the success message
        after successfully deleting a definition."""
        pub.subscribe(self.on_succeed_delete,
                      'succeed_delete_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(1)

        with pytest.raises(AttributeError):
            __ = DUT.tree.get_node(1).data['failure_definition']

        pub.unsubscribe(self.on_succeed_delete,
                        'succeed_delete_failure_definition')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete_failure_definition() should send the fail message when
        attempting to delete a non-existent failure definition."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_failure_definition')


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['definition'] == 'Mock Failure Definition 1'
        print("\033[36m\nsucceed_get_failure_definition_attributes topic was "
              "broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)
        print(
            "\033[36m\nsucceed_get_failure_definition_tree topic was broadcast"
        )

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return a dict of failure definition
        records on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_failure_definition_attributes')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'failure_definition')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_failure_definition_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(node_id=[1, 1, ''],
                              package={'definition': 'Test Description'})

        assert DUT.do_select(
            1, table='failure_definition').definition == 'Test Description'

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the failure definition treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_failure_definition_tree')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_failure_definition_tree')


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree[3].data['failure_definition'],
                          RAMSTKFailureDefinition)
        print(
            "\033[36m\nsucceed_insert_failure_definition topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new failure definition."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_failure_definition()

        assert isinstance(
            DUT.tree.get_node(1).data['failure_definition'],
            RAMSTKFailureDefinition)

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_failure_definition')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent failure definition '
            'with failure definition ID 100.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for failure definition ID 1.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update_failure_definition() should broadcast the fail message
        when attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(100, table='failure_definitions')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_failure_definition')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('failure_definition')

        DUT.do_update(1, table='failure_definition')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_failure_definition')
