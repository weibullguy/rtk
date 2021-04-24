# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_mode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing PoF algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMode
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMode


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mode_1 = RAMSTKMode()
    _mode_1.revision_id = 1
    _mode_1.hardware_id = 1
    _mode_1.mode_id = 1
    _mode_1.effect_local = ""
    _mode_1.mission = "Default Mission"
    _mode_1.other_indications = ""
    _mode_1.mode_criticality = 0.0
    _mode_1.single_point = 0
    _mode_1.design_provisions = ""
    _mode_1.type_id = 0
    _mode_1.rpn_severity_new = 1
    _mode_1.effect_next = ""
    _mode_1.detection_method = ""
    _mode_1.operator_actions = ""
    _mode_1.critical_item = 0
    _mode_1.hazard_rate_source = ""
    _mode_1.severity_class = ""
    _mode_1.description = "Test Failure Mode #1"
    _mode_1.mission_phase = ""
    _mode_1.mode_probability = ""
    _mode_1.remarks = ""
    _mode_1.mode_ratio = 0.0
    _mode_1.mode_hazard_rate = 0.0
    _mode_1.rpn_severity = 1
    _mode_1.isolation_method = ""
    _mode_1.effect_end = ""
    _mode_1.mode_op_time = 0.0
    _mode_1.effect_probability = 0.8

    _mode_2 = RAMSTKMode()
    _mode_2.revision_id = 1
    _mode_2.hardware_id = 1
    _mode_2.mode_id = 2
    _mode_2.effect_local = ""
    _mode_2.mission = "Default Mission"
    _mode_2.other_indications = ""
    _mode_2.mode_criticality = 0.0
    _mode_2.single_point = 0
    _mode_2.design_provisions = ""
    _mode_2.type_id = 0
    _mode_2.rpn_severity_new = 1
    _mode_2.effect_next = ""
    _mode_2.detection_method = ""
    _mode_2.operator_actions = ""
    _mode_2.critical_item = 0
    _mode_2.hazard_rate_source = ""
    _mode_2.severity_class = ""
    _mode_2.description = "Test Failure Mode #2"
    _mode_2.mission_phase = ""
    _mode_2.mode_probability = ""
    _mode_2.remarks = ""
    _mode_2.mode_ratio = 0.0
    _mode_2.mode_hazard_rate = 0.0
    _mode_2.rpn_severity = 1
    _mode_2.isolation_method = ""
    _mode_2.effect_end = ""
    _mode_2.mode_op_time = 0.0
    _mode_2.effect_probability = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mode_1,
        _mode_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmMode()

        assert isinstance(DUT, dmMode)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "modes"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_mode_attributes")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_mode_tree")
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_mode")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_modes")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_mode")
        assert pub.isSubscribed(DUT._do_insert_mode, "request_insert_mode")


@pytest.mark.usefixtures("mock_program_dao")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mode"], RAMSTKMode)
        print("\033[36m\nsucceed_retrieve_mode topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMode, RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and
        RAMSTKTestMethod instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_modes")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_modes")

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object when the tree is
        already populated."""
        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_modes")

        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_modes")

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKMode on
        success."""
        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        _mode = DUT.do_select(1, table="mode")

        assert isinstance(_mode, RAMSTKMode)
        assert _mode.effect_probability == 0.8
        assert _mode.description == "Test Failure Mode #1"

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        with pytest.raises(KeyError):
            DUT.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent PoF ID is
        requested."""
        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        assert DUT.do_select(100, table="mode") is None


@pytest.mark.usefixtures("mock_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mode topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mode ID 300."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mode ID 2."
        )
        print("\033[35m\nfail_delete_mode topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete(4)

        assert DUT.tree.get_node(4) is None

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mode")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mode")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mode")


@pytest.mark.usefixtures("mock_program_dao")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mode_id"] == 2
        assert attributes["description"] == "Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mode"], RAMSTKMode)
        assert isinstance(tree.get_node(2).data["mode"], RAMSTKMode)
        print("\033[36m\nsucceed_get_mode_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_attributes(2, "mode")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT.do_set_attributes(
            node_id=[1, -1], package={"detection_method": "Test detection method."}
        )
        DUT.do_set_attributes(node_id=[1, -1], package={"description": "Jared Kushner"})
        assert DUT.do_select(1, table="mode").description == "Jared Kushner"
        assert (
            DUT.do_select(1, table="mode").detection_method == "Test detection method."
        )

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_mode_tree")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree, "succeed_get_mode_tree")


@pytest.mark.usefixtures("mock_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["mode"], RAMSTKMode)
        assert tree.get_node(3).data["mode"].mode_id == 3
        assert tree.get_node(3).data["mode"].description is None
        print("\033[36m\nsucceed_insert_mode topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == (
            "An error occurred when attempting to add a "
            "test method to operating load ID 40."
        )
        print("\033[35m\nfail_insert_mode topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})

        DUT._do_insert_mode()

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mode")

    @pytest.mark.unit
    def test_do_insert_no_parent(self, mock_program_dao):
        """_do_insert_opload() should send the fail message if attempting to
        add an operating load to a non-existent mechanism ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT._parent_id = 4
        DUT._do_insert_mode()

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_mode")


@pytest.mark.usefixtures("mock_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent mode with mode ID 100."
        )
        print("\033[35m\nfail_update_mode topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for mode ID 1.")
        print("\033[35m\nfail_update_mode topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a PoF ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.do_update(100, table="mode")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_mode")

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_mode")

        DUT = dmMode()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1})
        DUT.tree.get_node(1).data.pop("mode")

        DUT.do_update(1, table="mode")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_mode")
