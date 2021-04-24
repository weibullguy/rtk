# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.stakeholder.stakeholder_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

# Third Party Imports
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amStakeholder, dmStakeholder
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKStakeholder


@pytest.fixture
def mock_program_dao(monkeypatch):
    _stakeholder_1 = RAMSTKStakeholder()
    _stakeholder_1.revision_id = 1
    _stakeholder_1.requirement_id = 1
    _stakeholder_1.stakeholder_id = 1
    _stakeholder_1.customer_rank = 1
    _stakeholder_1.description = 'Stakeholder Input'
    _stakeholder_1.group = ''
    _stakeholder_1.improvement = 0.0
    _stakeholder_1.overall_weight = 0.0
    _stakeholder_1.planned_rank = 1
    _stakeholder_1.priority = 1
    _stakeholder_1.stakeholder = ''
    _stakeholder_1.user_float_1 = 1.0
    _stakeholder_1.user_float_2 = 1.0
    _stakeholder_1.user_float_3 = 1.0
    _stakeholder_1.user_float_4 = 1.0
    _stakeholder_1.user_float_5 = 1.0

    _stakeholder_2 = RAMSTKStakeholder()
    _stakeholder_2.revision_id = 1
    _stakeholder_2.requirement_id = 1
    _stakeholder_2.stakeholder_id = 2
    _stakeholder_2.customer_rank = 1
    _stakeholder_2.description = 'Stakeholder Input'
    _stakeholder_2.group = ''
    _stakeholder_2.improvement = 0.0
    _stakeholder_2.overall_weight = 0.0
    _stakeholder_2.planned_rank = 1
    _stakeholder_2.priority = 1
    _stakeholder_2.stakeholder = ''
    _stakeholder_2.user_float_1 = 1.0
    _stakeholder_2.user_float_2 = 1.0
    _stakeholder_2.user_float_3 = 1.0
    _stakeholder_2.user_float_4 = 1.0
    _stakeholder_2.user_float_5 = 1.0

    DAO = MockDAO()
    DAO.table = [
        _stakeholder_1,
        _stakeholder_2,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Stakeholder data manager."""
        DUT = dmStakeholder()

        assert isinstance(DUT, dmStakeholder)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'stakeholders'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_stakeholders')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_stakeholders')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_stakeholder_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_stakeholder_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_stakeholder_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_stakeholder')
        assert pub.isSubscribed(DUT._do_insert_stakeholder,
                                'request_insert_stakeholder')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the function analysis
        manager."""
        DUT = amStakeholder(test_toml_user_configuration)

        assert isinstance(DUT, amStakeholder)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_stakeholder_attributes')
        assert pub.isSubscribed(DUT.on_get_tree,
                                'succeed_get_stakeholder_tree')
        assert pub.isSubscribed(DUT.do_calculate_stakeholder,
                                'request_calculate_stakeholder')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(
            tree.get_node(1).data['stakeholder'], RAMSTKStakeholder)
        print("\033[36m\nsucceed_retrieve_stakeholders topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKStakeholder instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_stakeholders')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_stakeholders')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all(1) should clear a populate Tree when selecting a new
        set of stakeholder records."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_stakeholders')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_stakeholders')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKStakeholder on
        success."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _stakeholder = DUT.do_select(1, table='stakeholder')

        assert isinstance(_stakeholder, RAMSTKStakeholder)
        assert _stakeholder.description == 'Stakeholder Input'
        assert _stakeholder.priority == 1

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Stakeholder ID is
        requested."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='stakeholder') is None


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_stakeholder topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent stakeholder input '
            'ID 300.')
        print("\033[35m\nfail_delete_stakeholder topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent stakeholder input '
            'ID 2.')
        print("\033[35m\nfail_delete_stakeholder topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 1

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_stakeholder')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a non-existent stakeholder."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_stakeholder')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree,
                      'fail_delete_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree,
                        'fail_delete_stakeholder')


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['stakeholder_id'] == 1
        assert attributes['description'] == 'Stakeholder Input'
        assert attributes['priority'] == 1
        print(
            "\033[36m\nsucceed_get_stakeholder_attributes topic was broadcast")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data, dict)
        assert isinstance(
            tree.get_node(1).data['stakeholder'], RAMSTKStakeholder)
        print("\033[36m\nsucceed_get_stakeholder_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of stakeholder attributes
        on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_stakeholder_attributes')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'stakeholder')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_stakeholder_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(node_id=[1, -1],
                              package={'stakeholder': 'Customer'})
        assert DUT.do_select(1, table='stakeholder').stakeholder == 'Customer'

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the stakeholder treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_stakeholder_tree')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_stakeholder_tree')


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 3
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(3).data['stakeholder'], RAMSTKStakeholder)
        assert tree.get_node(3).data['stakeholder'].stakeholder_id == 3
        assert tree.get_node(
            3).data['stakeholder'].description == 'New Stakeholder Input'
        print("\033[36m\nsucceed_insert_stakeholder topic was broadcast")

    @pytest.mark.unit
    def test_do_insert(self, mock_program_dao):
        """_do_insert_stakeholder() should send the success message after
        successfully inserting a new top-level stakeholder."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_stakeholder')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_stakeholder()

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_stakeholder')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent stakeholder input with '
            'stakeholder input ID 100.')
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for stakeholder input ID 1.')
        print("\033[35m\nfail_update_stakeholder topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should broadcast the fail update message when passed an
        ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_stakeholders')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_update(100, table='stakeholder')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_stakeholders')

    @pytest.mark.unit
    def test_do_update_data_manager_no_data_package(self, mock_program_dao):
        """do_update() should broadcast the fail update message when there is
        no data package attached to the node."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_stakeholders')

        DUT = dmStakeholder()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('stakeholder')
        DUT.do_update(1, table='stakeholder')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_stakeholders')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestAnalysisMethods:
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_improvement(self, mock_program_dao,
                                      test_toml_user_configuration):
        """do_calculate_stakeholder() should calculate the improvement factor
        and overall weight of a stakeholder input."""
        DUT = amStakeholder(test_toml_user_configuration)

        DATAMGR = dmStakeholder()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DATAMGR.do_get_tree()

        _stakeholder = DATAMGR.do_select(1, 'stakeholder')
        _stakeholder.planned_rank = 3
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 4
        _stakeholder.user_float_1 = 2.6
        DATAMGR.do_update(1, table='stakeholder')
        DATAMGR.do_get_attributes(node_id=1, table='stakeholder')

        DUT.do_calculate_stakeholder(1)

        assert DUT._attributes['improvement'] == 1.2
        assert DUT._attributes['overall_weight'] == 12.48
