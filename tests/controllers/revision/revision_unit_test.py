# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module algorithms and models."""

# Third Party Imports
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRevision
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKRevision


@pytest.fixture
def mock_program_dao(monkeypatch):
    _revision_1 = RAMSTKRevision()
    _revision_1.revision_id = 1
    _revision_1.availability_logistics = 0.9986
    _revision_1.availability_mission = 0.99934
    _revision_1.cost = 12532.15
    _revision_1.cost_failure = 0.0000352
    _revision_1.cost_hour = 1.2532
    _revision_1.hazard_rate_active = 0.0
    _revision_1.hazard_rate_dormant = 0.0
    _revision_1.hazard_rate_logistics = 0.0
    _revision_1.hazard_rate_mission = 0.0
    _revision_1.hazard_rate_software = 0.0
    _revision_1.mmt = 0.0
    _revision_1.mcmt = 0.0
    _revision_1.mpmt = 0.0
    _revision_1.mtbf_logistics = 0.0
    _revision_1.mtbf_mission = 0.0
    _revision_1.mttr = 0.0
    _revision_1.name = 'Original Revision'
    _revision_1.reliability_logistics = 0.99986
    _revision_1.reliability_mission = 0.99992
    _revision_1.remarks = 'This is the original revision.'
    _revision_1.revision_code = 'Rev. -'
    _revision_1.program_time = 2562
    _revision_1.program_time_sd = 26.83
    _revision_1.program_cost = 26492.83
    _revision_1.program_cost_sd = 15.62

    _revision_2 = RAMSTKRevision()
    _revision_2.revision_id = 2
    _revision_2.availability_logistics = 1.0
    _revision_2.availability_mission = 1.0
    _revision_2.cost = 0.0
    _revision_2.cost_failure = 0.0
    _revision_2.cost_hour = 0.0
    _revision_2.hazard_rate_active = 0.0
    _revision_2.hazard_rate_dormant = 0.0
    _revision_2.hazard_rate_logistics = 0.0
    _revision_2.hazard_rate_mission = 0.0
    _revision_2.hazard_rate_software = 0.0
    _revision_2.mmt = 0.0
    _revision_2.mcmt = 0.0
    _revision_2.mpmt = 0.0
    _revision_2.mtbf_logistics = 0.0
    _revision_2.mtbf_mission = 0.0
    _revision_2.mttr = 0.0
    _revision_2.name = 'Revision A'
    _revision_2.reliability_logistics = 1.0
    _revision_2.reliability_mission = 1.0
    _revision_2.remarks = 'This is the second revision.'
    _revision_2.revision_code = 'Rev. A'
    _revision_2.program_time = 0
    _revision_2.program_time_sd = 0.0
    _revision_2.program_cost = 0.0
    _revision_2.program_cost_sd = 0.0

    DAO = MockDAO()
    DAO.table = [
        _revision_1,
        _revision_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Revision data manager."""
        DUT = dmRevision()

        assert isinstance(DUT, dmRevision)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'revisions'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all,
                                'request_retrieve_revisions')
        assert pub.isSubscribed(DUT.do_update, 'request_update_revision')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_revisions')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_revision_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_revision_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_revision_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_revision')
        assert pub.isSubscribed(DUT._do_insert_revision,
                                'request_insert_revision')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKRevision instances on success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        assert isinstance(DUT.tree, Tree)
        assert isinstance(
            DUT.tree.get_node(1).data['revision'], RAMSTKRevision)

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKRevision on
        success."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')

        assert isinstance(_revision, RAMSTKRevision)
        assert _revision.availability_logistics == 0.9986
        assert _revision.name == 'Original Revision'

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select() should clear any existing tree when selecting
        revisions."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_select_all()

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Revision ID is
        requested."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        assert DUT.do_select(100, table='revision') is None


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_revision topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent revision ID 300.')
        print("\033[35m\nfail_delete_revision topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_revision')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a non-existent revision."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_revision')


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['revision_id'] == 1
        assert attributes['name'] == 'Original Revision'
        assert attributes['program_time'] == 2562
        print("\033[36m\nsucceed_get_revision_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['revision'], RAMSTKRevision)
        print("\033[36m\nsucceed_get_revision_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return a dict of revision attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_revision_attributes')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_attributes(1, 'revision')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_revision_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()

        DUT.do_set_attributes(node_id=[
            1,
        ], package={'revision_code': '-'})
        assert DUT.do_select(1, table='revision').revision_code == '-'

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the revision treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_revision_tree')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_revision_tree')


@pytest.mark.usefixtures('mock_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_revision topic was broadcast")

    def on_fail_insert_no_database(self, error_message):
        assert error_message == ('_do_insert_revision: Failed to insert '
                                 'revision into program database.')
        print("\033[35m\nfail_insert_revision topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT._do_insert_revision()

        assert isinstance(
            DUT.tree.get_node(3).data['revision'], RAMSTKRevision)
        assert DUT.tree.get_node(3).data['revision'].revision_id == 3
        assert DUT.tree.get_node(3).data['revision'].name == 'New Revision'

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_revision')

    @pytest.mark.unit
    def test_do_insert_no_database(self):
        """_do_insert_revision() should send the success message after
        successfully inserting a new revision."""
        pub.subscribe(self.on_fail_insert_no_database, 'fail_insert_revision')

        DUT = dmRevision()
        DUT._do_insert_revision()

        pub.unsubscribe(self.on_fail_insert_no_database,
                        'fail_insert_revision')


@pytest.mark.usefixtures('mock_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent revision with revision '
            'ID 100.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for revision ID 1.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        revision ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.do_update(100, table='revision')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_revision')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a
        Function ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all()
        DUT.tree.get_node(1).data.pop('revision')

        DUT.do_update(1, table='revision')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_revision')
