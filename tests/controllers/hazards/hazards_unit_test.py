# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_function.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Function algorithms and models."""

# Third Party Imports
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amHazards, dmHazards
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKHazardAnalysis


@pytest.fixture
def mock_program_dao(monkeypatch):
    _hazard_1 = RAMSTKHazardAnalysis()
    _hazard_1.revision_id = 1
    _hazard_1.function_id = 1
    _hazard_1.hazard_id = 1
    _hazard_1.assembly_effect = ''
    _hazard_1.assembly_hri = 20
    _hazard_1.assembly_hri_f = 4
    _hazard_1.assembly_mitigation = ''
    _hazard_1.assembly_probability = 'Level A - Frequent'
    _hazard_1.assembly_probability_f = 'Level A - Frequent'
    _hazard_1.assembly_severity = 'Medium'
    _hazard_1.assembly_severity_f = 'Medium'
    _hazard_1.function_1 = ''
    _hazard_1.function_2 = ''
    _hazard_1.function_3 = ''
    _hazard_1.function_4 = ''
    _hazard_1.function_5 = ''
    _hazard_1.potential_cause = ''
    _hazard_1.potential_hazard = ''
    _hazard_1.remarks = ''
    _hazard_1.result_1 = 0.0
    _hazard_1.result_2 = 0.0
    _hazard_1.result_3 = 0.0
    _hazard_1.result_4 = 0.0
    _hazard_1.result_5 = 0.0
    _hazard_1.system_effect = ''
    _hazard_1.system_hri = 20
    _hazard_1.system_hri_f = 20
    _hazard_1.system_mitigation = ''
    _hazard_1.system_probability = 'Level A - Frequent'
    _hazard_1.system_probability_f = 'Level A - Frequent'
    _hazard_1.system_severity = 'Medium'
    _hazard_1.system_severity_f = 'Medium'
    _hazard_1.user_blob_1 = ''
    _hazard_1.user_blob_2 = ''
    _hazard_1.user_blob_3 = ''
    _hazard_1.user_float_1 = 0.0
    _hazard_1.user_float_2 = 0.0
    _hazard_1.user_float_3 = 0.0
    _hazard_1.user_int_1 = 0
    _hazard_1.user_int_2 = 0
    _hazard_1.user_int_3 = 0

    DAO = MockDAO()
    DAO.table = [
        _hazard_1,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Hazards data manager."""
        DUT = dmHazards()

        assert isinstance(DUT, dmHazards)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'hazards'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_function')
        assert pub.isSubscribed(DUT.do_update, 'request_update_hazard')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_hazards')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_hazard_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_hazard_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_hazard_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_hazard')
        assert pub.isSubscribed(DUT._do_insert_hazard, 'request_insert_hazard')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the function analysis
        manager."""
        DUT = amHazards(test_toml_user_configuration)

        assert isinstance(DUT, amHazards)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_hazard_attributes')
        assert pub.isSubscribed(DUT.on_get_tree, 'succeed_get_hazard_tree')
        assert pub.isSubscribed(DUT.do_calculate_fha, 'request_calculate_fha')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['hazard'], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_retrieve_hazards topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKFunction instances on success."""
        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_hazards')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        pub.unsubscribe(self.on_succeed_select_all, 'succeed_retrieve_hazards')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should clear nodes from an existing Hazards tree."""
        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_hazards')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 2})

        pub.unsubscribe(self.on_succeed_select_all, 'succeed_retrieve_hazards')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKFunction on
        success."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        _hazard = DUT.do_select(1, table='hazard')

        assert isinstance(_hazard, RAMSTKHazardAnalysis)
        assert _hazard.assembly_hri_f == 4
        assert _hazard.assembly_probability == 'Level A - Frequent'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Function ID is
        requested."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        assert DUT.do_select(100, table='hazard') is None


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_hazard topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent hazard ID 10.')
        print("\033[35m\nfail_delete_hazard topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent hazard ID 1.')
        print("\033[35m\nfail_delete_hazard topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, mock_program_dao):
        """_do_delete_hazard() should send the success method when a hazard is
        successfully deleted."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_delete(1)

        assert DUT.tree.get_node(1) is None

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_hazard')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete_hazard() should send the success method when a hazard is
        successfully deleted."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_delete(10)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_hazard')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree."""
        pub.subscribe(self.on_fail_delete_not_in_tree, 'fail_delete_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.tree.remove_node(1)
        DUT._do_delete(1)

        pub.unsubscribe(self.on_fail_delete_not_in_tree, 'fail_delete_hazard')


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_id'] == 1
        assert attributes['potential_hazard'] == ''
        print("\033[36m\nsucceed_get_hazards_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['hazard'], RAMSTKHazardAnalysis)
        print("\033[36m\nsucceed_get_hazard_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """_do_get_attributes() should return a dict of failure definition
        records on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_hazards_attributes')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_get_attributes(1, 'hazard')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_hazards_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        DUT.do_set_attributes(node_id=[
            1,
        ],
                              package={'potential_hazard': 'Donald Trump'})
        assert DUT.do_select(1,
                             table='hazard').potential_hazard == 'Donald Trump'

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the hazard treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_hazard_tree')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_hazard_tree')

    @pytest.mark.unit
    def test_on_get_analysis_manager_tree(self, mock_program_dao,
                                          test_toml_user_configuration):
        """_on_get_tree() should assign the data manager's tree to the _tree
        attribute in response to the succeed_get_function_tree message."""
        DUT = amHazards(test_toml_user_configuration)

        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DATAMGR.do_get_tree()

        assert isinstance(DUT._tree, Tree)
        assert isinstance(
            DUT._tree.get_node(1).data['hazard'], RAMSTKHazardAnalysis)


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 2
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_insert_hazard topic was broadcast.")

    def on_fail_insert_no_parent(self, error_message):
        assert error_message == ('An error occured with RAMSTK.')
        print("\033[35m\nfail_insert_hazard topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_hazard() should send the success message after
        successfully inserting a new hazard."""
        pub.subscribe(self.on_succeed_insert_sibling, 'succeed_insert_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_insert_hazard(parent_id=1)

        assert isinstance(
            DUT.tree.get_node(2).data['hazard'], RAMSTKHazardAnalysis)

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_hazard')

    @pytest.mark.unit
    def test_do_insert_no_parent(self, mock_program_dao):
        """_do_insert_hazard() should send the fail message when attempting to
        add a hazard to a non-existent function ID."""
        pub.subscribe(self.on_fail_insert_no_parent, 'fail_insert_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT._do_insert_hazard(parent_id=10)

        pub.unsubscribe(self.on_fail_insert_no_parent, 'fail_insert_hazard')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent hazard with hazard ID '
            '100.')
        print("\033[35m\nfail_update_hazard topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for hazard ID 1.')
        print("\033[35m\nfail_update_hazard topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.do_update(100, 'hazard')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_hazard')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_hazard')

        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT.tree.get_node(1).data.pop('hazard')

        DUT.do_update(1, 'hazard')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_hazard')

    @pytest.mark.unit
    def test_do_update_root_node(self, mock_program_dao):
        """do_update() should return a non-zero error code when passed a Hazard
        ID that has no data package."""
        DUT = dmHazards()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1, 'function_id': 1})

        DUT.do_update(0, 'hazard')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestAnalysisMethods:
    """Class for testing analytical methods."""
    @pytest.mark.unit
    def test_do_calculate_hri(self, mock_program_dao,
                              test_toml_user_configuration):
        """do_calculate_hri() should calculate the hazard risk index hazard
        analysis."""
        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT = amHazards(test_toml_user_configuration)

        _hazard = DATAMGR.do_select(1, 'hazard')
        _hazard.assembly_severity = 'Major'
        _hazard.assembly_probability = 'Level A - Frequent'
        _hazard.system_severity = 'Medium'
        _hazard.system_probability = 'Level A - Frequent'
        _hazard.assembly_severity_f = 'Medium'
        _hazard.assembly_probability_f = 'Level B - Reasonably Probable'
        _hazard.system_severity_f = 'Medium'
        _hazard.system_probability_f = 'Level C - Occasional'
        DATAMGR.do_update(1, 'hazard')
        pub.sendMessage('request_get_hazard_attributes',
                        node_id=1,
                        table='hazard')

        pub.sendMessage('request_calculate_fha', node_id=1)

        assert DUT._attributes['assembly_hri'] == 30
        assert DUT._attributes['system_hri'] == 20
        assert DUT._attributes['assembly_hri_f'] == 16
        assert DUT._attributes['system_hri_f'] == 12

    @pytest.mark.unit
    def test_do_calculate_user_defined(self, mock_program_dao,
                                       test_toml_user_configuration):
        """do_calculate_user_defined() should calculate the user-defined hazard
        analysis."""
        DATAMGR = dmHazards()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1, 'function_id': 1})
        DUT = amHazards(test_toml_user_configuration)

        _hazard = DATAMGR.do_select(1, 'hazard')
        _hazard.user_float_1 = 1.5
        _hazard.user_float_2 = 0.8
        _hazard.user_int_1 = 2
        _hazard.function_1 = 'uf1*uf2'
        _hazard.function_2 = 'res1/ui1'
        DATAMGR.do_update(1, 'hazard')
        pub.sendMessage('request_get_hazard_attributes',
                        node_id=1,
                        table='hazard')

        pub.sendMessage('request_calculate_fha', node_id=1)

        assert DUT._attributes['result_1'] == pytest.approx(1.2)
        assert DUT._attributes['result_2'] == pytest.approx(0.6)
