# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.options.options_unit_test.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Options module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mocks import MockDAO
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmOptions
from ramstk.db.base import BaseDatabase
from ramstk.models.commondb import RAMSTKSiteInfo


@pytest.fixture
def mock_common_dao(monkeypatch):
    _site_1 = RAMSTKSiteInfo()
    _site_1.site_id = 1
    _site_1.site_name = 'DEMO SITE'
    _site_1.product_key = 'DEMO'
    _site_1.expire_on = date.today() + timedelta(30)
    _site_1.function_enabled = 1
    _site_1.requirement_enabled = 1
    _site_1.hardware_enabled = 1
    _site_1.software_enabled = 0
    _site_1.rcm_enabled = 0
    _site_1.testing_enabled = 0
    _site_1.incident_enabled = 0
    _site_1.survival_enabled = 0
    _site_1.vandv_enabled = 1
    _site_1.hazard_enabled = 1
    _site_1.stakeholder_enabled = 1
    _site_1.allocation_enabled = 1
    _site_1.similar_item_enabled = 1
    _site_1.fmea_enabled = 1
    _site_1.pof_enabled = 1
    _site_1.rbd_enabled = 0
    _site_1.fta_enabled = 0

    DAO = MockDAO()
    DAO.table = [
        _site_1,
    ]

    yield DAO


class TestCreateControllers:
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager_create(self, mock_common_dao):
        """__init__() should return a Options data manager."""
        DUT = dmOptions()

        assert isinstance(DUT, dmOptions)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._pkey == {
            'siteinfo': ['site_id'],
        }
        assert DUT._tag == 'options'
        assert DUT._root == 0
        assert DUT._site_id == 0

        assert pub.isSubscribed(DUT.do_update, 'request_update_option')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_option_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_options_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_option_attributes')


class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['siteinfo'], RAMSTKSiteInfo)
        # There should be a root node with no data package and a node with
        # the one RAMSTKSiteInfo record.
        assert len(tree.all_nodes()) == 2
        print("\033[36m\nsucceed_retrieve_options topic was broadcast.")

    @pytest.mark.unit
    def test_do_select_all(self, mock_common_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKProgramInfo and RAMSTKSiteInfo instances on success."""
        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_options')

        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})

        pub.unsubscribe(self.on_succeed_select_all, 'succeed_retrieve_options')

    @pytest.mark.unit
    def test_do_select_all_populated_tree(self, mock_common_dao):
        """do_select_all() should clear nodes from an existing Options tree."""
        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})

        pub.subscribe(self.on_succeed_select_all, 'succeed_retrieve_options')

        DUT.do_select_all({'site_id': 1})

        pub.unsubscribe(self.on_succeed_select_all, 'succeed_retrieve_options')

    @pytest.mark.unit
    def test_do_select(self, mock_common_dao):
        """do_select() should return an instance of the RAMSTKSiteInfo on
        success."""
        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})

        _options = DUT.do_select(1, table='siteinfo')

        assert isinstance(_options, RAMSTKSiteInfo)
        assert _options.site_id == 1
        assert _options.site_name == 'DEMO SITE'
        assert _options.product_key == 'DEMO'
        assert _options.expire_on == date.today() + timedelta(30)
        assert _options.function_enabled == 1
        assert _options.requirement_enabled == 1
        assert _options.hardware_enabled == 1
        assert _options.software_enabled == 0
        assert _options.rcm_enabled == 0
        assert _options.testing_enabled == 0
        assert _options.incident_enabled == 0
        assert _options.survival_enabled == 0
        assert _options.vandv_enabled == 1
        assert _options.hazard_enabled == 1
        assert _options.stakeholder_enabled == 1
        assert _options.allocation_enabled == 1
        assert _options.similar_item_enabled == 1
        assert _options.fmea_enabled == 1
        assert _options.pof_enabled == 1
        assert _options.rbd_enabled == 0
        assert _options.fta_enabled == 0

    @pytest.mark.unit
    def test_do_select_unknown_table(self, mock_common_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select(1, table='scibbidy-bibbidy-doo')

    @pytest.mark.unit
    def test_do_select_non_existent_id(self, mock_common_dao):
        """do_select() should return None when a non-existent Options ID is
        requested."""
        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})

        assert DUT.do_select(100, table='siteinfo') is None


class TestGetterSetter:
    """Class for testing methods that get or set."""
    def on_succeed_get_attributes(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['function_enabled'] == 1
        assert attributes['requirement_enabled'] == 1
        assert attributes['hardware_enabled'] == 1
        assert attributes['software_enabled'] == 0
        assert attributes['rcm_enabled'] == 0
        assert attributes['testing_enabled'] == 0
        assert attributes['incident_enabled'] == 0
        assert attributes['survival_enabled'] == 0
        assert attributes['vandv_enabled'] == 1
        assert attributes['hazard_enabled'] == 1
        assert attributes['stakeholder_enabled'] == 1
        assert attributes['allocation_enabled'] == 1
        assert attributes['similar_item_enabled'] == 1
        assert attributes['fmea_enabled'] == 1
        assert attributes['pof_enabled'] == 1
        assert attributes['rbd_enabled'] == 0
        print("\033[36m\nsucceed_get_siteinfo_attributes topic was broadcast.")

    def on_succeed_get_data_manager_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['siteinfo'], RAMSTKSiteInfo)
        print("\033[36m\nsucceed_get_options_tree topic was broadcast")

    @pytest.mark.unit
    def test_do_get_attributes(self, mock_common_dao):
        """do_get_attributes() should return a dict of site information
        attributes on success."""
        pub.subscribe(self.on_succeed_get_attributes,
                      'succeed_get_siteinfo_attributes')

        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})
        DUT.do_get_attributes(1, 'siteinfo')

        pub.unsubscribe(self.on_succeed_get_attributes,
                        'succeed_get_siteinfo_attributes')

    @pytest.mark.unit
    def test_do_set_attributes(self, mock_common_dao):
        """do_set_attributes() should return None when successfully setting
        site information attributes."""
        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})

        pub.sendMessage('request_set_option_attributes',
                        node_id=[1, ''],
                        package={'function_enabled': 1})
        pub.sendMessage('request_set_option_attributes',
                        node_id=[1, ''],
                        package={'requirement_enabled': 1})
        assert DUT.do_select(1, table='siteinfo').function_enabled == 1
        assert DUT.do_select(1, table='siteinfo').requirement_enabled == 1

        pub.unsubscribe(DUT.do_set_attributes, 'request_set_option_attributes')

    @pytest.mark.unit
    def test_on_get_data_manager_tree(self, mock_common_dao):
        """on_get_tree() should return the Options treelib Tree."""
        pub.subscribe(self.on_succeed_get_data_manager_tree,
                      'succeed_get_options_tree')

        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_data_manager_tree,
                        'succeed_get_options_tree')


class TestUpdateMethods:
    """Class for testing update() and update_all() methods."""
    def on_fail_update_non_existent_id(self, error_message):
        assert error_message == ('do_update: Attempted to save non-existent '
                                 'Site ID skullduggery.')
        print("\033[35m\nfail_update_options topic was broadcast")

    def on_fail_update_no_data_package(self, error_message):
        assert error_message == ('do_update: No data package found for Site 1 '
                                 'options.')
        print("\033[35m\nfail_update_options topic was broadcast")

    @pytest.mark.unit
    def test_do_update_non_existent_id(self, mock_common_dao):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_non_existent_id,
                      'fail_update_options')

        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})
        DUT.do_update('skullduggery', table='siteinfo')

        pub.unsubscribe(self.on_fail_update_non_existent_id,
                        'fail_update_options')

    @pytest.mark.unit
    def test_do_update_no_data_package(self, mock_common_dao):
        """do_update() should return a non-zero error code when passed a
        Options ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_no_data_package,
                      'fail_update_options')

        DUT = dmOptions()
        DUT.do_connect(mock_common_dao)
        DUT.do_select_all({'site_id': 1})
        DUT.tree.get_node(1).data.pop('siteinfo')

        DUT.do_update(1, table='siteinfo')

        pub.unsubscribe(self.on_fail_update_no_data_package,
                        'fail_update_options')
