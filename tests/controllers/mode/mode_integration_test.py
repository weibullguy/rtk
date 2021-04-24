# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mode.mode_integration_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Mode integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMode


@pytest.mark.usefixtures("test_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id)=(1, 100) is not "
            'present in table "ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_mechanism topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a "
            "record.  Database returned:\n\tKey (fld_revision_id, "
            "fld_hardware_id)=(4, 1) is not present in table "
            '"ramstk_hardware".'
        )
        print("\033[35m\nfail_insert_opstress topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_program_dao):
        """_do_insert_mechanism() should send the fail message if attempting to
        add an operating load to a non-existent mechanism ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_mode")

        DUT = dmMode()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._parent_id = 100
        DUT._do_insert_mode()

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_mode")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """_do_insert_mode() should send the fail message if attempting to add
        a mode to a non-existent Revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_mode")

        DUT = dmMode()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._revision_id = 4
        DUT._do_insert_mode()

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_mode")


@pytest.mark.usefixtures("test_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(4).data["mode"].description == ("Test failure mode")
        assert tree.get_node(4).data["mode"].operator_actions == (
            "Take evasive actions."
        )
        print("\033[36m\nsucceed_update_mode topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for mode ID 4 was the "
            "wrong type."
        )
        print("\033[35m\nfail_update_mode topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_mode")

        DUT = dmMode()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.tree.get_node(4).data["mode"].description = "Test failure mode"
        DUT.tree.get_node(4).data["mode"].operator_actions = "Take evasive actions."
        DUT.do_update(4, table="mode")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_mode")

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should broadcast the succeed message on success."""
        DUT = dmMode()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        pub.sendMessage("request_update_all_modes")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_mode")

        DUT = dmMode()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = DUT.do_select(4, table="mode")
        _mode.mode_criticality = {1: 2}

        DUT.do_update(4, table="mode")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_mode")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmMode()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = DUT.do_select(4, table="mode")
        _mode.mode_criticality = {1: 2}

        DUT.do_update(0, table="mode")
