# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_fmea.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing FMEA algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amFMEA, dmFMEA
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import (
    RAMSTKAction,
    RAMSTKCause,
    RAMSTKControl,
    RAMSTKMechanism,
    RAMSTKMode,
)

ATTRIBUTES = {
    "type_id": 0,
    "total_part_count": 0,
    "availability_mission": 1.0,
    "cost": 0.0,
    "hazard_rate_mission": 0.0,
    "mpmt": 0.0,
    "hardware_id": 0,
    "mtbf_logistics": 0.0,
    "safety_critical": 0,
    "mmt": 0.0,
    "hazard_rate_logistics": 0.0,
    "remarks": "",
    "mtbf_mission": 0.0,
    "fmea_code": "PRESS-001",
    "name": "FMEA Name",
    "level": 0,
    "mttr": 0.0,
    "mcmt": 0.0,
    "availability_logistics": 1.0,
    "total_mode_count": 0,
}


@pytest.mark.usefixtures("test_program_dao", "test_toml_user_configuration")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_hardware(self):
        """__init__() should return a FMEA data manager."""
        DUT = dmFMEA()

        assert isinstance(DUT, dmFMEA)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "fmeas"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert not DUT._is_functional
        assert DUT.last_id == {
            "mode": 0,
            "mechanism": 0,
            "cause": 0,
            "control": 0,
            "action": 0,
        }
        assert pub.isSubscribed(DUT.do_select_all, "selected_hardware")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_fmea")
        assert pub.isSubscribed(DUT._do_insert_action, "request_insert_fmea_action")
        assert pub.isSubscribed(DUT._do_insert_cause, "request_insert_fmea_cause")
        assert pub.isSubscribed(DUT._do_insert_control, "request_insert_fmea_control")
        assert pub.isSubscribed(
            DUT._do_insert_mechanism, "request_insert_fmea_mechanism"
        )
        assert pub.isSubscribed(DUT._do_insert_mode, "request_insert_fmea_mode")
        assert pub.isSubscribed(DUT.do_update, "request_update_fmea")

    @pytest.mark.unit
    def test_data_manager_functional(self):
        """__init__() should return a FMEA data manager."""
        DUT = dmFMEA(functional=True)

        assert isinstance(DUT, dmFMEA)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "fmeas"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._is_functional

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the fmea analysis
        manager."""
        DUT = amFMEA(test_toml_user_configuration)

        assert isinstance(DUT, amFMEA)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_tree, "succeed_retrieve_hardware_fmea")
        assert pub.isSubscribed(
            DUT._do_calculate_criticality, "request_calculate_criticality"
        )
        assert pub.isSubscribed(DUT._do_calculate_rpn, "request_calculate_rpn")


@pytest.mark.usefixtures("test_program_dao", "test_toml_user_configuration")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_retrieve_functional_fmea(self, tree):
        assert isinstance(tree, Tree)
        # assert isinstance(tree.get_node('1').data['mode'], RAMSTKMode)
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast when "
            "selecting a functional FMEA."
        )

    def on_succeed_retrieve_hardware_fmea(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("4").data["mode"], RAMSTKMode)
        print(
            "\033[36m\nsucceed_retrieve_fmea topic was broadcast when "
            "selecting a hardware FMEA."
        )

    @pytest.mark.integration
    def test_do_select_all_functional(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMode, RAMSTKCause, RAMSTKControl, and RAMSTKAction instances on
        success."""
        pub.subscribe(
            self.on_succeed_retrieve_functional_fmea, "succeed_retrieve_functional_fmea"
        )

        DUT = dmFMEA(functional=True)
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "function_id": 1})

        pub.unsubscribe(
            self.on_succeed_retrieve_functional_fmea, "succeed_retrieve_functional_fmea"
        )

    @pytest.mark.integration
    def test_do_select_all_hardware(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMode, RAMSTKMechansim, RAMSTKCause, RAMSTKControl, and
        RAMSTKAction instances on success."""
        pub.subscribe(
            self.on_succeed_retrieve_hardware_fmea, "succeed_retrieve_hardware_fmea"
        )

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        pub.unsubscribe(
            self.on_succeed_retrieve_hardware_fmea, "succeed_retrieve_hardware_fmea"
        )

    @pytest.mark.integration
    def test_do_select_mode(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKMode on
        success."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = DUT.do_select("4", table="mode")

        assert isinstance(_mode, RAMSTKMode)
        assert _mode.effect_probability == 1.0
        assert _mode.mission == "Default Mission"

    @pytest.mark.integration
    def test_do_select_mechanism(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKMechanism on
        success."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mechanism = DUT.do_select("4.1", table="mechanism")

        assert isinstance(_mechanism, RAMSTKMechanism)
        assert _mechanism.pof_include == 1
        assert _mechanism.rpn_detection_new == 7

    @pytest.mark.integration
    def test_do_select_cause(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKCause on
        success."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _cause = DUT.do_select("4.1.1", table="cause")

        assert isinstance(_cause, RAMSTKCause)
        assert _cause.description == "Test Failure Cause #1 for Mechanism ID 1"
        assert _cause.rpn_detection_new == 1

    @pytest.mark.integration
    def test_do_select_control(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKControl on
        success."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _control = DUT.do_select("4.1.1.1.c", table="control")

        assert isinstance(_control, RAMSTKControl)
        assert _control.description == "Test FMEA Control #1 for Mode ID 4"
        assert _control.type_id == ""

    @pytest.mark.integration
    def test_do_select_action(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKAction on
        success."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _action = DUT.do_select("4.1.1.1.a", table="action")

        assert isinstance(_action, RAMSTKAction)
        assert _action.action_recommended == (
            "Test FMEA Recommended Action #1 " "for Cause ID 1."
        )
        assert _action.action_due_date == date(2019, 8, 20)

    @pytest.mark.integration
    def test_do_select_unknown_table(self, test_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        with pytest.raises(KeyError):
            DUT.do_select("4", table="scibbidy-bibbidy-doo")

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_program_dao):
        """do_select() should return None when a non-existent FMEA ID is
        requested."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        assert DUT.do_select(100, table="mode") is None


@pytest.mark.usefixtures("test_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete_mode(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_fmea topic was broadcast.")

    def on_succeed_delete_mechanism(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_fmea topic was broadcast.")

    def on_succeed_delete_cause(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_fmea topic was broadcast.")

    def on_succeed_delete_control(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_fmea topic was broadcast.")

    def on_succeed_delete_action(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_fmea topic was broadcast.")

    def on_fail_delete_action(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent FMEA record with "
            "hardware ID 300."
        )
        print("\033[35m\nfail_delete_action topic was broadcast.")

    def on_fail_delete_control(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent FMEA record with "
            "hardware ID 300."
        )
        print("\033[35m\nfail_delete_control topic was broadcast.")

    def on_fail_delete_cause(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent FMEA record with "
            "hardware ID 300."
        )
        print("\033[35m\nfail_delete_cause topic was broadcast.")

    def on_fail_delete_mechanism(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent FMEA record with "
            "hardware ID 300."
        )
        print("\033[35m\nfail_delete_mechanism topic was broadcast.")

    def on_fail_delete_mode(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent FMEA record with "
            "hardware ID 300."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete_action(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_action, "succeed_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("6.1.1.1.a")

        pub.unsubscribe(self.on_succeed_delete_action, "succeed_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_action_non_existent_id(self, test_program_dao):
        """_do_delete_action() should send the fail message."""
        pub.subscribe(self.on_fail_delete_action, "fail_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("300")

        pub.unsubscribe(self.on_fail_delete_action, "fail_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_control(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_control, "succeed_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("6.1.1.1.c")

        pub.unsubscribe(self.on_succeed_delete_control, "succeed_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_control_non_existent_id(self, test_program_dao):
        """_do_delete_control() should send the fail message."""
        pub.subscribe(self.on_fail_delete_control, "fail_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("300")

        pub.unsubscribe(self.on_fail_delete_control, "fail_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_cause(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_cause, "succeed_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("6.1.1")

        pub.unsubscribe(self.on_succeed_delete_cause, "succeed_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_cause_non_existent_id(self, test_program_dao):
        """_do_delete_cause() should send the fail message."""
        pub.subscribe(self.on_fail_delete_cause, "fail_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("300")

        pub.unsubscribe(self.on_fail_delete_cause, "fail_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_mechanism(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_mechanism, "succeed_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("6.1")

        pub.unsubscribe(self.on_succeed_delete_mechanism, "succeed_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_mechanism_non_existent_id(self, test_program_dao):
        """_do_delete_mechanism() should send the fail message."""
        pub.subscribe(self.on_fail_delete_mechanism, "fail_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("300")

        pub.unsubscribe(self.on_fail_delete_mechanism, "fail_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_mode(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_mode, "succeed_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("6")

        pub.unsubscribe(self.on_succeed_delete_mode, "succeed_delete_fmea")

    @pytest.mark.integration
    def test_do_delete_mode_non_existent_id(self, test_program_dao):
        """_do_delete_mode() should send the fail message."""
        pub.subscribe(self.on_fail_delete_mode, "fail_delete_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete("300")

        pub.unsubscribe(self.on_fail_delete_mode, "fail_delete_fmea")


@pytest.mark.usefixtures("test_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_mode(self, node_id, tree):
        assert node_id == "7"
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_mode topic was broadcast.")

    def on_fail_insert_mode(self, error_message):
        assert error_message == (
            "_do_insert_mode: Attempted to add a mode to non-existent parent "
            "FMEA record with hardware ID 40."
        )
        print("\033[35m\nfail_insert_mode topic was broadcast.")

    def on_succeed_insert_mechanism(self, node_id, tree):
        assert node_id == "6.2"
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_mechanism topic was broadcast.")

    def on_fail_insert_mechanism(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id, fld_hardware_id, "
            'fld_mode_id)=(1, 1, 40) is not present in table "ramstk_mode".'
        )
        print("\033[35m\nfail_insert_mechanism topic was broadcast.")

    def on_succeed_insert_cause(self, node_id, tree):
        assert node_id == "6.2.2"
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_cause topic was broadcast.")

    def on_fail_insert_cause(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id, fld_hardware_id, "
            "fld_mode_id, fld_mechanism_id)=(1, 1, 7, 40) is not present in "
            'table "ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_cause topic was broadcast.")

    def on_succeed_insert_control(self, node_id, tree):
        assert node_id == "6.2.2.2.c"
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_control topic was broadcast.")

    def on_fail_insert_control(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id, fld_hardware_id, "
            "fld_mode_id, fld_mechanism_id, fld_cause_id)=("
            '1, 1, 7, 6, 40) is not present in table "ramstk_cause".'
        )
        print("\033[35m\nfail_insert_control topic was broadcast.")

    def on_succeed_insert_action(self, node_id, tree):
        assert node_id == "6.2.2.2.a"
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_action topic was broadcast.")

    def on_fail_insert_action(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  "
            "Database returned:\n\tKey (fld_revision_id, fld_hardware_id, "
            "fld_mode_id, fld_mechanism_id, fld_cause_id)=("
            '1, 1, 7, 6, 40) is not present in table "ramstk_cause".'
        )
        print("\033[35m\nfail_insert_action topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_mode(self, test_program_dao):
        """_do_insert_mode() should send the success message after successfully
        inserting a failure mode."""
        pub.subscribe(self.on_succeed_insert_mode, "succeed_insert_mode")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_mode()

        assert isinstance(DUT.tree.get_node("7").data["mode"], RAMSTKMode)
        assert DUT.tree.get_node("7").data["mode"].mode_id == 7
        assert DUT.tree.get_node("7").data["mode"].description == "New Failure Mode"

        pub.unsubscribe(self.on_succeed_insert_mode, "succeed_insert_mode")

    @pytest.mark.integration
    def test_do_insert_mode_no_hardware(self, test_program_dao):
        """_do_insert_mode() should send the fail message if attempting to
        insert a failure mode for a non-existent hardware ID."""
        pub.subscribe(self.on_fail_insert_mode, "fail_insert_mode")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._root = 40
        DUT._do_insert_mode()

        pub.unsubscribe(self.on_fail_insert_mode, "fail_insert_mode")

    @pytest.mark.integration
    def test_do_insert_mechanism(self, test_program_dao):
        """_do_insert_mechanism() should send the success message after
        successfully inserting a failure mechanism."""
        pub.subscribe(self.on_succeed_insert_mechanism, "succeed_insert_mechanism")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_mechanism("6")

        assert isinstance(DUT.tree.get_node("6.2").data["mechanism"], RAMSTKMechanism)
        assert DUT.tree.get_node("6.2").data["mechanism"].mechanism_id == 2
        assert (
            DUT.tree.get_node("6.2").data["mechanism"].description
            == "New Failure Mechanism"
        )

        pub.unsubscribe(self.on_succeed_insert_mechanism, "succeed_insert_mechanism")

    @pytest.mark.integration
    def test_do_insert_mechanism_no_mode(self, test_program_dao):
        """do_insert() should send the fail message if attempting to add a
        mechanism to a non-existent mode ID."""
        pub.subscribe(self.on_fail_insert_mechanism, "fail_insert_mechanism")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_mechanism("40")

        pub.unsubscribe(self.on_fail_insert_mechanism, "fail_insert_mechanism")

    @pytest.mark.integration
    def test_do_insert_mechanism_bad_mode_id(self, test_program_dao):
        """do_insert() should send the fail message if attempting to add a
        mechanism using int mode ID."""
        pub.subscribe(self.on_fail_insert_mechanism, "fail_insert_mechanism")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_mechanism(40)

        pub.unsubscribe(self.on_fail_insert_mechanism, "fail_insert_mechanism")

    @pytest.mark.integration
    def test_do_insert_cause(self, test_program_dao):
        """_do_insert_cause() should send the success message after
        successfully inserting a failure cause."""
        pub.subscribe(self.on_succeed_insert_cause, "succeed_insert_cause")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_cause("6.2")

        assert isinstance(DUT.tree.get_node("6.2.2").data["cause"], RAMSTKCause)
        assert DUT.tree.get_node("6.2.2").data["cause"].cause_id == 2
        assert (
            DUT.tree.get_node("6.2.2").data["cause"].description == "New Failure Cause"
        )

        pub.unsubscribe(self.on_succeed_insert_cause, "succeed_insert_cause")

    @pytest.mark.integration
    def test_do_insert_cause_no_mechanism(self, test_program_dao):
        """_do_insert_cause() should send the fail message if attempting to add
        a cause to a non-existent mechanism ID."""
        pub.subscribe(self.on_fail_insert_cause, "fail_insert_cause")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_cause("7.40")

        pub.unsubscribe(self.on_fail_insert_cause, "fail_insert_cause")

    @pytest.mark.integration
    def test_do_insert_control(self, test_program_dao):
        """_do_insert_control() should send the success message after
        successfully inserting a control."""
        pub.subscribe(self.on_succeed_insert_control, "succeed_insert_control")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_control("6.2.2")

        assert isinstance(DUT.tree.get_node("6.2.2.2.c").data["control"], RAMSTKControl)
        assert DUT.tree.get_node("6.2.2.2.c").data["control"].control_id == 2
        assert DUT.tree.get_node("6.2.2.2.c").data["control"].description == (
            "New Control"
        )

        pub.unsubscribe(self.on_succeed_insert_control, "succeed_insert_control")

    @pytest.mark.integration
    def test_do_insert_control_no_cause(self, test_program_dao):
        """_do_insert_control() should send the fail message if attempting to
        add a control to a non-existent cause ID."""
        pub.subscribe(self.on_fail_insert_control, "fail_insert_control")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_mechanism("7")
        DUT._do_insert_cause("7.6")
        DUT._do_insert_control("7.6.40")

        pub.unsubscribe(self.on_fail_insert_control, "fail_insert_control")

    @pytest.mark.integration
    def test_do_insert_action(self, test_program_dao):
        """_do_insert_action() should send the success message after
        successfully inserting an action."""
        pub.subscribe(self.on_succeed_insert_action, "succeed_insert_action")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_action("6.2.2")

        assert isinstance(DUT.tree.get_node("6.2.2.2.a").data["action"], RAMSTKAction)
        assert DUT.tree.get_node("6.2.2.2.a").data["action"].action_id == 2
        assert DUT.tree.get_node("6.2.2.2.a").data["action"].action_recommended == (
            "Recommended Action"
        )

        pub.unsubscribe(self.on_succeed_insert_action, "succeed_insert_action")

    @pytest.mark.integration
    def test_do_insert_action_no_cause(self, test_program_dao):
        """_do_insert_action() should send the fail message if attempting to
        add an action to a non-existent cause ID."""
        pub.subscribe(self.on_fail_insert_action, "fail_insert_action")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_insert_mechanism("7")
        DUT._do_insert_action("7.6.40")

        pub.unsubscribe(self.on_fail_insert_action, "fail_insert_action")


@pytest.mark.usefixtures("test_program_dao", "test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_mode_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mode_id"] == 5
        assert attributes["description"] == "System Test Failure Mode #2"
        assert attributes["critical_item"] == 0
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_mechanism_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mechanism_id"] == 1
        assert attributes["description"] == (
            "Test Failure Mechanism #1 for " "Mode ID 5"
        )
        print("\033[36m\nsucceed_get_mechanism_attributes topic was broadcast.")

    def on_succeed_get_cause_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["cause_id"] == 1
        assert attributes["description"] == (
            "Test Failure Cause #1 for " "Mechanism ID 1"
        )
        print("\033[36m\nsucceed_get_cause_attributes topic was broadcast.")

    def on_succeed_get_control_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["control_id"] == 1
        assert attributes["description"] == ("Test FMEA Control #1 for Mode ID 4")
        print("\033[36m\nsucceed_get_control_attributes topic was broadcast.")

    def on_succeed_get_action_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["action_id"] == 1
        assert attributes["action_recommended"] == (
            "Test FMEA Recommended " "Action #1 for Cause ID 1."
        )
        print("\033[36m\nsucceed_get_action_attributes topic was broadcast.")

    def on_succeed_get_fmea_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("4").data["mode"], RAMSTKMode)
        assert isinstance(tree.get_node("4.1").data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_get_fmea_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_mode_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_mode_attrs, "succeed_get_mode_attributes")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_attributes("5", "mode")

        pub.unsubscribe(self.on_succeed_get_mode_attrs, "succeed_get_mode_attributes")

    @pytest.mark.integration
    def test_do_get_mechanism_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of mechanism attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_mechanism_attrs, "succeed_get_mechanism_attributes"
        )

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_attributes("5.1", "mechanism")

        pub.unsubscribe(
            self.on_succeed_get_mechanism_attrs, "succeed_get_mechanism_attributes"
        )

    @pytest.mark.integration
    def test_do_get_cause_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of cause attributes on
        success."""
        pub.subscribe(self.on_succeed_get_cause_attrs, "succeed_get_cause_attributes")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_attributes("4.1.1", "cause")

        pub.unsubscribe(self.on_succeed_get_cause_attrs, "succeed_get_cause_attributes")

    @pytest.mark.integration
    def test_do_get_control_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of control attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_control_attrs, "succeed_get_control_attributes"
        )

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_attributes("4.1.1.1.c", "control")

        pub.unsubscribe(
            self.on_succeed_get_control_attrs, "succeed_get_control_attributes"
        )

    @pytest.mark.integration
    def test_do_get_action_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of action attributes on
        success."""
        pub.subscribe(self.on_succeed_get_action_attrs, "succeed_get_action_attributes")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_attributes("4.1.1.1.a", "action")

        pub.unsubscribe(
            self.on_succeed_get_action_attrs, "succeed_get_action_attributes"
        )

    @pytest.mark.integration
    def test_do_set_mode_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        failure mode attributes."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.do_set_attributes(
            node_id=["4", -1],
            package={"effect_local": "Some really bad shit will happen."},
        )
        DUT.do_set_attributes(
            node_id=["4", -1], package={"description": "Ivanka Trump"}
        )
        assert DUT.do_select("4", table="mode").description == "Ivanka Trump"
        assert DUT.do_select("4", table="mode").effect_local == (
            "Some really bad shit will happen."
        )

        pub.unsubscribe(DUT.do_set_attributes, "request_set_fmea_attributes")

    @pytest.mark.integration
    def test_do_set_mechanism_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        failure mechanism attributes."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.do_set_attributes(node_id=["4.1", -1], package={"rpn_detection": 8})
        DUT.do_set_attributes(
            node_id=["4.1", -1], package={"description": "Jared Kushner"}
        )
        assert DUT.do_select("4.1", table="mechanism").description == "Jared Kushner"
        assert DUT.do_select("4.1", table="mechanism").rpn_detection == 8

        pub.unsubscribe(DUT.do_set_attributes, "request_set_fmea_attributes")

    @pytest.mark.integration
    def test_do_set_cause_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        failure cause attributes."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.do_set_attributes(node_id=["4.1.1", -1], package={"rpn_detection": 8})
        DUT.do_set_attributes(
            node_id=["4.1.1", -1], package={"description": "Jared Kushner"}
        )
        assert DUT.do_select("4.1.1", table="cause").description == "Jared Kushner"
        assert DUT.do_select("4.1.1", table="cause").rpn_detection == 8

        pub.unsubscribe(DUT.do_set_attributes, "request_set_fmea_attributes")

    @pytest.mark.integration
    def test_do_set_control_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        control attributes."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.do_set_attributes(
            node_id=["4.1.1.1.c", -1], package={"type_id": "Prevention"}
        )
        DUT.do_set_attributes(
            node_id=["4.1.1.1.c", -1], package={"description": "Lock and chain"}
        )
        assert (
            DUT.do_select("4.1.1.1.c", table="control").description == "Lock and chain"
        )
        assert DUT.do_select("4.1.1.1.c", table="control").type_id == "Prevention"

        pub.unsubscribe(DUT.do_set_attributes, "request_set_fmea_attributes")

    @pytest.mark.integration
    def test_do_set_action_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        action attributes."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.do_set_attributes(
            node_id=["4.1.1.1.a", -1], package={"action_recommended": "Kick his ass"}
        )
        DUT.do_set_attributes(
            node_id=["4.1.1.1.a", -1], package={"action_owner": "Doyle Rowland"}
        )
        assert (
            DUT.do_select("4.1.1.1.a", table="action").action_recommended
            == "Kick his ass"
        )
        assert (
            DUT.do_select("4.1.1.1.a", table="action").action_owner == "Doyle Rowland"
        )

        pub.unsubscribe(DUT.do_set_attributes, "request_set_fmea_attributes")

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_program_dao):
        """on_get_tree() should return the fmea treelib Tree."""
        pub.subscribe(self.on_succeed_get_fmea_tree, "succeed_get_fmea_tree")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_fmea_tree, "succeed_get_fmea_tree")

    @pytest.mark.integration
    def test_on_get_tree_analysis_manager(
        self, test_program_dao, test_toml_user_configuration
    ):
        """on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_fmea_tree message."""
        DATAMGR = dmFMEA()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT = amFMEA(test_toml_user_configuration)
        DATAMGR.do_get_tree()

        assert isinstance(DUT._tree, Tree)
        assert isinstance(DUT._tree.get_node("4").data["mode"], RAMSTKMode)


@pytest.mark.usefixtures("test_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_succeed_update_fmea(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_fmea topic was broadcast")

    def on_fail_update_fmea_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent FMEA record ID 100."
        )
        print("\033[35m\nfail_update_fmea topic was broadcast")

    def on_fail_update_fmea_no_data(self, error_message):
        assert error_message == (
            "do_update: No data package found for FMEA " "record ID 5."
        )
        print("\033[35m\nfail_update_fmea topic was broadcast")

    def on_fail_update_fmea_wrong_data_type(self, error_message):
        assert error_message == (
            "do_update: The value for one or more attributes for FMEA record "
            "ID 5 was the wrong type."
        )
        print("\033[35m\nfail_update_fmea topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_fmea, "succeed_update_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.tree.get_node("5").data["mode"].description = "Test failure mode"
        DUT.tree.get_node("5").data["mode"].operator_actions = "Take evasive actions."
        DUT.do_update("5")
        DUT.tree.get_node("5.1").data[
            "mechanism"
        ].description = "Test failure mechanism, updated"

        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        assert DUT.tree.get_node("5").data["mode"].description == ("Test failure mode")
        assert DUT.tree.get_node("5").data["mode"].operator_actions == (
            "Take evasive actions."
        )
        assert DUT.tree.get_node("5.1").data["mechanism"].description == (
            "Test failure mechanism, updated"
        )

        pub.unsubscribe(self.on_succeed_update_fmea, "succeed_update_fmea")

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_fmea_non_existent_id, "fail_update_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_fmea_non_existent_id, "fail_update_fmea")

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_fmea_no_data, "fail_update_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.tree.get_node("5").data.pop("mode")

        DUT.do_update("5")

        pub.unsubscribe(self.on_fail_update_fmea_no_data, "fail_update_fmea")

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_fmea_wrong_data_type, "fail_update_fmea")

        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = DUT.do_select("5", table="mode")
        _eff_prob = _mode.effect_probability
        _mode.effect_probability = {1: 2}

        DUT.do_update("5")

        _mode.effect_probability = _eff_prob

        pub.unsubscribe(self.on_fail_update_fmea_wrong_data_type, "fail_update_fmea")

    @pytest.mark.integration
    def test_do_update_wrong_data_type_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmFMEA()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = DUT.do_select("4", table="mode")
        _eff_prob = _mode.effect_probability
        _mode.effect_probability = {1: 2}

        DUT.do_update(0)

        _mode.effect_probability = _eff_prob


@pytest.mark.usefixtures("test_program_dao", "test_toml_user_configuration")
class TestAnalysisMethods:
    """Class for testing analytical methods."""

    def on_succeed_calculate_criticality(self, item_criticality):
        assert isinstance(item_criticality, dict)
        assert item_criticality["I"] == 0.00212865
        assert item_criticality["IV"] == 0.003085
        print("\033[36m\nsucceed_calculate_fmea_criticality topic was broadcast")

    def on_succeed_calculate_rpn(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_calculate_rpn topic was broadcast")

    @pytest.mark.integration
    def test_do_calculate_criticality(
        self, test_program_dao, test_toml_user_configuration
    ):
        """do_calculate_criticality() should calculate the criticality for all
        failure modes and the hardware item."""
        pub.subscribe(
            self.on_succeed_calculate_criticality, "succeed_calculate_fmea_criticality"
        )

        DATAMGR = dmFMEA()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT = amFMEA(test_toml_user_configuration)

        pub.sendMessage("request_get_fmea_tree")
        pub.sendMessage("request_calculate_criticality", item_hr=0.000617)

        assert DUT._tree.get_node("4").data["mode"].mode_hazard_rate == 0.0003085
        assert DUT._tree.get_node("4").data["mode"].mode_criticality == 0.003085

    @pytest.mark.integration
    def test_do_calculate_rpn_using_mechanism(
        self, test_program_dao, test_toml_user_configuration
    ):
        """do_calculate_rpn() should calculate the risk priority number (RPN)
        for all failure modes when using the mechanism for O and D values."""
        pub.subscribe(self.on_succeed_calculate_rpn, "succeed_calculate_rpn")

        DATAMGR = dmFMEA()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT = amFMEA(test_toml_user_configuration)

        pub.sendMessage("request_get_fmea_tree")
        pub.sendMessage("request_calculate_rpn")

        assert DUT._tree.get_node("4.1").data["mechanism"].rpn == 16
        assert DUT._tree.get_node("5.1").data["mechanism"].rpn == 8
        assert DUT._tree.get_node("4.1").data["mechanism"].rpn_new == 14
        assert DUT._tree.get_node("5.1").data["mechanism"].rpn_new == 20

    # Add this to the integration suite when adding the functional FMEA.
    @pytest.mark.skip
    def test_do_calculate_rpn_using_cause(
        self, test_program_dao, test_toml_user_configuration
    ):
        """do_calculate_rpn() should calculate the risk priority number (RPN)
        for all failure modes when using the cause for O and D values."""
        DATAMGR = dmFMEA(functional=True)
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all({"revision_id": 1, "function_id": 1})
        DUT = amFMEA(test_toml_user_configuration)

        pub.sendMessage("request_get_fmea_tree")
        pub.sendMessage("request_calculate_rpn", method="cause")

        assert DUT._tree.get_node("1.4").data["cause"].rpn == 16
        assert DUT._tree.get_node("1.5").data["cause"].rpn == 14
        assert DUT._tree.get_node("1.6").data["cause"].rpn == 16
        assert DUT._tree.get_node("1.4").data["cause"].rpn_new == 5
        assert DUT._tree.get_node("1.5").data["cause"].rpn_new == 8
        assert DUT._tree.get_node("1.6").data["cause"].rpn_new == 9

        pub.unsubscribe(self.on_succeed_calculate_rpn, "succeed_calculate_rpn")
