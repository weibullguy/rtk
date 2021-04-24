# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.pof_integration.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Class for testing PoF integrations."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmMechanism, dmOpLoad, dmOpStress, dmPoF, dmTestMethod
from ramstk.models.programdb import (
    RAMSTKMechanism,
    RAMSTKOpLoad,
    RAMSTKOpStress,
    RAMSTKTestMethod,
)

test_mechanism = dmMechanism()
test_opload = dmOpLoad()
test_opstress = dmOpStress()
test_test_method = dmTestMethod()


@pytest.mark.usefixtures("test_program_dao")
class TestSelectMethods:
    """Class for testing data manager select_all() and select() methods."""

    def on_succeed_select_all(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node("1").data["pof"], RAMSTKMechanism)
        assert isinstance(tree.get_node("1.1").data["pof"], RAMSTKOpLoad)
        assert isinstance(tree.get_node("1.1.1s").data["pof"], RAMSTKOpStress)
        assert isinstance(tree.get_node("1.1.1t").data["pof"], RAMSTKTestMethod)
        print("\033[36m\nsucceed_retrieve_pof topic was broadcast.")

    @pytest.mark.integration
    def test_on_select_all(self, test_program_dao):
        """on_select_all() should return a Tree() object populated with
        RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod
        instances on success."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_pof")

        DUT.do_set_test_method_tree(test_test_method.tree)
        DUT.do_set_opstress_tree(test_opstress.tree)
        DUT.do_set_opload_tree(test_opload.tree)
        DUT.do_set_mechanism_tree(test_mechanism.tree)

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_on_select_all_populated_tree(self, test_program_dao):
        """on_select_all() should return a Tree() object populated with
        RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod
        instances on success."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        DUT.do_set_opstress_tree(test_opstress.tree)
        DUT.do_set_mechanism_tree(test_mechanism.tree)
        DUT.do_set_opload_tree(test_opload.tree)
        DUT.do_set_test_method_tree(test_test_method.tree)
        DUT.on_select_all()

        pub.subscribe(self.on_succeed_select_all, "succeed_retrieve_pof")

        DUT.on_select_all()

        pub.unsubscribe(self.on_succeed_select_all, "succeed_retrieve_pof")


@pytest.mark.usefixtures("test_program_dao")
class TestDeleteMethods:
    """Class for testing the data manager delete() method."""

    @pytest.mark.integration
    def test_do_delete_test_method(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        DUT.do_set_mechanism_tree(test_mechanism.tree)
        DUT.do_set_opload_tree(test_opload.tree)
        DUT.do_set_opstress_tree(test_opstress.tree)
        DUT.do_set_test_method_tree(test_test_method.tree)

        assert DUT.tree.contains("1.1.1t")
        assert DUT.tree.contains("1.1.1s")
        assert DUT.tree.contains("1.1")
        assert DUT.tree.contains("1")

        test_test_method._do_delete(1)

        assert not DUT.tree.contains("1.1.1t")
        assert DUT.tree.contains("1.1.1s")
        assert DUT.tree.contains("1.1")
        assert DUT.tree.contains("1")

    @pytest.mark.integration
    def test_do_delete_opstress(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting an operating stress."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        DUT.do_set_mechanism_tree(test_mechanism.tree)
        DUT.do_set_opload_tree(test_opload.tree)
        DUT.do_set_opstress_tree(test_opstress.tree)
        DUT.do_set_test_method_tree(test_test_method.tree)

        assert not DUT.tree.contains("1.1.1t")
        assert DUT.tree.contains("1.1.1s")
        assert DUT.tree.contains("1.1")
        assert DUT.tree.contains("1")

        test_opstress._do_delete(1)

        assert not DUT.tree.contains("1.1.1t")
        assert not DUT.tree.contains("1.1.1s")
        assert DUT.tree.contains("1.1")
        assert DUT.tree.contains("1")

    @pytest.mark.integration
    def test_do_delete_opload(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting on operating load."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        DUT.do_set_test_method_tree(test_test_method.tree)
        DUT.do_set_opstress_tree(test_opstress.tree)
        DUT.do_set_opload_tree(test_opload.tree)
        DUT.do_set_mechanism_tree(test_mechanism.tree)

        assert not DUT.tree.contains("1.1.1t")
        assert not DUT.tree.contains("1.1.1s")
        assert DUT.tree.contains("1.1")
        assert DUT.tree.contains("1")

        test_opload._do_delete(1)

        assert not DUT.tree.contains("1.1.1t")
        assert not DUT.tree.contains("1.1.1s")
        assert not DUT.tree.contains("1.1")
        assert DUT.tree.contains("1")


@pytest.mark.usefixtures("test_program_dao")
class TestInsertMethods:
    """Class for testing the data manager insert() method."""

    def on_succeed_insert_opload(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("5.1.2")
        print("\033[36m\nsucceed_insert_opload topic was broadcast.")

    def on_fail_insert_no_mechanism(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            "returned:\n\tKey (fld_revision_id, fld_hardware_id, fld_mode_id, "
            "fld_mechanism_id)=(1, 1, 6, 40) is not present in table "
            '"ramstk_mechanism".'
        )
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    def on_succeed_insert_opstress(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("5.1.1.2.s")
        print("\033[36m\nsucceed_insert_opstress topic was broadcast.")

    def on_fail_insert_no_opload(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            'returned:\n\t"1.40"\nLINE 1'
        )
        print("\033[35m\nfail_insert_opstress topic was broadcast.")

    def on_succeed_insert_test_method(self, tree):
        assert isinstance(tree, Tree)
        assert tree.contains("5.1.1.2.t")
        print("\033[36m\nsucceed_insert_test_method topic was broadcast.")

    def on_fail_insert_no_opstress(self, error_message):
        assert error_message == (
            "do_insert: Database error when attempting to add a record.  Database "
            'returned:\n\t"1.1.40"\nLINE 1'
        )
        print("\033[35m\nfail_insert_test_method topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_opload(self, test_program_dao):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_succeed_insert_opload, "succeed_retrieve_pof")
        pub.sendMessage("request_insert_opload", parent_id=1)
        pub.unsubscribe(self.on_succeed_insert_opload, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_opload_no_mechanism(self, test_program_dao):
        """_do_insert_opload() should send the fail message if attempting to
        add an operating load to a non-existent mechanism ID."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_fail_insert_no_mechanism, "fail_insert_opload")
        pub.sendMessage("request_insert_opload", parent_id=40)
        pub.unsubscribe(self.on_fail_insert_no_mechanism, "fail_insert_opload")

    @pytest.mark.integration
    def test_do_insert_opstress(self, test_program_dao):
        """_do_insert_opstress() should send the success message after
        successfully inserting an operating stress."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_succeed_insert_opstress, "succeed_retrieve_pof")
        pub.sendMessage("request_insert_opstress", parent_id="1.1")
        pub.unsubscribe(self.on_succeed_insert_opstress, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_opstress_no_opload(self, test_program_dao):
        """_do_insert_opstress() should send the fail message if attempting to
        add a control to a non-existent operating load ID."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_fail_insert_no_opload, "fail_insert_opstress")
        pub.sendMessage("request_insert_opstress", parent_id="1.40")
        pub.unsubscribe(self.on_fail_insert_no_opload, "fail_insert_opstress")

    @pytest.mark.integration
    def test_do_insert_test_method(self, test_program_dao):
        """_do_insert_testmethod() should send the success message after
        successfully inserting a test method."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_succeed_insert_test_method, "succeed_retrieve_pof")
        pub.sendMessage("request_insert_test_method", parent_id="1.1.2")
        pub.unsubscribe(self.on_succeed_insert_test_method, "succeed_retrieve_pof")

    @pytest.mark.integration
    def test_do_insert_test_method_no_opstress(self, test_program_dao):
        """_do_insert_testmethod() should send the fail message if attempting
        to add an action to a non-existent opstress ID."""
        test_mechanism.do_connect(test_program_dao)
        test_opload.do_connect(test_program_dao)
        test_opstress.do_connect(test_program_dao)
        test_test_method.do_connect(test_program_dao)

        test_mechanism.do_select_all(
            attributes={"revision_id": 1, "hardware_id": 1, "mode_id": 6}
        )
        test_opload.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
            }
        )
        test_opstress.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
            }
        )
        test_test_method.do_select_all(
            attributes={
                "revision_id": 1,
                "hardware_id": 1,
                "mode_id": 6,
                "mechanism_id": 1,
                "load_id": 1,
                "stress_id": 1,
            }
        )

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)

        pub.subscribe(self.on_fail_insert_no_opstress, "fail_insert_test_method")
        pub.sendMessage("request_insert_test_method", parent_id="1.1.40")
        pub.unsubscribe(self.on_fail_insert_no_opstress, "fail_insert_test_method")
