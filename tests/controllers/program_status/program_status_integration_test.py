# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.program_status.program_status_integration_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Program Status module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmProgramStatus


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            'do_insert: Database error when attempting to add a record.  '
            'Database returned:\n\tKey (fld_revision_id)=(30) is not present '
            'in table "ramstk_revision".')
        print("\033[35m\nfail_insert_program_status topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """_do_insert_program_status() should send the fail message if
        attempting to add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_revision,
                      'fail_insert_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 30
        DUT._do_insert_program_status()

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_program_status')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(
            1).data['program_status'].cost_remaining == 47832.00
        assert tree.get_node(1).data['program_status'].time_remaining == 528.3
        print("\033[36m\nsucceed_update_program_status topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for program '
            'status ID 1 was the wrong type.')
        print("\033[35m\nfail_update_program_status topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """_do_update_program_status() should broadcast the
        'succeed_update_program_status' message on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.tree.get_node(1).data['program_status'].cost_remaining = 47832.00
        DUT.tree.get_node(1).data['program_status'].time_remaining = 528.3

        DUT.do_update(1, table='program_status')

        pub.unsubscribe(self.on_succeed_update,
                        'succeed_update_program_status')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should update all the functions in the database."""
        DUT = dmProgramStatus()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.tree.get_node(1).data['program_status'].cost_remaining = 2.00
        DUT.tree.get_node(1).data['program_status'].time_remaining = 8.3

        DUT.do_update_all()

        assert DUT.tree.get_node(
            1).data['program_status'].cost_remaining == 2.00
        assert DUT.tree.get_node(
            1).data['program_status'].time_remaining == 8.3

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a Status
        ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_program_status')

        DUT = dmProgramStatus()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _status = DUT.do_select(1, table='program_status')
        _status.time_remaining = {1: 2}

        DUT.do_update(1, table='program_status')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_program_status')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed the root
        ID."""
        DUT = dmProgramStatus()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _status = DUT.do_select(1, table='program_status')
        _status.time_remaining = {1: 2}

        DUT.do_update(0, table='program_status')
