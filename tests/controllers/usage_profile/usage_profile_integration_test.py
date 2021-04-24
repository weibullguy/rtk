# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.usage_profile.usage_profile_integration_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Usage Profile integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmEnvironment, dmMission, dmMissionPhase, dmUsageProfile
from ramstk.models.programdb import RAMSTKEnvironment, RAMSTKMission, RAMSTKMissionPhase

test_mission = dmMission()
test_phase = dmMissionPhase()
test_environment = dmEnvironment()


@pytest.mark.usefixtures("test_program_dao")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("1").data["usage_profile"], RAMSTKMission)
        assert isinstance(
            tree.get_node("1.1").data["usage_profile"], RAMSTKMissionPhase
        )
        assert isinstance(
            tree.get_node("1.1.1").data["usage_profile"], RAMSTKEnvironment
        )
        print("\033[36m\nsucceed_retrieve_usage_profile topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMission, RAMSTKMissionPhase, and RAMSTKEnvironment instances on
        success."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_usage_profile")

        DUT.do_set_environment_tree(test_environment.tree)
        DUT.do_set_mission_tree(test_mission.tree)
        DUT.do_set_mission_phase_tree(test_phase.tree)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_usage_profile")

    @pytest.mark.integration
    def test_on_select_all_tree_loaded(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMission, RAMSTKMissionPhase, and RAMSTKEnvironment instances on
        success when the tree is already populated."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        DUT.do_set_environment_tree(test_environment.tree)
        DUT.do_set_mission_tree(test_mission.tree)
        DUT.do_set_mission_phase_tree(test_phase.tree)
        DUT.on_select_all()

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_usage_profile")

        DUT.on_select_all()

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_usage_profile")


@pytest.mark.usefixtures("test_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.integration
    def test_do_delete_mission(self, test_program_dao):
        """_do_delete_mission() should send the success message after
        successfully deleting a mission."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        DUT.do_set_environment_tree(test_environment.tree)
        DUT.do_set_mission_tree(test_mission.tree)
        DUT.do_set_mission_phase_tree(test_phase.tree)

        test_mission._do_delete(1)

        assert not DUT.tree.contains("1.1.1")
        assert not DUT.tree.contains("1.1")
        assert not DUT.tree.contains("1")

    @pytest.mark.integration
    def test_do_delete_mission_phase(self, test_program_dao):
        """_do_delete_mission_phase() should send the success message after
        successfully deleting a mission phase."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        DUT.do_set_environment_tree(test_environment.tree)
        DUT.do_set_mission_tree(test_mission.tree)
        DUT.do_set_mission_phase_tree(test_phase.tree)

        test_phase._do_delete(2)

        assert not DUT.tree.contains("2.2.2")
        assert not DUT.tree.contains("2.2")
        assert DUT.tree.contains("2")

    @pytest.mark.integration
    def test_do_delete_environment(self, test_program_dao):
        """_do_delete_environment() should send the success message after
        successfully deleting an environment."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        DUT.do_set_environment_tree(test_environment.tree)
        DUT.do_set_mission_tree(test_mission.tree)
        DUT.do_set_mission_phase_tree(test_phase.tree)

        test_environment._do_delete(3)

        assert not DUT.tree.contains("3.3.3")
        assert DUT.tree.contains("3.3")
        assert DUT.tree.contains("3")


@pytest.mark.usefixtures("test_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_mission(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("4")
        print("\033[36m\nsucceed_insert_mission topic was broadcast.")

    def on_succeed_insert_mission_phase(self, tree):
        assert isinstance(tree, Tree)
        assert DUT.tree.contains("4.4")
        print("\033[36m\nsucceed_insert_mission_phase topic was broadcast.")

    def on_succeed_insert_environment(self, tree):
        assert isinstance(tree, Tree)
        assert DUT.tree.contains("3.3.4")
        print("\033[36m\nsucceed_insert_environment topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_mission(self, test_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_succeed_insert_mission, "succeed_retrieve_usage_profile")
        pub.sendMessage("request_insert_mission")
        pub.unsubscribe(
            self.on_succeed_insert_mission, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_insert_mission_phase(self, test_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission phase."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        pub.subscribe(
            self.on_succeed_insert_mission_phase, "succeed_retrieve_usage_profile"
        )
        pub.sendMessage("request_insert_mission_phase", mission_id=4)
        pub.unsubscribe(
            self.on_succeed_insert_mission_phase, "succeed_retrieve_usage_profile"
        )

    @pytest.mark.integration
    def test_do_insert_environment(self, test_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new environment."""
        test_mission.do_connect(test_program_dao)
        test_phase.do_connect(test_program_dao)
        test_environment.do_connect(test_program_dao)

        test_mission.do_select_all(attributes={"revision_id": 1})
        test_phase.do_select_all(attributes={"revision_id": 1})
        test_environment.do_select_all(attributes={"revision_id": 1})

        DUT = dmUsageProfile()
        DUT.do_connect(test_program_dao)

        pub.subscribe(
            self.on_succeed_insert_environment, "succeed_retrieve_usage_profile"
        )
        pub.sendMessage("request_insert_environment", phase_id=3)
        pub.unsubscribe(
            self.on_succeed_insert_environment, "succeed_retrieve_usage_profile"
        )
