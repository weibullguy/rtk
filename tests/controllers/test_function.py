# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_function.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Function algorithms and models."""

# Third Party Imports
import pytest
from __mocks__ import MOCK_FUNCTIONS, MOCK_HRDWR_TREE, MOCK_RQRMNT_TREE
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFunction, dmHardware
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFunction


class MockDao:
    _all_functions = []

    def _do_delete_function(self, record):
        for _idx, _record in enumerate(self._all_functions):
            if _record.function_id == record.function_id:
                self._all_functions.pop(_idx)

    def do_delete(self, record):
        try:
            self._do_delete_function(record)
        except AttributeError:
            raise DataAccessError('An error occurred with RAMSTK.')

    def do_insert(self, record):
        if record.parent_id == 30:
            raise DataAccessError('An error occurred with RAMSTK.')
        else:
            self._all_functions.append(record)

    def do_select_all(self,
                      table,
                      key=None,
                      value=None,
                      order=None,
                      _all=False):
        self._all_functions = []
        if table == RAMSTKFunction:
            for _key in MOCK_FUNCTIONS:
                _record = table()
                _record.revision_id = value
                _record.function_id = _key
                _record.set_attributes(MOCK_FUNCTIONS[_key])
                self._all_functions.append(_record)

        return self._all_functions

    def do_update(self, record):
        for _key in MOCK_FUNCTIONS:
            if _key == record.function_id:
                MOCK_FUNCTIONS[_key]['name'] = str(record.name)
                MOCK_FUNCTIONS[_key]['cost'] = float(record.cost)

    def get_last_id(self, table, id_column):
        return max(MOCK_FUNCTIONS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Function data manager."""
        DUT = dmFunction()

        assert isinstance(DUT, dmFunction)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'functions'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_function')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_functions')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_function_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_functions_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_function_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_function')
        assert pub.isSubscribed(DUT._do_insert_function,
                                'request_insert_function')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_functions(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['function'], RAMSTKFunction)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFunction instances on success."""
        pub.subscribe(self.on_succeed_retrieve_functions,
                      'succeed_retrieve_functions')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_retrieve_functions,
                        'succeed_retrieve_functions')

    @pytest.mark.unit
    def test_do_select_function(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKFunction on
        success."""
        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _function = DUT.do_select(1, table='function')

        assert isinstance(_function, RAMSTKFunction)
        assert _function.availability_logistics == 1.0
        assert _function.name == 'Function Name'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Function ID is
        requested."""
        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='function') is None


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_function(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_function topic was broadcast.")

    def on_fail_delete_function(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent function ID 300.')
        print("\033[35m\nfail_delete_function topic was broadcast.")

    def on_fail_delete_function_no_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent function ID 2.')
        print("\033[35m\nfail_delete_function topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_function(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_function,
                      'succeed_delete_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete_function,
                        'succeed_delete_function')

    @pytest.mark.unit
    def test_do_delete_function_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a function ID that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_function, 'fail_delete_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_function, 'fail_delete_function')

    @pytest.mark.unit
    def test_do_delete_function_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree."""
        pub.subscribe(self.on_fail_delete_function_no_tree,
                      'fail_delete_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_function_no_tree,
                        'fail_delete_function')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_function(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_fail_insert_function_no_parent(self, error_message):
        assert error_message == ('_do_insert_function: Attempted to insert '
                                 'child function under non-existent function ID 40.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    def on_fail_insert_function_db_error(self, error_message):
        assert error_message == ('An error occurred with RAMSTK.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling_function(self, mock_program_dao):
        """_do_insert_function() should send the success message after
        successfully inserting a sibling function."""
        pub.subscribe(self.on_succeed_insert_function,
                      'succeed_insert_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_function()

        assert isinstance(
            DUT.tree.get_node(3).data['function'], RAMSTKFunction)
        assert DUT.tree.get_node(3).data['function'].function_id == 3
        assert DUT.tree.get_node(3).data['function'].name == 'New Function'

        pub.unsubscribe(self.on_succeed_insert_function,
                        'succeed_insert_function')

    @pytest.mark.unit
    def test_do_insert_child_function(self, mock_program_dao):
        """_do_insert_function() should send the success message after
        successfully inserting a child function."""
        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_function(parent_id=2)

        assert isinstance(
            DUT.tree.get_node(3).data['function'], RAMSTKFunction)
        assert DUT.tree.get_node(3).data['function'].function_id == 3
        assert DUT.tree.get_node(3).data['function'].name == 'New Function'

    @pytest.mark.unit
    def test_do_insert_function_no_parent(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_function_no_parent,
                      'fail_insert_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_function(parent_id=40)

        pub.unsubscribe(self.on_fail_insert_function_no_parent,
                        'fail_insert_function')

    @pytest.mark.unit
    def test_do_insert_function_database_error(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_function_db_error,
                      'fail_insert_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_function(parent_id=30)

        pub.unsubscribe(self.on_fail_insert_function_db_error, 'fail_insert_function')

@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_function_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_id'] == 1
        assert attributes['name'] == 'Function Name'
        assert attributes['safety_critical'] == 0
        print("\033[36m\nsucceed_get_function_attributes topic was broadcast.")

    def on_succeed_get_function_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['function'], RAMSTKFunction)
        print("\033[36m\nsucceed_get_function_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes_function(self, mock_program_dao):
        """_do_get_attributes() should return a dict of function attributes on
        success."""
        pub.subscribe(self.on_succeed_get_function_attrs,
                      'succeed_get_function_attributes')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'function')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_function_attributes',
                        node_id=[1, -1],
                        package={'function_code': '-'})
        assert DUT.do_select(1, table='function').function_code == '-'

    @pytest.mark.skip
    def test_do_set_all_attributes(self, mock_program_dao):
        """do_set_all_attributes() should send the success message."""
        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_set_all_function_attributes',
                        attributes={
                            'function_id': 1,
                            'function_code': '1',
                            'remarks': 'These are remarks added by a test.',
                        })
        assert DUT.do_select(1, table='function').function_code == '1'
        assert DUT.do_select(
            1,
            table='function').remarks == 'These are remarks added by a test.'

        pub.sendMessage('request_set_all_function_attributes',
                        attributes={
                            'function_id': 1,
                            'function_code': '',
                            'remarks': '',
                        })

    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, mock_program_dao):
        """on_get_tree() should return the function treelib Tree."""
        pub.subscribe(self.on_succeed_get_function_tree,
                      'succeed_get_function_tree')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_function_tree,
                        'succeed_get_function_tree')


class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_function(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_function topic was broadcast")

    def on_fail_update_function(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent function with function ID 100.')
        print("\033[35m\nfail_update_function topic was broadcast")

    def on_fail_update_function_no_data(self, error_message):
        assert error_message == ('do_update: The value for one or more attributes for function ID 1 was the wrong type.')
        print("\033[35m\nfail_update_function topic was broadcast")

    @pytest.mark.unit
    def test_do_update_data_manager(self, mock_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_function,
                      'succeed_update_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.tree.get_node(1).data['function'].name = 'Test Function'
        DUT.do_update(1)

        DUT.do_select_all(attributes={'revision_id': 1})
        assert DUT.tree.get_node(1).data['function'].name == 'Test Function'

        pub.unsubscribe(self.on_succeed_update_function,
                        'succeed_update_function')

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_function, 'fail_update_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_function, 'fail_update_function')

    @pytest.mark.unit
    def test_do_update_wrong_data_type(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_function_no_data,
                      'fail_update_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data['function'].cost = None

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_function_no_data,
                        'fail_update_function')

    @pytest.mark.unit
    def test_do_update_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_function_no_data,
                      'fail_update_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(0)

        pub.unsubscribe(self.on_fail_update_function_no_data,
                        'fail_update_function')
