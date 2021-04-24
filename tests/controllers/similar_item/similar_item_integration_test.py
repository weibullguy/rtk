# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.similar_item.similar_item_itegration_test.py is part
#       of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Similar Item module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmSimilarItem


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods:
    """Class for testing the data manager insert() method."""
    def on_fail_insert_no_hardware(self, error_message):
        assert error_message == (
            'do_insert: Database error when attempting to add a record.  '
            'Database returned:\n\tKey (fld_hardware_id)=(15) is not present '
            'in table "ramstk_hardware".')
        print("\033[35m\nfail_insert_similar_item topic was broadcast.")

    def on_fail_insert_no_revision(self, error_message):
        assert error_message == (
            'do_insert: Database error when attempting to add a record.  '
            'Database returned:\n\tKey (fld_revision_id)=(40) is not present '
            'in table "ramstk_revision".')
        print("\033[35m\nfail_insert_similar_item topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_no_hardware(self, test_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_hardware,
                      'fail_insert_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._do_insert_similar_item(hardware_id=15, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_hardware,
                        'fail_insert_similar_item')

    @pytest.mark.integration
    def test_do_insert_no_revision(self, test_program_dao):
        """_do_insert_function() should send the fail message if attempting to
        add a function to a non-existent parent ID."""
        pub.subscribe(self.on_fail_insert_no_revision,
                      'fail_insert_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        DUT._revision_id = 40
        DUT._do_insert_similar_item(hardware_id=8, parent_id=0)

        pub.unsubscribe(self.on_fail_insert_no_revision,
                        'fail_insert_similar_item')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(2).data['similar_item'].parent_id == 1
        assert tree.get_node(
            2).data['similar_item'].percent_weight_factor == 0.9832
        assert tree.get_node(2).data['similar_item'].mtbf_goal == 12000
        print("\033[36m\nsucceed_update_similar_item topic was broadcast.")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for similar item '
            'ID 1 was the wrong type.')
        print("\033[35m\nfail_update_similar_item topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        pub.sendMessage('request_update_similar_item',
                        node_id=2,
                        table='similar_item')

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_similar_item')

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_similar_item')

        DUT = dmSimilarItem()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _similar_item = DUT.do_select(1, table='similar_item')
        _similar_item.change_factor_1 = {1: 2}

        DUT.do_update(1, table='similar_item')

        pub.unsubscribe(self.on_fail_update_wrong_data_type,
                        'fail_update_similar_item')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        DUT = dmSimilarItem()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})
        _similar_item = DUT.do_select(1, table='similar_item')
        _similar_item.change_factor_1 = {1: 2}

        DUT.do_update(0, table='similar_item')

    @pytest.mark.integration
    def test_do_update_all(self, test_program_dao):
        """do_update_all() should return a zero error code on success."""
        DUT = dmSimilarItem()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all(attributes={'revision_id': 1})

        def on_message(tree):
            assert isinstance(tree, Tree)

        pub.subscribe(on_message, 'succeed_update_similar_item')

        pub.sendMessage('request_update_all_similar_items')
