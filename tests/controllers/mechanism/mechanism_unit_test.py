# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mechanism.mechanism_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing failure Mechanism algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMechanism


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mechanism_1 = RAMSTKMechanism()
    _mechanism_1.revision_id = 1
    _mechanism_1.mode_id = 6
    _mechanism_1.mechanism_id = 2
    _mechanism_1.description = "Test Failure Mechanism #1"
    _mechanism_1.rpn = 100
    _mechanism_1.rpn_new = 100
    _mechanism_1.rpn_detection = 10
    _mechanism_1.rpn_detection_new = 10
    _mechanism_1.rpn_occurrence_new = 10
    _mechanism_1.rpn_occurrence = 10
    _mechanism_1.pof_include = 1

    _mechanism_2 = RAMSTKMechanism()
    _mechanism_2.revision_id = 1
    _mechanism_2.mode_id = 1
    _mechanism_2.mechanism_id = 3
    _mechanism_2.description = "Test Failure Mechanism #2"
    _mechanism_2.rpn = 100
    _mechanism_2.rpn_new = 100
    _mechanism_2.rpn_detection = 10
    _mechanism_2.rpn_detection_new = 10
    _mechanism_2.rpn_occurrence_new = 10
    _mechanism_2.rpn_occurrence = 10
    _mechanism_2.pof_include = 1

    DAO = MockDAO()
    DAO.table = [
        _mechanism_1,
        _mechanism_2,
    ]

    yield DAO


@pytest.mark.usefixtures("mock_program_dao")
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmMechanism()

        assert isinstance(DUT, dmMechanism)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "mechanisms"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == 0
        assert pub.isSubscribed(DUT.do_select_all, "selected_mode")
        assert pub.isSubscribed(
            DUT.do_get_attributes, "request_get_mechanism_attributes"
        )
        assert pub.isSubscribed(
            DUT.do_set_attributes, "request_set_mechanism_attributes"
        )
        assert pub.isSubscribed(DUT.do_set_attributes, "wvw_editing_mechanism")
        assert pub.isSubscribed(DUT.do_update, "request_update_mechanism")
        assert pub.isSubscribed(DUT.do_select_all, "selected_mode")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_mechanism_tree")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_mechanism")
        assert pub.isSubscribed(DUT._do_insert_mechanism, "request_insert_mechanism")


@pytest.mark.usefixtures("mock_program_dao")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_retrieve_mechanism topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMechanism instances on success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_mechanism")

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMechanism instances on success."""
        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 1})

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_mechanism")

        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_mechanism")

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKMechanism on
        success."""
        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

        _mechanism = DUT.do_select(2, table="mechanism")

        assert isinstance(_mechanism, RAMSTKMechanism)
        assert _mechanism.pof_include == 1
        assert _mechanism.rpn_detection_new == 10

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

        with pytest.raises(KeyError):
            DUT.do_select(2, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent mechanism ID is
        requested."""
        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

        assert DUT.do_select(100, table="mechanism") is None


@pytest.mark.usefixtures("mock_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_mechanism topic was broadcast when deleting "
            "a failure mode."
        )

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Mechanism ID 300."
        )
        print("\033[35m\nfail_delete_mechanism topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent Mechanism ID 2."
        )
        print("\033[35m\nfail_delete_mechanism topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT._do_delete(2)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mechanism")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mechanism")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mechanism")


@pytest.mark.usefixtures("mock_program_dao")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["mechanism_id"] == 2
        assert attributes["description"] == "System Test Failure Mode #2"
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(2).data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_get_mechanism_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT.do_get_attributes(2, "mechanism")

        pub.unsubscribe(self.on_succeed_get_attributes, "succeed_get_mode_attributes")

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

        DUT.do_set_attributes(node_id=[2, -1], package={"rpn_detection": 4})
        DUT.do_set_attributes(
            node_id=[2, -1], package={"description": "Big test failure mechanism."}
        )
        assert (
            DUT.do_select(2, table="mechanism").description
            == "Big test failure mechanism."
        )
        assert DUT.do_select(2, table="mechanism").rpn_detection == 4

        pub.unsubscribe(DUT.do_set_attributes, "request_set_mechanism_attributes")

    @pytest.mark.unit
    def test_on_get_tree_data_manager(self, mock_program_dao):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mechanism_tree"
        )

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT.do_get_tree()

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mechanism_tree"
        )


@pytest.mark.usefixtures("mock_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(4).data["mechanism"], RAMSTKMechanism)
        print("\033[36m\nsucceed_insert_mechanism topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})

        DUT._do_insert_mechanism()

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mechanism")


@pytest.mark.usefixtures("mock_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent mechanism with mechanism ID 100."
        )
        print("\033[35m\nfail_update_mechanism topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for mechanism ID 2.")
        print("\033[35m\nfail_update_mechanism topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a PoF ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT.do_update(100, table="mechanism")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_mechanism")

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_mechanism")

        DUT = dmMechanism()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all({"revision_id": 1, "hardware_id": 1, "mode_id": 6})
        DUT.tree.get_node(2).data.pop("mechanism")
        DUT.do_update(2, table="mechanism")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_mechanism")
