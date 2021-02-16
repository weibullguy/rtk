# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.revision.revision_integration_test.py is
#       part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing revision module integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRevision


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""
    def on_succeed_update_revision(self, tree):
        assert isinstance(tree, Tree)
        assert tree.get_node(1).data['revision'].name == 'Test Revision'
        print("\033[36m\nsucceed_update_revision topic was broadcast")

    def on_fail_update_revision_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for revision ID '
            '1 was the wrong type.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    @pytest.mark.integration
    def test_do_update_revision(self, test_program_dao):
        """do_update() should send the succeed_update_revision message on
        success."""
        pub.subscribe(self.on_succeed_update_revision,
                      'succeed_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')
        _revision.name = 'Test Revision'
        DUT.do_update(1)

        pub.unsubscribe(self.on_succeed_update_revision,
                        'succeed_update_revision')

    @pytest.mark.integration
    def test_do_update_revision_wrong_data_type(self, test_program_dao):
        """do_update() should send the fail_update_revision message when passed
        a revision ID that that has a wrong data type for one or more
        attributes."""
        pub.subscribe(self.on_fail_update_revision_wrong_data_type,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.tree.get_node(1).data['revision'].cost = None

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_revision_wrong_data_type,
                        'fail_update_revision')

    @pytest.mark.integration
    def test_do_update_revision_root_node(self, test_program_dao):
        """do_update() should end the fail_update_revision message when passed
        a revision ID that has no data package."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        DUT.do_update(0)
