# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.usage_profile.usage_profile_unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing Usage Profile module algorithms and models."""

# Third Party Imports
# noinspection PyPackageRequirements
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmUsageProfile
from ramstk.db.base import BaseDatabase


# noinspection PyPep8Naming
class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a Revision data manager."""
        DUT = dmUsageProfile()

        assert isinstance(DUT, dmUsageProfile)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "usage_profiles"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(
            DUT.do_set_environment_tree, "succeed_retrieve_environments"
        )
        assert pub.isSubscribed(DUT.do_set_mission_tree, "succeed_retrieve_missions")
        assert pub.isSubscribed(
            DUT.do_set_mission_phase_tree, "succeed_retrieve_mission_phases"
        )
        assert pub.isSubscribed(
            DUT.do_set_environment_tree, "succeed_delete_environment"
        )
        assert pub.isSubscribed(DUT.do_set_mission_tree, "succeed_delete_mission")
        assert pub.isSubscribed(
            DUT.do_set_mission_phase_tree, "succeed_delete_mission_phase"
        )
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_environment")
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_mission")
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_mission_phase")
