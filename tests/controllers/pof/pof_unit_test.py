# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.pof.pof_unit_test.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmPoF
from ramstk.db.base import BaseDatabase


class TestCreateControllers:
    """Class for controller initialization test suite."""

    @pytest.mark.unit
    def test_data_manager_create(self):
        """__init__() should return a PoF data manager."""
        DUT = dmPoF()

        assert isinstance(DUT, dmPoF)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == "pofs"
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert pub.isSubscribed(
            DUT.do_set_mechanism_tree, "succeed_retrieve_mechanisms"
        )
        assert pub.isSubscribed(DUT.do_set_opload_tree, "succeed_retrieve_oploads")
        assert pub.isSubscribed(DUT.do_set_opstress_tree, "succeed_retrieve_opstresss")
        assert pub.isSubscribed(
            DUT.do_set_test_method_tree, "succeed_retrieve_test_methods"
        )
        assert pub.isSubscribed(DUT.do_set_mechanism_tree, "succeed_delete_mechanism")
        assert pub.isSubscribed(DUT.do_set_opload_tree, "succeed_delete_opload")
        assert pub.isSubscribed(DUT.do_set_opstress_tree, "succeed_delete_opstress")
        assert pub.isSubscribed(
            DUT.do_set_test_method_tree, "succeed_delete_test_method"
        )
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_mechanism")
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_opload")
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_opstress")
        assert pub.isSubscribed(DUT._on_insert, "succeed_insert_test_method")
