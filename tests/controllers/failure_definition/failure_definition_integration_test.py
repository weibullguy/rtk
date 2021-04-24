# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.failure_definition.failure_definition_integration_test.py
#       is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing failure definition module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmFailureDefinition


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods:
    """Class to test data controller insert methods using actual database."""
    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            '_do_insert_failure_definition: Attempting to add failure '
            'definition to non-existent revision 40.')
        print("\033[35m\nfail_insert_function topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """do_insert() should send the fail_insert_failure_definition message
        when attempting to insert a new failure definition with a non-existent
        revision ID."""
        pub.subscribe(self.on_fail_insert_no_revision,
                      'fail_insert_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 40
        DUT._do_insert_failure_definition()

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_failure_definition')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_update_failure_definition topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for failure '
            'definition ID 1 was the wrong type.')
        print("\033[35m\nfail_update_failure_definition topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should send the succeed_update_failure_definition on
        success."""
        pub.subscribe(self.on_succeed_update,
                      'succeed_update_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _failure_definition = DUT.do_select(1, table='failure_definition')
        _failure_definition.definition = 'Big test definition'

        DUT.do_update(1, table='failure_definition')
        _failure_definition = DUT.do_select(1, table='failure_definition')

        assert _failure_definition.definition == 'Big test definition'

        pub.unsubscribe(self.on_succeed_update,
                        'succeed_update_failure_definition')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all failure_definition() should return None on success."""
        DUT = dmFailureDefinition()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        _failure_definition = DUT.do_select(1, table='failure_definition')
        _failure_definition.definition = 'Big test definition #1'
        _failure_definition = DUT.do_select(2, table='failure_definition')
        _failure_definition.definition = 'Big test definition #2'

        pub.sendMessage('request_update_all_failure_definitions')

        _failure_definition = DUT.do_select(1, table='failure_definition')
        assert _failure_definition.definition == 'Big test definition #1'

        _failure_definition = DUT.do_select(2, table='failure_definition')
        assert _failure_definition.definition == 'Big test definition #2'

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should send the succeed_update_failure_definition on
        success."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_failure_definition')

        DUT = dmFailureDefinition()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT.tree.get_node(1).data['failure_definition'].definition = {
            1: 'Big test definition',
        }

        DUT.do_update(1, table='failure_definition')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_failure_definition')
