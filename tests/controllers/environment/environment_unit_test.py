# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.environment.environment_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Environment module algorithms and models."""

# Third Party Imports
import pytest

# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmEnvironment
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKEnvironment


@pytest.fixture
def mock_program_dao(monkeypatch):
    _environment_1 = RAMSTKEnvironment()
    _environment_1.revision_id = 1
    _environment_1.phase_id = 1
    _environment_1.environment_id = 1
    _environment_1.name = 'Condition Name'
    _environment_1.units = 'Units'
    _environment_1.minimum = 0.0
    _environment_1.maximum = 0.0
    _environment_1.mean = 0.0
    _environment_1.variance = 0.0
    _environment_1.ramp_rate = 0.0
    _environment_1.low_dwell_time = 0.0
    _environment_1.high_dwell_time = 0.0

    _environment_2 = RAMSTKEnvironment()
    _environment_2.revision_id = 1
    _environment_2.phase_id = 1
    _environment_2.environment_id = 2
    _environment_2.name = 'Condition Name'
    _environment_2.units = 'Units'
    _environment_2.minimum = 0.0
    _environment_2.maximum = 0.0
    _environment_2.mean = 0.0
    _environment_2.variance = 0.0
    _environment_2.ramp_rate = 0.0
    _environment_2.low_dwell_time = 0.0
    _environment_2.high_dwell_time = 0.0

    _environment_3 = RAMSTKEnvironment()
    _environment_3.revision_id = 1
    _environment_3.phase_id = 1
    _environment_3.environment_id = 3
    _environment_3.name = 'Condition Name'
    _environment_3.units = 'Units'
    _environment_3.minimum = 0.0
    _environment_3.maximum = 0.0
    _environment_3.mean = 0.0
    _environment_3.variance = 0.0
    _environment_3.ramp_rate = 0.0
    _environment_3.low_dwell_time = 0.0
    _environment_3.high_dwell_time = 0.0

    DAO = MockDAO()
    DAO.table = [
        _environment_1,
        _environment_2,
        _environment_3,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return an Environment data manager."""
        DUT = dmEnvironment()

        assert isinstance(DUT, dmEnvironment)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'environments'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_environment_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_environment_tree')
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_environment')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_environments')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_environment')
        assert pub.isSubscribed(DUT._do_insert_environment,
                                'request_insert_environment')


@pytest.mark.usefixtures('mock_program_dao')
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['environment'], RAMSTKEnvironment)
        assert isinstance(
            tree.get_node(2).data['environment'], RAMSTKEnvironment)
        assert isinstance(
            tree.get_node(3).data['environment'], RAMSTKEnvironment)
        print("\033[36m\nsucceed_retrieve_environments topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMission, RAMSTKMissionPhase, and RAMSTKEnvironment instances on
        success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_environments')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_environments')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object when the tree is
        already populated."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_environments')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_environments')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return the RAMSTKEnvironment instance on
        success."""
        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _environment = DUT.do_select(1, table='environment')

        assert isinstance(_environment, RAMSTKEnvironment)
        assert _environment.environment_id == 1

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='environment') is None


@pytest.mark.usefixtures('mock_program_dao')
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_environment topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent environment ID 10.')
        print("\033[35m\nfail_delete_environment topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent environment ID 2.')
        print("\033[35m\nfail_delete_environment topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete_mission() should send the success message after
        successfully deleting a mission."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_environment')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(1)

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_environment')

    @pytest.mark.unit
    def test_do_delete_mission_non_existent_id(self, mock_program_dao):
        """_do_delete_mission() should send the sfail message when attempting
        to delete a non-existent mission ID."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_environment')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_environment')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree,
                      'fail_delete_environment')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree,
                        'fail_delete_environment')


@pytest.mark.usefixtures('mock_program_dao')
class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['phase_id'] == 1
        assert attributes['environment_id'] == 1
        assert attributes['name'] == 'Condition Name'
        print(
            "\033[36m\nsucceed_get_environment_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['environment'], RAMSTKEnvironment)
        print("\033[36m\nsucceed_get_environment_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return treelib Tree() on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_environment_attributes')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'environment')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_environment_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(
            node_id=[1, ''], package={'name': 'This is the environment name.'})

        assert DUT.do_select(
            1, table='environment').name == ('This is the environment name.')

    @pytest.mark.unit
    def test_on_get_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_environment_tree')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_environment_tree')


@pytest.mark.usefixtures('mock_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(4).data['environment'], RAMSTKEnvironment)
        print("\033[36m\nsucceed_insert_environment topic was broadcast")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """do_insert() should send the success message after successfully
        inserting a new environment."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_environment')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_environment(1)

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_environment')


@pytest.mark.usefixtures('mock_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent environment with '
            'environment ID 10.')
        print("\033[35m\nfail_update_environment topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for environment ID 1.')
        print("\033[35m\nfail_update_environment topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_environment')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(10, table='environment')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_environment')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update_usage_profile() should broadcast the fail message when
        attempting to save a non-existent ID."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_environment')

        DUT = dmEnvironment()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('environment')
        DUT.do_update(1, table='environment')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_environment')
