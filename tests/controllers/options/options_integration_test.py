# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.options.options_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options module integrations."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import dmOptions


@pytest.mark.usefixtures('test_common_dao')
class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_succeed_update(self, node_id):
        assert node_id == 1
        print("\033[36m\nsucceed_update_options topic was broadcast")

    def on_fail_update_options_wrong_data_type(self, error_message):
        assert error_message == ('do_update: The value for one or more '
                                 'attributes for Site 1 options was the wrong '
                                 'type.')
        print("\033[35m\nfail_update_options topic was broadcast")

    @pytest.mark.integration
    def test_do_update(self, test_common_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update, 'succeed_update_options')

        DUT = dmOptions()
        DUT.do_connect(test_common_dao)
        DUT.do_select_all({'site_id': 1})

        DUT.tree.get_node(1).data['siteinfo'].hardware_enabled = 0
        DUT.tree.get_node(1).data['siteinfo'].vandv_enabled = 0
        DUT.do_update(1, table='siteinfo')

        pub.unsubscribe(self.on_succeed_update, 'succeed_update_options')

        assert DUT.tree.get_node(1).data['siteinfo'].hardware_enabled == 0
        assert DUT.tree.get_node(1).data['siteinfo'].vandv_enabled == 0

        DUT.tree.get_node(1).data['siteinfo'].hardware_enabled = 1
        DUT.tree.get_node(1).data['siteinfo'].vandv_enabled = 1
        DUT.do_update(1, table='siteinfo')

        assert DUT.tree.get_node(1).data['siteinfo'].hardware_enabled == 1
        assert DUT.tree.get_node(1).data['siteinfo'].vandv_enabled == 1

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_common_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_fail_update_options_wrong_data_type,
                      'fail_update_options')

        DUT = dmOptions()
        DUT.do_connect(test_common_dao)
        DUT.do_select_all({'site_id': 1})

        DUT.tree.get_node(1).data['siteinfo'].hardware_enabled = {0: 1}
        DUT.do_update(1, table='siteinfo')

        pub.unsubscribe(self.on_fail_update_options_wrong_data_type,
                        'fail_update_options')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_common_dao):
        """do_update() should return a zero error code on success."""
        DUT = dmOptions()
        DUT.do_connect(test_common_dao)
        DUT.do_select_all({'site_id': 1})

        DUT.tree.get_node(1).data['siteinfo'].hardware_enabled = {0: 1}
        DUT.do_update(0, table='siteinfo')
