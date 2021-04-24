# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_method.method_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Operating Stress algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmTestMethod
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKTestMethod


@pytest.fixture
def mock_program_dao(monkeypatch):
    _test_method_1 = RAMSTKTestMethod()
    _test_method_1.revision_id = 1
    _test_method_1.hardware_id = 1
    _test_method_1.mode_id = 1
    _test_method_1.mechanism_id = 1
    _test_method_1.load_id = 1
    _test_method_1.test_id = 1
    _test_method_1.description = "Test Test Method #1"
    _test_method_1.boundary_conditions = "Waters"
    _test_method_1.remarks = ""

    _test_method_2 = RAMSTKTestMethod()
    _test_method_2.revision_id = 1
    _test_method_2.hardware_id = 1
    _test_method_2.mode_id = 1
    _test_method_2.mechanism_id = 1
    _test_method_2.load_id = 1
    _test_method_2.test_id = 2
    _test_method_2.description = "Test Test Method #2"
    _test_method_2.boundary_conditions = "Sands"
    _test_method_2.remarks = ""

    DAO = MockDAO()
    DAO.table = [
        _test_method_1,
        _test_method_2,
    ]

    yield DAO


@pytest.mark.usefixtures("mock_program_dao")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmTestMethod()

        assert isinstance(DUT, dmTestMethod)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "test_methods"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_load")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_test_method_attributes"
        )
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_test_method_attributes"
        )
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_test_method")
        assert pub.isSubscribed(DUT.do_update, "request_update_test_method")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_test_method_tree")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_test_method")
        assert pub.isSubscribed(
            DUT._do_insert_test_method, "request_insert_test_method"
        )


@pytest.mark.usefixtures("mock_program_dao")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["test_method"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_retrieve_test_method topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKTestMethod instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_test_method")

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKTestMethod instances on success."""
        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_test_method")

        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_test_method")

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKTestMethod on
        success."""
        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        print(DUT.tree.all_nodes())
        _test_method = DUT.do_select(2, table="test_method")

        assert isinstance(_test_method, RAMSTKTestMethod)
        assert _test_method.description == "Test Test Method #2"
        assert _test_method.boundary_conditions == "Sands"

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        with pytest.raises(KeyError):
            DUT.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent test_method ID is
        requested."""
        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        assert DUT.do_select(100, table="test_method") is None


@pytest.mark.usefixtures("mock_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_test_method topic was broadcast when deleting "
            "a failure mode."
        )

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Test Method ID 300."
        )
        print("\033[35m\nfail_delete_test_method topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Test Method ID 2."
        )
        print("\033[35m\nfail_delete_test_method topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT._do_delete(2)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_test_method")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_test_method")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_test_method")


@pytest.mark.usefixtures("mock_program_dao")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["load_id"] == 1
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(2).data["test_method"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_get_test_method_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT.do_get_attributes(1, "test_method")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        DUT.do_set_attributes(
            node_id=[1, -1],
            package={"boundary_conditions": "Big test boundary condition."},
        )
        DUT.do_set_attributes(
            node_id=[1, -1], package={"description": "Big test test method."}
        )

        pub.unsubscribe(DUT.do_set_attributes, "request_set_test_method_attributes")

        assert DUT.do_select(1, table="test_method").description == (
            "Big test test " "method."
        )
        assert (
            DUT.do_select(1, table="test_method").boundary_conditions
            == "Big test boundary condition."
        )

    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, mock_program_dao):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_test_method_tree"
        )

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT.do_get_tree()

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_test_method_tree"
        )


@pytest.mark.usefixtures("mock_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["test_method"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_insert_test_method topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_test_method() should send the success message after
        successfully inserting an operating load."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        DUT._do_insert_test_method(1)

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_test_method")


@pytest.mark.usefixtures("mock_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent test method with test method "
            "ID 100."
        )
        print("\033[35m\nfail_update_test_method topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            "do_update: No data package found for test method ID 1."
        )
        print("\033[35m\nfail_update_test_method topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a PoF ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 1,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT.do_update(100, table="test_method")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_test_method")

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_test_method")

        DUT = dmTestMethod()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(
            {
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        DUT.tree.get_node(1).data.pop("test_method")
        DUT.do_update(1, table="test_method")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_test_method")
