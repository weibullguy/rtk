# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.hazards.hazards_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hazards module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmHazards


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == ('_do_insert_hazard: A database error '
                                 'occurred when attempting to add a child '
                                 'function to parent function ID 1.')
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    def on_fail_insert_no_function(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.integration
    def test_insert_no_revision(self, test_program_dao):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_revision, 'fail_insert_hazard')

        DUT = dmHazards()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.revision_id = 40
        DUT._do_insert_hazard(parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_revision, 'fail_insert_hazard')

    @pytest.mark.integration
    def test_insert_no_function(self, test_program_dao):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_function, 'fail_insert_hazard')

        DUT = dmHazards()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.function_id = 40
        DUT._do_insert_hazard(parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_function, 'fail_insert_hazard')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data['hazard'].potential_hazard == 'Big Hazard'
        print("\033[36m\nsucceed_update_hazard topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for hazard ID 1 '
            'was the wrong type.')
        print("\033[35m\nfail_update_hazard topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        DUT.tree.get_node(1).data['hazard'].potential_hazard = 'Big Hazard'
        DUT.do_update(1, 'hazard')

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_hazard')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        DUT = dmHazards()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        DUT.tree.get_node(
            1).data['hazard'].potential_hazard = 'Big test hazard'

        pub.sendMessage('request_update_all_functions')

        assert DUT.tree.get_node(
            1).data['hazard'].potential_hazard == 'Big test hazard'

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.tree.get_node(1).data['hazard'].assembly_effect = {1: 'What?'}

        DUT.do_update(1, 'hazard')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_hazard')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        DUT = dmHazards()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.tree.get_node(1).data['hazard'].assembly_effect = {1: 'What?'}

        DUT.do_update(0, 'hazard')
