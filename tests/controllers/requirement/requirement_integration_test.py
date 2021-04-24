# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.requirement.requirement_integration_test.py is part
#       of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Requirement module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRequirement


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            '_do_insert_requirement: Attempted to insert child requirement '
            'under non-existent requirement ID 32.')
        print("\033[35m\nfail_insert_requirement topic was broadcast")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new top-level requirement."""
        pub.subscribe(self.on_fail_insert_no_revision,
                      'fail_insert_requirement')

        DUT = dmRequirement()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 40
        DUT._do_insert_requirement(parent_id=1)

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_requirement')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(
            1).data['requirement'].description == 'Test Requirement'
        print("\033[36m\nsucceed_update_requirement topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for requirement '
            'ID 1 was the wrong type.')
        print("\033[35m\nfail_update_requirement topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _requirement = DUT.do_select(1, table='requirement')
        _requirement.description = 'Test Requirement'
        DUT.do_update(1, table='requirement')

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_requirement')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should update all the functions in the database."""
        DUT = dmRequirement()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _requirement = DUT.do_select(1, table='requirement')
        _requirement.description = 'Big test requirement #1'
        _requirement = DUT.do_select(2, table='requirement')
        _requirement.description = 'Big test requirement #2'

        pub.sendMessage('request_update_all_requirements')

        assert DUT.do_select(
            1, table='requirement').description == 'Big test requirement #1'
        assert DUT.do_select(
            2, table='requirement').description == 'Big test requirement #2'

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_requirement')

        DUT = dmRequirement()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _requirement = DUT.do_select(1, table='requirement')
        _requirement.priority = {1: 2}

        DUT.do_update(1, table='requirement')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_requirement')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmRequirement()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _requirement = DUT.do_select(1, table='requirement')
        _requirement.priority = {1: 2}

        DUT.do_update(0, table='requirement')
