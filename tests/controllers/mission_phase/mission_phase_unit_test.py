# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.mission_phase.mission_phase_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Mission Phase module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMissionPhase
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMissionPhase


@pytest.fixture
def mock_program_dao(monkeypatch):
    _mission_phase_1 = RAMSTKMissionPhase()
    _mission_phase_1.revision_id = 1
    _mission_phase_1.mission_id = 1
    _mission_phase_1.phase_id = 1
    _mission_phase_1.description = 'Phase #1 for mission #1'
    _mission_phase_1.name = 'Start Up'
    _mission_phase_1.phase_start = 0.0
    _mission_phase_1.phase_end = 0.0

    _mission_phase_2 = RAMSTKMissionPhase()
    _mission_phase_2.revision_id = 1
    _mission_phase_2.mission_id = 1
    _mission_phase_2.phase_id = 2
    _mission_phase_2.description = 'Phase #2 for mission #1'
    _mission_phase_2.name = 'Operation'
    _mission_phase_2.phase_start = 0.0
    _mission_phase_2.phase_end = 0.0

    _mission_phase_3 = RAMSTKMissionPhase()
    _mission_phase_3.revision_id = 1
    _mission_phase_3.mission_id = 1
    _mission_phase_3.phase_id = 3
    _mission_phase_3.description = 'Phase #3 for mission #1'
    _mission_phase_3.name = 'Shut Down'
    _mission_phase_3.phase_start = 0.0
    _mission_phase_3.phase_end = 0.0

    DAO = MockDAO()
    DAO.table = [
        _mission_phase_1,
        _mission_phase_2,
        _mission_phase_3,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return an MissionPhase data manager."""
        DUT = dmMissionPhase()

        assert isinstance(DUT, dmMissionPhase)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'mission_phases'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_mission_phase_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_mission_phase_tree')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_mission_phase')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_mission_phases')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_mission_phase')
        assert pub.isSubscribed(DUT._do_insert_mission_phase,
                                'request_insert_mission_phase')


@pytest.mark.usefixtures('mock_program_dao')
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['mission_phase'], RAMSTKMissionPhase)
        assert isinstance(
            tree.get_node(2).data['mission_phase'], RAMSTKMissionPhase)
        print("\033[36m\nsucceed_retrieve_mission_phases topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMissionPhase instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_mission_phases')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_mission_phases')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object when the tree is
        already populated."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_mission_phases')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_mission_phases')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return the RAMSTKMission instance on
        success."""
        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _mission_phase = DUT.do_select(1, table='mission_phase')

        assert isinstance(_mission_phase, RAMSTKMissionPhase)
        assert _mission_phase.phase_id == 1

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='mission_phase') is None


@pytest.mark.usefixtures('mock_program_dao')
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_mission_phase topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent mission phase ID '
            '10.')
        print("\033[35m\nfail_delete_mission_phase topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent mission phase ID 2.')
        print("\033[35m\nfail_delete_mission_phase topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete_mission_phase() should send the success message after
        successfully deleting a mission phase."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_mission_phase')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(1)

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_mission_phase')

    @pytest.mark.unit
    def test_do_delete_mission_phase_non_existent_id(self, mock_program_dao):
        """_do_delete_mission_phase() should send the sfail message when attempting
        to delete a non-existent mission phase ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_mission_phase')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_mission_phase')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree,
                      'fail_delete_mission_phase')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree,
                        'fail_delete_mission_phase')


@pytest.mark.usefixtures('mock_program_dao')
class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['mission_id'] == 1
        assert attributes['phase_id'] == 1
        assert attributes['description'] == 'Phase #1 for mission #1'
        print(
            "\033[36m\nsucceed_get_mission_phase_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['mission_phase'], RAMSTKMissionPhase)
        print("\033[36m\nsucceed_get_mission_phase_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_mission_phase_attributes')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'mission_phase')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_mission_phase_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(
            node_id=[1, ''], package={'phase_start': 12.86})

        assert DUT.do_select(
            1, table='mission_phase').phase_start == 12.86

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_mission_phase_tree')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_mission_phase_tree')


@pytest.mark.usefixtures('mock_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(4).data['mission_phase'], RAMSTKMissionPhase)
        print("\033[36m\nsucceed_insert_mission_phase topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new mission_phase."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_mission_phase')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_mission_phase(1)

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_mission_phase')


@pytest.mark.usefixtures('mock_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent mission phase with '
            'mission phase ID 10.')
        print("\033[35m\nfail_update_mission_phase topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for mission phase ID 1.')
        print("\033[35m\nfail_update_mission_phase topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_mission_phase')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(10, table='mission_phase')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_mission_phase')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_mission_phase')

        DUT = dmMissionPhase()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('mission_phase')
        DUT.do_update(1, table='mission_phase')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_mission_phase')
