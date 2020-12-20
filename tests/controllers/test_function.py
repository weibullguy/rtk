# pylint: disable=protected-access, no-self-use, missing-docstring
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
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import dmFunction, dmHardware, mmFunction
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
            raise DataAccessError('')

    def do_insert(self, record):
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
                MOCK_FUNCTIONS[_key]['name'] = record.name

    def get_last_id(self, table, id_column):
        return max(MOCK_FUNCTIONS.keys())


@pytest.fixture
def mock_program_dao(monkeypatch):
    yield MockDao()


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a Function data manager."""
        DUT = dmFunction()

        assert isinstance(DUT, dmFunction)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'function'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_function')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_functions')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_function_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_function_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_function_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_function')
        assert pub.isSubscribed(DUT._do_insert_function,
                                'request_insert_function')

    @pytest.mark.unit
    def test_matrix_manager_create(self):
        """__init__() should create an instance of the function matrix
        manager."""
        DUT = mmFunction()

        assert isinstance(DUT, mmFunction)
        assert isinstance(DUT._column_tables, dict)
        assert isinstance(DUT._col_tree, dict)
        assert isinstance(DUT._row_tree, Tree)
        assert DUT.dic_matrices == {}
        assert DUT.n_row == 1
        assert DUT.n_col == 1
        assert pub.isSubscribed(DUT.do_create_rows,
                                'succeed_retrieve_functions')
        assert pub.isSubscribed(DUT._do_create_function_matrix_columns,
                                'succeed_retrieve_hardware')
        assert pub.isSubscribed(DUT._on_delete_function,
                                'succeed_delete_function')
        assert pub.isSubscribed(DUT._on_delete_hardware,
                                'succeed_delete_hardware')
        assert pub.isSubscribed(DUT._on_insert_function,
                                'succeed_insert_function')
        assert pub.isSubscribed(DUT._on_insert_hardware,
                                'succeed_insert_hardware')


class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_functions(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['function'], RAMSTKFunction)
        print("\033[36m\nsucceed_retrieve_functions topic was broadcast.")

    def on_request_select_matrix(self, matrix_type):
        assert matrix_type == 'fnctn_hrdwr'
        print("\033[36m\nrequest_select_matrix topic was broadcast for the "
              "fnctn_hrdwr matrix.")

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

    @pytest.mark.unit
    def test_do_create_matrix(self, mock_program_dao):
        """_do_create() should create an instance of the function matrix
        manager."""
        pub.subscribe(self.on_request_select_matrix, 'request_select_matrix')

        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_hardware', tree=MOCK_HRDWR_TREE)

        pub.unsubAll('request_select_matrix')

        assert DUT._col_tree['fnctn_hrdwr'] == MOCK_HRDWR_TREE
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1') == 0
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS1') == 0
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS2') == 0
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS3') == 0
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS4') == 0
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS1:A1') == 0
        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS1:A2') == 0

    @pytest.mark.unit
    def test_do_create_matrix_no_row_tree_hardware(self, mock_program_dao):
        """_do_create_validation_matrix_columns() should not create a vldtn-
        hrdwr matrix unless there is a row tree already populated."""
        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DUT._row_tree = Tree()

        pub.sendMessage('succeed_retrieve_hardware', tree=MOCK_HRDWR_TREE)

        assert DUT._col_tree['fnctn_hrdwr'] == MOCK_HRDWR_TREE

    @pytest.mark.unit
    def test_do_create_matrix_wrong_column_tree(self, mock_program_dao):
        """_do_create_validation_matrix_columns() should not create a matrix
        when passed a column tree that doesn't exist in the matrix dict."""
        DUT = mmFunction()
        DUT._row_tree = Tree()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_requirements', tree=MOCK_RQRMNT_TREE)

        with pytest.raises(KeyError):
            DUT._col_tree['fcntn_rqrmnt']


class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_function(self, node_id, tree):
        assert node_id == 2
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

    @pytest.mark.unit
    def test_do_delete_matrix_row(self, mock_program_dao):
        """do_delete_row() should remove the appropriate row from the hardware
        matrices."""
        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_hardware', tree=MOCK_HRDWR_TREE)

        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS4') == 0

        DATAMGR.tree.remove_node(1)
        pub.sendMessage('succeed_delete_function',
                        node_id=1,
                        tree=DATAMGR.tree)

        with pytest.raises(KeyError):
            DUT.do_select('fnctn_hrdwr', 1, 'S1:SS4')

    @pytest.mark.unit
    def test_do_delete_matrix_hardware_column(self, test_program_dao):
        """do_delete_column() should remove the appropriate column from the
        requested hardware matrix."""
        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_hardware', tree=MOCK_HRDWR_TREE)

        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS2') == 0

        pub.sendMessage('succeed_delete_hardware',
                        node_id=3,
                        tree=MOCK_HRDWR_TREE)

        with pytest.raises(KeyError):
            DUT.do_select('fnctn_hrdwr', 1, 'S1:SS2')


class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_function(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_function topic was broadcast.")

    def on_fail_insert_function(self, error_message):
        assert error_message == ('_do_insert_function: Attempting to add a function as a child of '
                                 'non-existent parent node 40.')
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
        pub.subscribe(self.on_fail_insert_function, 'fail_insert_function')

        DUT = dmFunction()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_function(parent_id=40)

    @pytest.mark.unit
    def test_do_insert_matrix_row(self, mock_program_dao):
        """do_insert_row() should add a row to the end of each hardware
        matrix."""
        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_hardware', tree=MOCK_HRDWR_TREE)

        with pytest.raises(KeyError):
            DUT.do_select('fnctn_hrdwr', 4, 'S1:SS4')

        DATAMGR.tree.create_node(tag='Test Insert Function',
                                 identifier=4,
                                 parent=1,
                                 data=None)
        pub.sendMessage('succeed_insert_function',
                        node_id=4,
                        tree=DATAMGR.tree)

        assert DUT.do_select('fnctn_hrdwr', 4, 'S1:SS4') == 0

    @pytest.mark.unit
    def test_do_insert_matrix_hardware_column(self, mock_program_dao):
        """do_insert_column() should add a column to the right of the requested
        validation matrix."""
        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('succeed_retrieve_hardware', tree=MOCK_HRDWR_TREE)

        with pytest.raises(KeyError):
            DUT.do_select('fnctn_hrdwr', 1, 'S1:SS15')

        MOCK_HRDWR_TREE.create_node(tag='S1:SS15',
                                    identifier=15,
                                    parent=0,
                                    data=None)

        pub.sendMessage('succeed_insert_hardware',
                        node_id=15,
                        tree=MOCK_HRDWR_TREE)

        assert DUT.do_select('fnctn_hrdwr', 1, 'S1:SS15') == 0


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
    def on_succeed_update_function(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_function topic was broadcast")

    def on_fail_update_function(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent function with function ID 100.')
        print("\033[35m\nfail_update_function topic was broadcast")

    def on_fail_update_function_no_data(self, error_message):
        assert error_message == ('do_update: No data package found for function ID 0.')
        print("\033[35m\nfail_update_function topic was broadcast")

    def on_succeed_update_matrix(self):
        print("\033[36m\nsucceed_update_matrix topic was broadcast")

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
    def test_do_update_no_data_package(self, mock_program_dao):
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

    @pytest.mark.integration
    def test_do_update_matrix_manager(self, test_program_dao):
        """do_update() should broadcast the 'succeed_update_matrix' on
        success."""
        pub.subscribe(self.on_succeed_update_matrix, 'succeed_update_matrix')

        DUT = mmFunction()

        DATAMGR = dmFunction()
        DATAMGR.do_connect(test_program_dao)

        HRDWRMGR = dmHardware()
        HRDWRMGR.do_connect(test_program_dao)

        def on_succeed_load_matrix(matrix_type, matrix):
            DUT.dic_matrices['fnctn_hrdwr'].loc[1, 'S1:SS2'] = 1

        pub.subscribe(on_succeed_load_matrix, 'succeed_load_matrix')

        pub.sendMessage('selected_revision', attributes={'revision_id': 1})
        pub.sendMessage('do_request_update_matrix',
                        matrix_type='fnctn_hrdwr')

        pub.unsubscribe(self.on_succeed_update_matrix, 'succeed_update_matrix')
        pub.unsubscribe(on_succeed_load_matrix, 'succeed_load_matrix')
