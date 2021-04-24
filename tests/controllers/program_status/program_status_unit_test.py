# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_status.program_status_unit_test.py is part
#       of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmProgramStatus
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKProgramStatus


@pytest.fixture
def mock_program_dao(monkeypatch):
    _status_1 = RAMSTKProgramStatus()
    _status_1.revision_id = 1
    _status_1.status_id = 1
    _status_1.cost_remaining = 284.98
    _status_1.date_status = date.today() - timedelta(days=1)
    _status_1.time_remaining = 125.0

    _status_2 = RAMSTKProgramStatus()
    _status_2.revision_id = 1
    _status_2.status_id = 2
    _status_2.cost_remaining = 212.32
    _status_2.date_status = date.today()
    _status_2.time_remaining = 112.5

    DAO = MockDAO()
    DAO.table = [
        _status_1,
        _status_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Validation data manager."""
        DUT = dmProgramStatus()

        assert isinstance(DUT, dmProgramStatus)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'program_status'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_program_status')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_program_status')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_program_status_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_program_status_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_program_status_attributes')
        assert pub.isSubscribed(DUT._do_delete,
                                'request_delete_program_status')
        assert pub.isSubscribed(DUT._do_insert_program_status,
                                'request_insert_program_status')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['program_status'], RAMSTKProgramStatus)
        print("\033[36m\nsucceed_retrieve_program_status topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_program_status')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKValidation on
        success."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _status = DUT.do_select(2, table='program_status')

        assert isinstance(_status, RAMSTKProgramStatus)
        assert _status.cost_remaining == 212.32
        assert _status.time_remaining == 112.5

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Validation ID is
        requested."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='program_status') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_program_status topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent program status ID '
            '300.')
        print("\033[35m\nfail_delete_program_status topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent program status '
            'ID 2.')
        print("\033[35m\nfail_delete_program_status topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete,
                        'succeed_delete_program_status')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a record that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_program_status')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree,
                      'fail_delete_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree,
                        'fail_delete_program_status')


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['status_id'] == 1
        assert attributes['cost_remaining'] == 284.98
        assert attributes['date_status'] == date.today() - timedelta(days=1)
        assert attributes['time_remaining'] == 125.0
        print("\033[36m\nsucceed_get_program_status_attributes topic was "
              "broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['program_status'], RAMSTKProgramStatus)
        print("\033[36m\nsucceed_get_program_status_tree topic was broadcast")

    def on_request_get_program_status_tree(self):
        print("\033[36m\nrequest_get_program_status_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of validation attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_program_status_attributes')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'program_status')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_program_status_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(node_id=[1], package={'cost_remaining': 8321.54})
        assert DUT.do_select(1,
                             table='program_status').cost_remaining == 8321.54

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """_on_get_status_tree() should return the status treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_program_status_tree')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_program_status_tree')

    @pytest.mark.unit
    def test_on_calculate_plan(self, mock_program_dao):
        """_do_set_attributes() should update program status on successful
        calculation of the plan."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_set_attributes(cost_remaining=14608.45, time_remaining=469.00)

        _node_id = DUT._dic_status[date.today()]

        assert DUT.tree.get_node(
            _node_id).data['program_status'].cost_remaining == 14608.45
        assert DUT.tree.get_node(
            _node_id).data['program_status'].time_remaining == 469.00

    @pytest.mark.unit
    def test_on_calculate_plan_no_record(self, mock_program_dao):
        """_do_set_attributes() should update program status on successful
        calculation of the plan."""
        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._dic_status.pop(date.today())
        DUT._do_set_attributes(cost_remaining=1408.45, time_remaining=49.00)

        _node_id = DUT._dic_status[date.today()]

        assert DUT.tree.get_node(
            _node_id).data['program_status'].cost_remaining == 1408.45
        assert DUT.tree.get_node(
            _node_id).data['program_status'].time_remaining == 49.00


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(3).data['program_status'], RAMSTKProgramStatus)
        assert tree.get_node(3).data['program_status'].status_id == 3
        assert tree.get_node(
            3).data['program_status'].date_status == date.today()
        print("\033[36m\nsucceed_insert_program_status topic was broadcast.")

    def on_fail_insert_program_status_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_program_status topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_validation() should send the success message after
        successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_program_status()

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_program_status')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent program status with '
            'program status ID 100.')
        print("\033[35m\nfail_update_program_status topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ('do_update: No data package found for '
                                 'program status ID 1.')
        print("\033[35m\nfail_update_program_status topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(100, table='program_status')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_program_status')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('program_status')

        DUT.do_update(1, table='program_status')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_program_status')
