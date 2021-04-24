# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission.mission_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMission
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMission


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_1 = RAMSTKMission()
    _mission_1.revision_id = 1
    _mission_1.mission_id = 1
    _mission_1.description = "Test mission #1"
    _mission_1.mission_time = 100.0
    _mission_1.time_units = "hours"

    _mission_2 = RAMSTKMission()
    _mission_2.revision_id = 1
    _mission_2.mission_id = 2
    _mission_2.description = "Test mission #2"
    _mission_2.mission_time = 24.0
    _mission_2.time_units = "hours"

    DAO = MockDAO()
    DAO.table = [
        _mission_1,
        _mission_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return an Mission data manager."""
        DUT = dmMission()

        assert isinstance(DUT, dmMission)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "missions"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes, "request_get_mission_attributes")
        assert pub.isSubscribed(DUT.do_get_tree, "request_get_mission_tree")
        assert pub.isSubscribed(DUT.do_select_all, "selected_revision")
        assert pub.isSubscribed(DUT.do_update, "request_update_mission")
        assert pub.isSubscribed(DUT.do_update_all, "request_update_all_missions")
        assert pub.isSubscribed(DUT._do_delete, "request_delete_mission")
        assert pub.isSubscribed(DUT._do_insert_mission, "request_insert_mission")


@pytest.mark.usefixtures("mock_program_dao")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mission"], RAMSTKMission)
        assert isinstance(tree.get_node(2).data["mission"], RAMSTKMission)
        print("\033[36m\nsucceed_retrieve_missions topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMission, RAMSTKMissionPhase, and RAMSTKMission instances on
        success."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_missions")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_missions")

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object when the tree is
        already populated."""
        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_missions")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.do_select_all(attributes={"revision_id": 1})

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_missions")

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return the RAMSTKMission instance on
        success."""
        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        _mission = DUT.do_select(1, table="mission")

        assert isinstance(_mission, RAMSTKMission)
        assert _mission.mission_id == 1

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table="scibbidy-bibbidy-doo")

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        assert DUT.do_select(100, table="mission") is None


@pytest.mark.usefixtures("mock_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mission topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mission ID 10."
        )
        print("\033[35m\nfail_delete_mission topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            "_do_delete: Attempted to delete non-existent mission ID 2."
        )
        print("\033[35m\nfail_delete_mission topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete_mission() should send the success message after
        successfully deleting a mission."""
        pub.subscribe(self.on_succeed_delete, "succeed_delete_mission")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT._do_delete(1)

        pub.unsubscribe(self.on_succeed_delete, "succeed_delete_mission")

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete_mission() should send the sfail message when attempting
        to delete a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id, "fail_delete_mission")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT._do_delete(10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id, "fail_delete_mission")

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree, "fail_delete_mission")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, "fail_delete_mission")


@pytest.mark.usefixtures("mock_program_dao")
class TestGetterSetter:
    """Class for testing methods that get or set."""

    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes["revision_id"] == 1
        assert attributes["mission_id"] == 1
        assert attributes["description"] == "Test mission #1"
        print("\033[36m\nsucceed_get_mission_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data["mission"], RAMSTKMission)
        print("\033[36m\nsucceed_get_mission_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_attributes, "succeed_get_mission_attributes")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.do_get_attributes(1, "mission")

        pub.unsubscribe(
            self.on_succeed_get_attributes, "succeed_get_mission_attributes"
        )

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})

        DUT.do_set_attributes(node_id=[1, ""], package={"mission_time": 12.86})

        assert DUT.do_select(1, table="mission").mission_time == 12.86

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree, "succeed_get_mission_tree")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.do_get_tree()

        pub.unsubscribe(
            self.on_succeed_get_data_manager_tree, "succeed_get_mission_tree"
        )


@pytest.mark.usefixtures("mock_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(3).data["mission"], RAMSTKMission)
        print("\033[36m\nsucceed_insert_mission topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        pub.subscribe(self.on_succeed_insert_sibling, "succeed_insert_mission")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT._do_insert_mission()

        pub.unsubscribe(self.on_succeed_insert_sibling, "succeed_insert_mission")


@pytest.mark.usefixtures("mock_program_dao")
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""

    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            "do_update: Attempted to save non-existent mission with " "mission ID 10."
        )
        print("\033[35m\nfail_update_mission topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ("do_update: No data package found for mission ID 1.")
        print("\033[35m\nfail_update_mission topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id, "fail_update_mission")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.do_update(10, table="mission")

        pub.unsubscribe(self.on_fail_update_non_existent_id, "fail_update_mission")

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_no_data_package, "fail_update_mission")

        DUT = dmMission()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={"revision_id": 1})
        DUT.tree.get_node(1).data.pop("mission")
        DUT.do_update(1, table="mission")

        pub.unsubscribe(self.on_fail_update_no_data_package, "fail_update_mission")
