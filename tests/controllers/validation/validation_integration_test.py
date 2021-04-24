# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.validation.validation_integration_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module integrations."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pandas as pd
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import amValidation, dmProgramStatus, dmValidation


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            'do_insert: Database error when attempting to add a record.  '
            'Database returned:\n\tKey (fld_revision_id)=(30) is not present '
            'in table "ramstk_revision".')
        print("\033[35m\nfail_insert_validation topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision,
                      'fail_insert_validation')

        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 30
        DUT._do_insert_validation(parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_validation')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data['validation'].name == 'Test Validation'
        assert tree.get_node(1).data['validation'].time_maximum == 10.5
        print("\033[36m\nsucceed_update_validation topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for validation '
            'ID 1 was the wrong type.')
        print("\033[35m\nfail_update_validation topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_validation')

        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _validation = DUT.do_select(1, 'validation')
        _validation.name = 'Test Validation'
        _validation.time_maximum = 10.5
        DUT.do_update(1, table='validation')

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_validation')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should update all the functions in the database."""
        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _validation = DUT.do_select(1, table='validation')
        _validation.description = 'Big test validation #1'
        _validation = DUT.do_select(2, table='validation')
        _validation.description = 'Big test validation #2'

        DUT.do_update_all()

        assert DUT.do_select(
            1, table='validation').description == 'Big test validation #1'
        assert DUT.do_select(
            2, table='validation').description == 'Big test validation #2'

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_validation')

        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _validation = DUT.do_select(1, table='validation')
        _validation.time_mean = {1: 2}

        DUT.do_update(1, table='validation')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_validation')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmValidation()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _validation = DUT.do_select(1, table='validation')
        _validation.time_mean = {1: 2}

        DUT.do_update(0, table='validation')


@pytest.mark.usefixtures('test_program_dao', 'test_toml_user_configuration')
class TestAnalysisMethods:
    """Class for testing analytical methods."""
    @pytest.mark.integration
    def test_do_select_actuals(self, test_program_dao,
                               test_toml_user_configuration):
        """_do_select_actuals() should return a pandas DataFrame() containing
        actual plan status."""
        DATAMGR = dmValidation()
        DATAMGR.do_connect(test_program_dao)
        DATAMGR.do_select_all(attributes={'revision_id': 1})
        PSMGR = dmProgramStatus()
        PSMGR.do_connect(test_program_dao)
        PSMGR.do_select_all(attributes={'revision_id': 1})

        DUT = amValidation(test_toml_user_configuration)

        pub.sendMessage('request_get_validations_tree')
        pub.sendMessage('succeed_calculate_all_validation_tasks',
                        cost_remaining=212.32,
                        time_remaining=112.5)
        pub.sendMessage('request_get_program_status_tree')

        _actuals = DUT._do_select_actual_status()

        assert isinstance(_actuals, pd.DataFrame)
        assert _actuals.loc[pd.to_datetime(date.today()), 'cost'] == 212.32
        assert _actuals.loc[pd.to_datetime(date.today()), 'time'] == 112.5
