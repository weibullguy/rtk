# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.opstress.opstress_integration_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOpStress


@pytest.mark.usefixtures("test_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id, fld_load_id)=(1, 1, 6, 1, 100) is not present in table "
            '"ramstk_op_load".'
        )
        print("\033[35m\nfail_insert_opstress topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id, fld_load_id)=(10, 1, 6, 1, 1) is not present in table "
            '"ramstk_op_load".'
        )
        print("\033[35m\nfail_insert_opstress topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_parent(self, test_program_dao):
        """_do_insert_opstress() should send the fail message if attempting to
        add an operating load to a non-existent opstress ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_opstress")

        DUT = dmOpStress()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT._parent_id = 100
        DUT._do_insert_opstress(100)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_opstress")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """_do_insert_opstress() should send the success message after
        successfully inserting an operating stress."""
        pub.subscribe(self.on_fail_insert_no_revision, "fail_insert_opstress")

        DUT = dmOpStress()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT._revision_id = 10
        DUT._do_insert_opstress(1)

        pub.unsubscribe(self.on_fail_insert_no_revision, "fail_insert_opstress")


@pytest.mark.usefixtures("test_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["opstress"].description == ("Big test opstress.")
        assert tree.get_node(1).data["opstress"].load_history == (
            "Big test load history."
        )
        print("\033[36m\nsucceed_update_opstress topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for opstress ID 1 was "
            "the wrong type."
        )
        print("\033[35m\nfail_update_opstress topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, "succeed_update_opstress")

        DUT = dmOpStress()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        DUT.tree.get_node(1).data["opstress"].description = "Big test opstress."
        DUT.tree.get_node(1).data["opstress"].load_history = "Big test load history."
        DUT.do_update(1, table="opstress")

        pub.unsubscribe(self.on_succeed_update, "succeed_update_opstress")

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should broadcast the succeed message on success."""
        DUT = dmOpStress()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        pub.sendMessage("request_update_all_opstresss")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type, "fail_update_opstress")

        DUT = dmOpStress()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        _opstress = DUT.do_select(1, table="opstress")
        _opstress.rpn_detection = {1: 2}

        DUT.do_update(1, table="opstress")

        pub.unsubscribe(self.on_fail_update_wrong_data_type, "fail_update_opstress")

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmOpStress()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        _opstress = DUT.do_select(1, table="opstress")
        _opstress.rpn_detection_new = {1: 2}

        DUT.do_update(0, table="opstress")
