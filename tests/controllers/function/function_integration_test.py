# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.function.function_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing function module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFunction


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == ('_do_insert_function: A database error '
                                 'occurred when attempting to add a child '
                                 'function to parent function ID 1.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_revision, 'fail_insert_function')

        DUT = dmFunction()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 40
        DUT._do_insert_function(parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_function')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_function topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == ('do_update: The value for one or more '
                                 'attributes for function ID 1 was the wrong '
                                 'type.')
        print("\033[35m\nfail_update_function topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_function')

        DUT = dmFunction()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.tree.get_node(1).data['function'].name = 'Test Function'
        DUT.do_update(1, 'function')

        DUT.do_select_all(attributes={'revision_id': 1})
        assert DUT.tree.get_node(1).data['function'].name == 'Test Function'

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_function')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should update all the functions in the database."""
        DUT = dmFunction()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _function = DUT.do_select(1, table='function')
        _function.name = 'Big test function #1'
        _function = DUT.do_select(2, table='function')
        _function.name = 'Big test function #2'

        pub.sendMessage('request_update_all_functions')

        _function = DUT.do_select(1, table='function')
        assert _function.name == 'Big test function #1'

        _function = DUT.do_select(2, table='function')
        assert _function.name == 'Big test function #2'

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_function')

        DUT = dmFunction()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data['function'].name = {1: 1.56}

        DUT.do_update(1, 'function')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_function')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        DUT = dmFunction()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data['function'].name = {1: 1.56}

        DUT.do_update(0, 'function')
