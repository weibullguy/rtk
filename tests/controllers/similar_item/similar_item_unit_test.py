# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.similar_item.similar_item_unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amSimilarItem, dmSimilarItem
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKSimilarItem


@pytest.fixture
def mock_program_dao(monkeypatch):
    _similar_item_1 = RAMSTKSimilarItem()
    _similar_item_1.revision_id = 1
    _similar_item_1.hardware_id = 1
    _similar_item_1.change_description_1 = ""
    _similar_item_1.change_description_2 = ""
    _similar_item_1.change_description_3 = ""
    _similar_item_1.change_description_4 = ""
    _similar_item_1.change_description_5 = ""
    _similar_item_1.change_description_6 = ""
    _similar_item_1.change_description_7 = ""
    _similar_item_1.change_description_8 = ""
    _similar_item_1.change_description_9 = ""
    _similar_item_1.change_description_10 = ""
    _similar_item_1.change_factor_1 = 1.0
    _similar_item_1.change_factor_2 = 1.0
    _similar_item_1.change_factor_3 = 1.0
    _similar_item_1.change_factor_4 = 1.0
    _similar_item_1.change_factor_5 = 1.0
    _similar_item_1.change_factor_6 = 1.0
    _similar_item_1.change_factor_7 = 1.0
    _similar_item_1.change_factor_8 = 1.0
    _similar_item_1.change_factor_9 = 1.0
    _similar_item_1.change_factor_10 = 1.0
    _similar_item_1.environment_from_id = 0
    _similar_item_1.environment_to_id = 0
    _similar_item_1.function_1 = "0"
    _similar_item_1.function_2 = "0"
    _similar_item_1.function_3 = "0"
    _similar_item_1.function_4 = "0"
    _similar_item_1.function_5 = "0"
    _similar_item_1.parent_id = 0
    _similar_item_1.similar_item_method_id = 1
    _similar_item_1.quality_from_id = 0
    _similar_item_1.quality_to_id = 0
    _similar_item_1.result_1 = 0.0
    _similar_item_1.result_2 = 0.0
    _similar_item_1.result_3 = 0.0
    _similar_item_1.result_4 = 0.0
    _similar_item_1.result_5 = 0.0
    _similar_item_1.temperature_from = 30.0
    _similar_item_1.temperature_to = 30.0
    _similar_item_1.user_blob_1 = ""
    _similar_item_1.user_blob_2 = ""
    _similar_item_1.user_blob_3 = ""
    _similar_item_1.user_blob_4 = ""
    _similar_item_1.user_blob_5 = ""
    _similar_item_1.user_float_1 = 0.0
    _similar_item_1.user_float_2 = 0.0
    _similar_item_1.user_float_3 = 0.0
    _similar_item_1.user_float_4 = 0.0
    _similar_item_1.user_float_5 = 0.0
    _similar_item_1.user_int_1 = 0
    _similar_item_1.user_int_2 = 0
    _similar_item_1.user_int_3 = 0
    _similar_item_1.user_int_4 = 0
    _similar_item_1.user_int_5 = 0

    _similar_item_2 = RAMSTKSimilarItem()
    _similar_item_2.revision_id = 1
    _similar_item_2.hardware_id = 2
    _similar_item_2.change_description_1 = ""
    _similar_item_2.change_description_2 = ""
    _similar_item_2.change_description_3 = ""
    _similar_item_2.change_description_4 = ""
    _similar_item_2.change_description_5 = ""
    _similar_item_2.change_description_6 = ""
    _similar_item_2.change_description_7 = ""
    _similar_item_2.change_description_8 = ""
    _similar_item_2.change_description_9 = ""
    _similar_item_2.change_description_10 = ""
    _similar_item_2.change_factor_1 = 1.0
    _similar_item_2.change_factor_2 = 1.0
    _similar_item_2.change_factor_3 = 1.0
    _similar_item_2.change_factor_4 = 1.0
    _similar_item_2.change_factor_5 = 1.0
    _similar_item_2.change_factor_6 = 1.0
    _similar_item_2.change_factor_7 = 1.0
    _similar_item_2.change_factor_8 = 1.0
    _similar_item_2.change_factor_9 = 1.0
    _similar_item_2.change_factor_10 = 1.0
    _similar_item_2.environment_from_id = 0
    _similar_item_2.environment_to_id = 0
    _similar_item_2.function_1 = "0"
    _similar_item_2.function_2 = "0"
    _similar_item_2.function_3 = "0"
    _similar_item_2.function_4 = "0"
    _similar_item_2.function_5 = "0"
    _similar_item_2.parent_id = 1
    _similar_item_2.similar_item_method_id = 1
    _similar_item_2.quality_from_id = 0
    _similar_item_2.quality_to_id = 0
    _similar_item_2.result_1 = 0.0
    _similar_item_2.result_2 = 0.0
    _similar_item_2.result_3 = 0.0
    _similar_item_2.result_4 = 0.0
    _similar_item_2.result_5 = 0.0
    _similar_item_2.temperature_from = 30.0
    _similar_item_2.temperature_to = 30.0
    _similar_item_2.user_blob_1 = ""
    _similar_item_2.user_blob_2 = ""
    _similar_item_2.user_blob_3 = ""
    _similar_item_2.user_blob_4 = ""
    _similar_item_2.user_blob_5 = ""
    _similar_item_2.user_float_1 = 0.0
    _similar_item_2.user_float_2 = 0.0
    _similar_item_2.user_float_3 = 0.0
    _similar_item_2.user_float_4 = 0.0
    _similar_item_2.user_float_5 = 0.0
    _similar_item_2.user_int_1 = 0
    _similar_item_2.user_int_2 = 0
    _similar_item_2.user_int_3 = 0
    _similar_item_2.user_int_4 = 0
    _similar_item_2.user_int_5 = 0

    _similar_item_3 = RAMSTKSimilarItem()
    _similar_item_3.revision_id = 1
    _similar_item_3.hardware_id = 3
    _similar_item_3.change_description_1 = ""
    _similar_item_3.change_description_2 = ""
    _similar_item_3.change_description_3 = ""
    _similar_item_3.change_description_4 = ""
    _similar_item_3.change_description_5 = ""
    _similar_item_3.change_description_6 = ""
    _similar_item_3.change_description_7 = ""
    _similar_item_3.change_description_8 = ""
    _similar_item_3.change_description_9 = ""
    _similar_item_3.change_description_10 = ""
    _similar_item_3.change_factor_1 = 1.0
    _similar_item_3.change_factor_2 = 1.0
    _similar_item_3.change_factor_3 = 1.0
    _similar_item_3.change_factor_4 = 1.0
    _similar_item_3.change_factor_5 = 1.0
    _similar_item_3.change_factor_6 = 1.0
    _similar_item_3.change_factor_7 = 1.0
    _similar_item_3.change_factor_8 = 1.0
    _similar_item_3.change_factor_9 = 1.0
    _similar_item_3.change_factor_10 = 1.0
    _similar_item_3.environment_from_id = 0
    _similar_item_3.environment_to_id = 0
    _similar_item_3.function_1 = "0"
    _similar_item_3.function_2 = "0"
    _similar_item_3.function_3 = "0"
    _similar_item_3.function_4 = "0"
    _similar_item_3.function_5 = "0"
    _similar_item_3.parent_id = 2
    _similar_item_3.similar_item_method_id = 1
    _similar_item_3.quality_from_id = 0
    _similar_item_3.quality_to_id = 0
    _similar_item_3.result_1 = 0.0
    _similar_item_3.result_2 = 0.0
    _similar_item_3.result_3 = 0.0
    _similar_item_3.result_4 = 0.0
    _similar_item_3.result_5 = 0.0
    _similar_item_3.temperature_from = 30.0
    _similar_item_3.temperature_to = 30.0
    _similar_item_3.user_blob_1 = ""
    _similar_item_3.user_blob_2 = ""
    _similar_item_3.user_blob_3 = ""
    _similar_item_3.user_blob_4 = ""
    _similar_item_3.user_blob_5 = ""
    _similar_item_3.user_float_1 = 0.0
    _similar_item_3.user_float_2 = 0.0
    _similar_item_3.user_float_3 = 0.0
    _similar_item_3.user_float_4 = 0.0
    _similar_item_3.user_float_5 = 0.0
    _similar_item_3.user_int_1 = 0
    _similar_item_3.user_int_2 = 0
    _similar_item_3.user_int_3 = 0
    _similar_item_3.user_int_4 = 0
    _similar_item_3.user_int_5 = 0

    DAO = MockDAO()
    DAO.table = [
        _similar_item_1,
        _similar_item_2,
        _similar_item_3,
    ]

    yield DAO


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Hardware data manager."""
        DUT = dmSimilarItem()

        assert isinstance(DUT, dmSimilarItem)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "similar_items"
        assert DUT._root == 0
        assert DUT._pkey == {"similar_item": ["revision_id", "hardware_id"]}
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_similar_item_attributes"
        )
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_similar_item_attributes"
        )
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_similar_item")
        assert pub.isSubscribed(DUT.do_set_tree, "succeed_calculate_similar_item")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_similar_items")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_similar_item_tree")
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_similar_item")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_hardware")
        assert pub.isSubscribed(
            DUT._do_insert_similar_item, "request_insert_similar_item"
        )

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the hardware analysis
        manager."""
        DUT = amSimilarItem(test_toml_user_configuration)

        assert isinstance(DUT, amSimilarItem)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert DUT._dic_hardware_hrs == {}
        assert pub.isSubscribed(
            DUT.on_get_all_attributes, "succeed_get_similar_item_attributes"
        )
        assert pub.isSubscribed(DUT.on_get_tree, "succeed_get_similar_item_tree")
        assert pub.isSubscribed(DUT.on_get_tree, "succeed_retrieve_similar_item")
        assert pub.isSubscribed(DUT.on_get_tree, "succeed_update_similar_item")
        assert pub.isSubscribed(
            DUT._do_calculate_similar_item, "request_calculate_similar_item"
        )
        assert pub.isSubscribed(
            DUT._do_roll_up_change_descriptions, "request_roll_up_change_descriptions"
        )
        assert pub.isSubscribed(
            DUT._on_get_hardware_attributes, "succeed_get_hardwares_tree"
        )


@pytest.mark.usefixtures("mock_program_dao", "test_toml_user_configuration")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["similar_item"], RAMSTKSimilarItem)
        print("\033[36m\nsucceed_retrieve_similar_item topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKHardware instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear nodes from an existing allocation
        tree."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_similar_item")

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKSimilarItem on
        success."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        _similar_item = DUT.do_select(1, table="similar_item")

        assert isinstance(_similar_item, RAMSTKSimilarItem)
        assert _similar_item.change_description_1 == ""
        assert _similar_item.temperature_from == 30.0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Hardware ID is
        requested."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        assert DUT.do_select(100, table="hardware") is None


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_similar_item topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent similar item "
            "record with hardware ID 300."
        )
        print("\033[35m\nfail_delete_similar_item topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent similar item record "
            "with hardware ID 2."
        )
        print("\033[35m\nfail_delete_similar_item topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        pub.sendMessage("request_delete_hardware", node_id=DUT.last_id)

        assert DUT.last_id == 2

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_similar_item")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        pub.sendMessage("request_delete_hardware", node_id=300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_similar_item")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_similar_item")


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["change_description_1"] == ""
        assert attributes["change_description_2"] == ""
        assert attributes["change_description_3"] == ""
        assert attributes["change_description_4"] == ""
        assert attributes["change_description_5"] == ""
        assert attributes["change_description_6"] == ""
        assert attributes["change_description_7"] == ""
        assert attributes["change_description_8"] == ""
        assert attributes["change_description_9"] == ""
        assert attributes["change_description_10"] == ""
        assert attributes["change_factor_1"] == 1.0
        assert attributes["change_factor_2"] == 1.0
        assert attributes["change_factor_3"] == 1.0
        assert attributes["change_factor_4"] == 1.0
        assert attributes["change_factor_5"] == 1.0
        assert attributes["change_factor_6"] == 1.0
        assert attributes["change_factor_7"] == 1.0
        assert attributes["change_factor_8"] == 1.0
        assert attributes["change_factor_9"] == 1.0
        assert attributes["change_factor_10"] == 1.0
        assert attributes["environment_from_id"] == 0
        assert attributes["environment_to_id"] == 0
        assert attributes["function_1"] == "0"
        assert attributes["function_2"] == "0"
        assert attributes["function_3"] == "0"
        assert attributes["function_4"] == "0"
        assert attributes["function_5"] == "0"
        assert attributes["parent_id"] == 1
        assert attributes["similar_item_method_id"] == 1
        assert attributes["quality_from_id"] == 0
        assert attributes["quality_to_id"] == 0
        assert attributes["result_1"] == 0.0
        assert attributes["result_2"] == 0.0
        assert attributes["result_3"] == 0.0
        assert attributes["result_4"] == 0.0
        assert attributes["result_5"] == 0.0
        assert attributes["temperature_from"] == 30.0
        assert attributes["temperature_to"] == 30.0
        assert attributes["user_blob_1"] == ""
        assert attributes["user_blob_2"] == ""
        assert attributes["user_blob_3"] == ""
        assert attributes["user_blob_4"] == ""
        assert attributes["user_blob_5"] == ""
        assert attributes["user_float_1"] == 0.0
        assert attributes["user_float_2"] == 0.0
        assert attributes["user_float_3"] == 0.0
        assert attributes["user_float_4"] == 0.0
        assert attributes["user_float_5"] == 0.0
        assert attributes["user_int_1"] == 0
        assert attributes["user_int_2"] == 0
        assert attributes["user_int_3"] == 0
        assert attributes["user_int_4"] == 0
        assert attributes["user_int_5"] == 0
        print("\033[36m\nsucceed_get_similar_item_attributes topic was " "broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["similar_item"], RAMSTKSimilarItem)
        print("\033[36m\nsucceed_get_similar_item_tree topic was broadcast.")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of hardware attributes on
        success."""
        pub.subscribe(
            self.on_succeed_get_attributes, "succeed_get_similar_item_attributes"
        )

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        DUT.do_get_attributes(
            node_id=2,
            table="similar_item",
        )

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_similar_item_attributes"
        )

    @pytest.mark.unit
    def test_on_get_attributes(self, mock_program_dao, test_toml_user_configuration):
        """_get_all_attributes() should update the attributes dict on
        success."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1})
        DATAMGR.do_get_attributes(node_id=2, table="similar_item")

        assert DUT._attributes["hardware_id"] == 2
        assert DUT._attributes["change_description_1"] == ""
        assert DUT._attributes["change_description_2"] == ""
        assert DUT._attributes["change_factor_1"] == 1.0
        assert DUT._attributes["change_factor_1"] == 1.0

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_hardware_tree message."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_similar_item_tree"
        )

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1})

        pub.sendMessage("request_get_similar_item_tree")

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_similar_item_tree"
        )

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        DUT.do_set_attributes(
            node_id=[2, -1],
            package={"change_description_1": "Testing set name from moduleview."},
        )
        assert (
            DUT.do_select(2, table="similar_item").change_description_1
            == "Testing set name from moduleview."
        )

        DUT.do_set_attributes(
            node_id=[2, -1],
            package={"change_factor_1": 0.003862},
        )
        assert DUT.do_select(2, table="similar_item").change_factor_1 == 0.003862


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(node_id).data["similar_item"], RAMSTKSimilarItem
        )
        assert tree.get_node(node_id).data["similar_item"].revision_id == 1
        assert tree.get_node(node_id).data["similar_item"].hardware_id == 4
        assert tree.get_node(node_id).data["similar_item"].parent_id == 1
        print("\033[36m\nsucceed_insert_similar_item topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == ("An error occurred with RAMSTK.")
        print("\033[35m\nfail_insert_similar_item topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new sibling hardware assembly."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT._do_insert_similar_item(hardware_id=4, parent_id=1)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_similar_item")

    @pytest.mark.unit
    def test_do_insert_no_parent(self, mock_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_parent, "fail_insert_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT._do_insert_similar_item(hardware_id=5, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_parent, "fail_insert_similar_item")


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent similar item with "
            "similar item ID 100."
        )
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for " "similar item ID 1."
        )
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Allocation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        DUT.do_update(100, table="similar_item")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_similar_item")

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_similar_item")

        DUT = dmSimilarItem()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.tree.get_node(1).data.pop("similar_item")

        DUT.do_update(1, table="similar_item")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_similar_item")


@pytest.mark.usefixtures("mock_program_dao", "test_toml_user_configuration")
class TestAnalysisMethods:
    """Class for similar item methods test suite."""

    def on_succeed_roll_up(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data["similar_item"].change_description_1 == (
            "This is change description 1 for assembly 2.\n\n"
        )
        assert tree.get_node(1).data["similar_item"].change_description_2 == (
            "This is change description 2 for assembly 2.\n\n"
        )
        assert tree.get_node(1).data["similar_item"].change_description_3 == (
            "This is change description 3 for assembly 2.\n\n"
        )
        print("\033[36m\nsucceed_roll_up_change_descriptions topic was broadcast.")

    @pytest.mark.unit
    def test_do_calculate_topic_633(
        self, mock_program_dao, test_toml_user_configuration
    ):
        """do_calculate_goal() should calculate the Topic 6.3.3 similar
        item."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1})

        DUT._dic_hardware_hrs = {1: 0.000628}

        DUT._tree.get_node(1).data["similar_item"].similar_item_method_id = 1
        DUT._tree.get_node(1).data[
            "similar_item"
        ].change_description_1 = "Test change description for factor #1."
        DUT._tree.get_node(1).data["similar_item"].environment_from_id = 2
        DUT._tree.get_node(1).data["similar_item"].environment_to_id = 3
        DUT._tree.get_node(1).data["similar_item"].quality_from_id = 1
        DUT._tree.get_node(1).data["similar_item"].quality_to_id = 2
        DUT._tree.get_node(1).data["similar_item"].temperature_from = 55.0
        DUT._tree.get_node(1).data["similar_item"].temperature_to = 65.0

        pub.sendMessage("request_calculate_similar_item", node_id=1)

        assert DUT._tree.get_node(1).data["similar_item"].change_factor_1 == 0.8
        assert DUT._tree.get_node(1).data["similar_item"].change_factor_2 == 1.4
        assert DUT._tree.get_node(1).data["similar_item"].change_factor_3 == 1.0
        assert DUT._tree.get_node(1).data["similar_item"].result_1 == pytest.approx(
            0.0005607143
        )

    @pytest.mark.unit
    def test_do_calculate_user_defined(
        self, mock_program_dao, test_toml_user_configuration
    ):
        """do_calculate_goal() should calculate the Topic 644 similar item."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1})

        DUT._dic_hardware_hrs = {1: 0.00617}

        DUT._tree.get_node(1).data["similar_item"].similar_item_method_id = 2
        DUT._tree.get_node(1).data["similar_item"].change_description_1 = (
            "Test change description for " "factor #1."
        )
        DUT._tree.get_node(1).data["similar_item"].change_factor_1 = 0.85
        DUT._tree.get_node(1).data["similar_item"].change_factor_2 = 1.2
        DUT._tree.get_node(1).data["similar_item"].function_1 = "pi1*pi2*hr"
        DUT._tree.get_node(1).data["similar_item"].function_2 = "0"
        DUT._tree.get_node(1).data["similar_item"].function_3 = "0"
        DUT._tree.get_node(1).data["similar_item"].function_4 = "0"
        DUT._tree.get_node(1).data["similar_item"].function_5 = "0"

        pub.sendMessage("request_calculate_similar_item", node_id=1)

        assert DUT._tree.get_node(1).data["similar_item"].change_description_1 == (
            "Test change description for factor #1."
        )
        assert DUT._tree.get_node(1).data["similar_item"].change_factor_1 == 0.85
        assert DUT._tree.get_node(1).data["similar_item"].change_factor_2 == 1.2
        assert DUT._tree.get_node(1).data["similar_item"].result_1 == pytest.approx(
            0.0062934
        )

    @pytest.mark.unit
    def test_do_calculate_no_method(
        self, mock_program_dao, test_toml_user_configuration
    ):
        """do_calculate_goal() should calculate the Topic 644 similar item."""
        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1})

        DUT._tree.get_node(1).data["similar_item"].similar_item_method_id = 0

        assert DUT._do_calculate_similar_item(1) is None

    @pytest.mark.unit
    def test_do_roll_up_change_descriptions(
        self, mock_program_dao, test_toml_user_configuration
    ):
        """do_roll_up_change_descriptions() should combine all child change
        descriptions into a single change description for the parent."""
        pub.subscribe(self.on_succeed_roll_up, "succeed_roll_up_change_descriptions")

        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        DUT._tree.get_node(2).data[
            "similar_item"
        ].change_description_1 = "This is change description 1 for assembly 2."
        DUT._tree.get_node(2).data[
            "similar_item"
        ].change_description_2 = "This is change description 2 for assembly 2."
        DUT._tree.get_node(2).data[
            "similar_item"
        ].change_description_3 = "This is change description 3 for assembly 2."

        pub.sendMessage(
            "request_roll_up_change_descriptions", node=DUT._tree.get_node(1)
        )

        pub.unsubscribe(self.on_succeed_roll_up, "succeed_roll_up_change_descriptions")

    @pytest.mark.unit
    def test_on_select_hardware(self, mock_program_dao, test_toml_user_configuration):
        """_on_select_hardware() should assign the node hazard rate to the
        _node_hazard_rate attribute."""
        # RAMSTK Package Imports
        from ramstk.models.programdb import RAMSTKHardware, RAMSTKReliability

        DUT = amSimilarItem(test_toml_user_configuration)

        DATAMGR = dmSimilarItem()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={"revision_id": 1, "hardware_id": 1})

        _hardware = RAMSTKHardware()
        _hardware.hardware_id = 1
        _reliability = RAMSTKReliability()
        _reliability.hazard_rate_active = 0.00032

        _tree = Tree()
        _tree.create_node(tag="hardwares", identifier=0, parent=None)
        _tree.create_node(
            tag="hardware",
            identifier=1,
            parent=0,
            data={
                "hardware": _hardware,
                "reliability": _reliability,
            },
        )

        pub.sendMessage("succeed_get_hardwares_tree", tree=_tree)

        assert DUT._dic_hardware_hrs[1] == 0.00032
