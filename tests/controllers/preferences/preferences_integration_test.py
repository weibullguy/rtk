# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.preferences.preferences_integration_test.py is part
#       of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Preferences integrations."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import dmPreferences


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_preferences topic was broadcast")

    def on_fail_update_wrong_data_type(self, error_message):
        assert error_message == ('do_update: The value for one or more '
                                 'attributes for Preferences 1 was the wrong '
                                 'type.')
        print("\033[35m\nfail_update_preferences topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(test_program_dao)

        DUT.tree.get_node(1).data['programinfo'].hardware_active = 0
        DUT.tree.get_node(1).data['programinfo'].vandv_active = 0
        DUT.do_update(1, table='programinfo')

        assert DUT.tree.get_node(1).data['programinfo'].hardware_active == 0
        assert DUT.tree.get_node(1).data['programinfo'].vandv_active == 0

        DUT.tree.get_node(1).data['programinfo'].hardware_active = 1
        DUT.tree.get_node(1).data['programinfo'].vandv_active = 1
        DUT.do_update(1, table='programinfo')

        assert DUT.tree.get_node(1).data['programinfo'].hardware_active == 1
        assert DUT.tree.get_node(1).data['programinfo'].vandv_active == 1

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_preferences')

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_preferences')

        DUT = dmPreferences()
        DUT._do_select_all(test_program_dao)
        DUT.tree.get_node(1).data['programinfo'].hardware_active = {0: 1}
        DUT.do_update(1, table='programinfo')

        pub.subscribe(self.on_fail_update_wrong_data_type,
                      'fail_update_preferences')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        DUT = dmPreferences()
        DUT._do_select_all(test_program_dao)
        DUT.tree.get_node(1).data['programinfo'].hardware_active = {0: 1}
        DUT.do_update(0, table='programinfo')
