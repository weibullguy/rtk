# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.validation.validation_unit_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pandas as pd
import pytest
# noinspection PyUnresolvedReferences
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk import RAMSTKUserConfiguration
from ramstk.controllers import amValidation, dmProgramStatus, dmValidation
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKValidation


@pytest.fixture
def mock_program_dao(monkeypatch):
    _validation_1 = RAMSTKValidation()
    _validation_1.revision_id = 1
    _validation_1.validation_id = 1
    _validation_1.acceptable_maximum = 30.0
    _validation_1.acceptable_mean = 20.0
    _validation_1.acceptable_minimum = 10.0
    _validation_1.acceptable_variance = 0.0
    _validation_1.confidence = 95.0
    _validation_1.cost_average = 0.0
    _validation_1.cost_ll = 0.0
    _validation_1.cost_maximum = 0.0
    _validation_1.cost_mean = 0.0
    _validation_1.cost_minimum = 0.0
    _validation_1.cost_ul = 0.0
    _validation_1.cost_variance = 0.0
    _validation_1.date_end = date.today() + timedelta(days=30)
    _validation_1.date_start = date.today()
    _validation_1.description = ''
    _validation_1.measurement_unit = 0
    _validation_1.name = 'PRF-0001'
    _validation_1.status = 0.0
    _validation_1.task_type = 0
    _validation_1.task_specification = ''
    _validation_1.time_average = 0.0
    _validation_1.time_ll = 0.0
    _validation_1.time_maximum = 0.0
    _validation_1.time_mean = 0.0
    _validation_1.time_minimum = 0.0
    _validation_1.time_ul = 0.0
    _validation_1.time_variance = 0.0

    _validation_2 = RAMSTKValidation()
    _validation_2.revision_id = 1
    _validation_2.validation_id = 2
    _validation_2.acceptable_maximum = 30.0
    _validation_2.acceptable_mean = 20.0
    _validation_2.acceptable_minimum = 10.0
    _validation_2.acceptable_variance = 0.0
    _validation_2.confidence = 95.0
    _validation_2.cost_average = 0.0
    _validation_2.cost_ll = 0.0
    _validation_2.cost_maximum = 0.0
    _validation_2.cost_mean = 0.0
    _validation_2.cost_minimum = 0.0
    _validation_2.cost_ul = 0.0
    _validation_2.cost_variance = 0.0
    _validation_2.date_end = date.today() + timedelta(days=20)
    _validation_2.date_start = date.today() - timedelta(days=10)
    _validation_2.description = ''
    _validation_2.measurement_unit = 0
    _validation_2.name = ''
    _validation_2.status = 0.0
    _validation_2.task_type = 5
    _validation_2.task_specification = ''
    _validation_2.time_average = 0.0
    _validation_2.time_ll = 0.0
    _validation_2.time_maximum = 0.0
    _validation_2.time_mean = 0.0
    _validation_2.time_minimum = 0.0
    _validation_2.time_ul = 0.0
    _validation_2.time_variance = 0.0

    _validation_3 = RAMSTKValidation()
    _validation_3.revision_id = 1
    _validation_3.validation_id = 3
    _validation_3.acceptable_maximum = 30.0
    _validation_3.acceptable_mean = 20.0
    _validation_3.acceptable_minimum = 10.0
    _validation_3.acceptable_variance = 0.0
    _validation_3.confidence = 95.0
    _validation_3.cost_average = 0.0
    _validation_3.cost_ll = 0.0
    _validation_3.cost_maximum = 0.0
    _validation_3.cost_mean = 0.0
    _validation_3.cost_minimum = 0.0
    _validation_3.cost_ul = 0.0
    _validation_3.cost_variance = 0.0
    _validation_3.date_end = date.today() + timedelta(days=30)
    _validation_3.date_start = date.today()
    _validation_3.description = ''
    _validation_3.measurement_unit = 0
    _validation_3.name = ''
    _validation_3.status = 0.0
    _validation_3.task_type = 5
    _validation_3.task_specification = ''
    _validation_3.time_average = 20.0
    _validation_3.time_ll = 19.0
    _validation_3.time_maximum = 40.0
    _validation_3.time_mean = 34.0
    _validation_3.time_minimum = 12.0
    _validation_3.time_ul = 49.0
    _validation_3.time_variance = 0.0

    DAO = MockDAO()
    DAO.table = [
        _validation_1,
        _validation_2,
        _validation_3,
    ]

    yield DAO


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Validation data manager."""
        DUT = dmValidation()

        assert isinstance(DUT, dmValidation)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'validations'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(DUT.do_select_all, 'selected_revision')
        assert pub.isSubscribed(DUT.do_update, 'request_update_validation')
        assert pub.isSubscribed(DUT.do_update_all,
                                'request_update_all_validations')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_validation_attributes')
        assert pub.isSubscribed(DUT.do_get_tree,
                                'request_get_validations_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_validation_attributes')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_validation')
        assert pub.isSubscribed(DUT._do_insert_validation,
                                'request_insert_validation')

    @pytest.mark.unit
    def test_analysis_manager_create(self, test_toml_user_configuration):
        """__init__() should create an instance of the validation analysis
        manager."""
        DUT = amValidation(test_toml_user_configuration)

        assert isinstance(DUT, amValidation)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT._attributes, dict)
        assert isinstance(DUT._tree, Tree)
        assert isinstance(DUT._status_tree, Tree)
        assert DUT._attributes == {}
        assert pub.isSubscribed(DUT.on_get_all_attributes,
                                'succeed_get_all_validation_attributes')
        assert pub.isSubscribed(DUT.on_get_tree,
                                'succeed_get_validations_tree')
        assert pub.isSubscribed(DUT._on_get_status_tree,
                                'succeed_retrieve_program_status')
        assert pub.isSubscribed(DUT._do_calculate_task,
                                'request_calculate_validation_task')
        assert pub.isSubscribed(DUT._do_calculate_all_tasks,
                                'request_calculate_validation_tasks')
        assert pub.isSubscribed(DUT.do_calculate_plan,
                                'request_calculate_plan')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_retrieve_validations topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_validations')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_validations')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKValidation instances on success."""
        pub.subscribe(self.on_succeed_select_all,
                      'succeed_retrieve_validations')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.unsubscribe(self.on_succeed_select_all,
                        'succeed_retrieve_validations')

    @pytest.mark.unit
    def test_do_select(self, mock_program_dao):
        """do_select() should return an instance of the RAMSTKValidation on
        success."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _validation = DUT.do_select(1, table='validation')

        assert isinstance(_validation, RAMSTKValidation)
        assert _validation.acceptable_maximum == 30.0
        assert _validation.name == 'PRF-0001'

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_program_dao):
        """do_select() should return None when a non-existent Validation ID is
        requested."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        assert DUT.do_select(100, table='validation') is None


class TestDeleteMethods:
    """Class for testing the data manager delete() method."""
    def on_succeed_delete(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_validation topic was broadcast.")

    def on_fail_delete_non_existent_id(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent validation task '
            'ID 300.')
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    def on_fail_delete_not_in_tree(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent validation task '
            'ID 2.')
        print("\033[35m\nfail_delete_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete_validation(self, mock_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete, 'succeed_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(DUT.last_id)

        assert DUT.last_id == 2

        pub.unsubscribe(self.on_succeed_delete, 'succeed_delete_validation')

    @pytest.mark.unit
    def test_do_delete_non_existent_id(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a record that doesn't exist in the database."""
        pub.subscribe(self.on_fail_delete_non_existent_id,
                      'fail_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_delete(300)

        pub.unsubscribe(self.on_fail_delete_non_existent_id,
                        'fail_delete_validation')

    @pytest.mark.unit
    def test_do_delete_not_in_tree(self, mock_program_dao):
        """_do_delete() should send the fail message when attempting to remove
        a node that doesn't exist from the tree even if it exists in the
        database."""
        pub.subscribe(self.on_fail_delete_not_in_tree,
                      'fail_delete_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.remove_node(2)
        DUT._do_delete(2)

        pub.unsubscribe(self.on_fail_delete_not_in_tree,
                        'fail_delete_validation')


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['validation_id'] == 1
        assert attributes['name'] == 'PRF-0001'
        assert attributes['time_average'] == 0.0
        print(
            "\033[36m\nsucceed_get_validation_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(1).data['validation'], RAMSTKValidation)
        print("\033[36m\nsucceed_get_validation_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_program_dao):
        """do_get_attributes() should return a dict of validation attributes on
        success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_validation_attributes')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_attributes(1, 'validation')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_validation_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_program_dao):
        """do_set_attributes() should send the success message."""
        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_set_attributes(node_id=[1],
                              package={'task_specification': 'MIL-HDBK-217F'})

        assert DUT.do_select(
            1, table='validation').task_specification == 'MIL-HDBK-217F'

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_program_dao):
        """on_get_tree() should return the validation treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_validation_tree')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_validation_tree')

    @pytest.mark.unit
    def test_on_get_analysis_manager_tree(self, mock_program_dao,
                                          test_toml_user_configuration):
        """_do_request_tree() should send the tree request messages."""
        DUT = amValidation(test_toml_user_configuration)

        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DATAMGR.do_get_tree()

        assert isinstance(DUT._tree, Tree)
        assert isinstance(
            DUT._tree.get_node(1).data['validation'], RAMSTKValidation)


class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_sibling(self, node_id, tree):
        assert node_id == 4
        assert isinstance(tree, Tree)
        assert isinstance(
            tree.get_node(4).data['validation'], RAMSTKValidation)
        assert tree.get_node(4).data['validation'].validation_id == 4
        assert tree.get_node(
            4).data['validation'].name == 'New Validation Task'
        print("\033[36m\nsucceed_insert_validation topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert_sibling(self, mock_program_dao):
        """_do_insert_validation() should send the success message after
        successfully inserting a validation task."""
        pub.subscribe(self.on_succeed_insert_sibling,
                      'succeed_insert_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_validation(parent_id=0)

        pub.unsubscribe(self.on_succeed_insert_sibling,
                        'succeed_insert_validation')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent validation with '
            'validation ID 100.')
        print("\033[35m\nfail_update_validation topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == (
            'do_update: No data package found for validation ID 1.')
        print("\033[35m\nfail_update_validation topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_program_dao):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        DUT.do_update(100, table='validation')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_validation')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_program_dao):
        """do_update() should raise the 'fail_update_validation' message when
        passed a Validation ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(mock_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data.pop('validation')
        DUT.do_update(1, table='validation')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_validation')


@pytest.mark.usefixtures('mock_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods():
    """Class for testing analytical methods."""
    def on_succeed_calculate_plan(self, attributes):
        assert attributes['plan'].loc[pd.to_datetime(date.today()
                                                     - timedelta(days=10)),
                                      'lower'] == pytest.approx(50.0004502)
        assert attributes['plan'].loc[pd.to_datetime(date.today()
                                                     + timedelta(days=20)),
                                      'mean'] == pytest.approx(55.666667)
        assert attributes['plan'].loc[pd.to_datetime(date.today()
                                                     + timedelta(days=30)),
                                      'upper'] == 0.0
        assert attributes['assessed'].loc[pd.to_datetime(date.today()
                                                         + timedelta(days=30)),
                                          'lower'] == 10.0
        assert attributes['assessed'].loc[pd.to_datetime(date.today()
                                                         + timedelta(days=30)),
                                          'mean'] == 20.0
        assert attributes['assessed'].loc[pd.to_datetime(date.today()
                                                         + timedelta(days=30)),
                                          'upper'] == 30.0
        print(
            "\033[36m\nsucceed_calculate_verification_plan topic was broadcast"
        )

    @pytest.mark.unit
    def test_do_calculate_task(self, mock_program_dao,
                               test_toml_user_configuration):
        """do_calculate_task() should calculate the validation task time and
        cost."""
        DUT = amValidation(test_toml_user_configuration)

        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DATAMGR.do_get_tree()

        _validation = DATAMGR.do_select(1, 'validation')
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(1, table='validation')

        DUT._do_calculate_task(node_id=1)

        assert DUT._tree.get_node(
            1).data['validation'].time_ll == pytest.approx(11.86684674)
        assert DUT._tree.get_node(
            1).data['validation'].time_mean == pytest.approx(21.66666667)
        assert DUT._tree.get_node(
            1).data['validation'].time_ul == pytest.approx(31.46648659)
        assert DUT._tree.get_node(1).data['validation'].time_variance == 25.0
        assert DUT._tree.get_node(
            1).data['validation'].cost_ll == pytest.approx(1659.34924016)
        assert DUT._tree.get_node(
            1).data['validation'].cost_mean == pytest.approx(2525.0)
        assert DUT._tree.get_node(
            1).data['validation'].cost_ul == pytest.approx(3390.65075984)
        assert DUT._tree.get_node(1).data[
            'validation'].cost_variance == pytest.approx(195069.44444444)

    @pytest.mark.unit
    def test_do_calculate_all_tasks(self, mock_program_dao,
                                    test_toml_user_configuration):
        """_do_calculate_all_tasks() should calculate the validation tasks time
        and cost."""
        DUT = amValidation(test_toml_user_configuration)

        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DATAMGR.do_get_tree()

        _validation = DATAMGR.do_select(1, 'validation')
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(1, table='validation')

        DUT._do_calculate_all_tasks()

        assert DUT._tree.get_node(
            1).data['validation'].time_ll == pytest.approx(11.86684674)
        assert DUT._tree.get_node(
            1).data['validation'].time_mean == pytest.approx(21.66666667)
        assert DUT._tree.get_node(
            1).data['validation'].time_ul == pytest.approx(31.46648659)
        assert DUT._tree.get_node(1).data['validation'].time_variance == 25.0
        assert DUT._tree.get_node(
            1).data['validation'].cost_ll == pytest.approx(1659.34924016)
        assert DUT._tree.get_node(
            1).data['validation'].cost_mean == pytest.approx(2525.0)
        assert DUT._tree.get_node(
            1).data['validation'].cost_ul == pytest.approx(3390.65075984)
        assert DUT._tree.get_node(1).data[
            'validation'].cost_variance == pytest.approx(195069.44444444)

    @pytest.mark.unit
    def test_do_calculate_verification_plan(self, mock_program_dao,
                                            test_toml_user_configuration):
        """do_calculate_plan() should calculate the planned validation effort
        time and cost."""
        pub.subscribe(self.on_succeed_calculate_plan,
                      'succeed_calculate_verification_plan')

        DUT = amValidation(test_toml_user_configuration)

        DATAMGR = dmValidation()
        DATAMGR.do_connect(mock_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        DATAMGR.do_get_tree()

        _validation = DATAMGR.do_select(1, 'validation')
        _validation.time_minimum = 10.0
        _validation.time_average = 20.0
        _validation.time_maximum = 40.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 1850.0
        _validation.cost_average = 2200.0
        _validation.cost_maximum = 4500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(1, table='validation')

        _validation = DATAMGR.do_select(2, 'validation')
        _validation.time_minimum = 15.0
        _validation.time_average = 32.0
        _validation.time_maximum = 60.0
        _validation.time_mean = 0.0
        _validation.cost_minimum = 750.0
        _validation.cost_average = 1200.0
        _validation.cost_maximum = 2500.0
        _validation.confidence = 95.0
        DATAMGR.do_update(2, table='validation')

        DUT.do_calculate_plan()

        pub.unsubscribe(self.on_succeed_calculate_plan,
                        'succeed_calculate_verification_plan')
