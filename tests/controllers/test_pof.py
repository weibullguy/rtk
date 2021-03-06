# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.controllers.test_pof.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing PoF algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmPoF
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import (
    RAMSTKMechanism, RAMSTKMode, RAMSTKOpLoad,
    RAMSTKOpStress, RAMSTKTestMethod
)


@pytest.mark.usefixtures('test_program_dao')
class TestCreateControllers():
    """Class for controller initialization test suite."""
    @pytest.mark.unit
    def test_data_manager(self):
        """__init__() should return a PoF data manager."""
        DUT = dmPoF()

        assert isinstance(DUT, dmPoF)
        assert isinstance(DUT.tree, Tree)
        assert isinstance(DUT.dao, BaseDatabase)
        assert DUT._tag == 'pofs'
        assert DUT._root == 0
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert DUT.last_id == {'opload': 0, 'opstress': 0, 'testmethod': 0}
        assert pub.isSubscribed(DUT.do_select_all, 'selected_hardware')
        assert pub.isSubscribed(DUT._do_delete, 'request_delete_pof')
        assert pub.isSubscribed(DUT._do_insert_opload,
                                'request_insert_pof_opload')
        assert pub.isSubscribed(DUT._do_insert_opstress,
                                'request_insert_pof_opstress')
        assert pub.isSubscribed(DUT._do_insert_testmethod,
                                'request_insert_pof_testmethod')
        assert pub.isSubscribed(DUT.do_update, 'request_update_pof')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_mode_attributes')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_mechanism_attributes')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_opload_attributes')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_opstress_attributes')
        assert pub.isSubscribed(DUT.do_get_attributes,
                                'request_get_test_method_attributes')
        assert pub.isSubscribed(DUT.do_get_tree, 'request_get_pof_tree')
        assert pub.isSubscribed(DUT.do_set_attributes,
                                'request_set_pof_attributes')


@pytest.mark.usefixtures('test_program_dao')
class TestSelectMethods():
    """Class for testing data manager select_all() and select() methods."""
    def on_succeed_retrieve_pof(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node('4').data['mode'], RAMSTKMode)
        print("\033[36m\nsucceed_retrieve_pof topic was broadcast.")

    @pytest.mark.integration
    def test_do_select_all(self, test_program_dao):
        """do_select_all() should return a Tree() object populated with
        RAMSTKMode, RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and
        RAMSTKTestMethod instances on success."""
        pub.subscribe(self.on_succeed_retrieve_pof, 'succeed_retrieve_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        assert isinstance(DUT.tree.get_node('4').data['mode'], RAMSTKMode)

        pub.unsubscribe(self.on_succeed_retrieve_pof, 'succeed_retrieve_pof')

    @pytest.mark.integration
    def test_do_select_mode(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKMode on
        success."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        _mode = DUT.do_select('4', table='mode')

        assert isinstance(_mode, RAMSTKMode)
        assert _mode.effect_probability == 1.0
        assert _mode.mission == 'Default Mission'

    @pytest.mark.integration
    def test_do_select_mechanism(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKMechanism on
        success."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        _mechanism = DUT.do_select('4.1', table='mechanism')

        assert isinstance(_mechanism, RAMSTKMechanism)
        assert _mechanism.pof_include == 1
        assert _mechanism.rpn_detection_new == 7

    @pytest.mark.integration
    def test_do_select_opload(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKOpLoad on
        success."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        _opload = DUT.do_select('4.1.1', table='opload')

        assert isinstance(_opload, RAMSTKOpLoad)
        assert _opload.description == 'Test Operating Load'
        assert _opload.damage_model == ''

    @pytest.mark.integration
    def test_do_select_opstress(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKOpStress on
        success."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        _opstress = DUT.do_select('4.1.1.1.s', table='opstress')

        assert isinstance(_opstress, RAMSTKOpStress)
        assert _opstress.description == 'Test Operating Stress'
        assert _opstress.load_history == ''

    @pytest.mark.integration
    def test_do_select_test_method(self, test_program_dao):
        """do_select() should return an instance of the RAMSTKTestMethod on
        success."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        _method = DUT.do_select('4.1.1.1.t', table='testmethod')

        assert isinstance(_method, RAMSTKTestMethod)
        assert _method.description == 'Test Test Method'
        assert _method.boundary_conditions == ''

    @pytest.mark.integration
    def test_do_select_unknown_table(self, test_program_dao):
        """do_select() should raise a KeyError when an unknown table name is
        requested."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        with pytest.raises(KeyError):
            DUT.do_select('4', table='scibbidy-bibbidy-doo')

    @pytest.mark.integration
    def test_do_select_non_existent_id(self, test_program_dao):
        """do_select() should return None when a non-existent PoF ID is
        requested."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        assert DUT.do_select(100, table='mode') is None


@pytest.mark.usefixtures('test_program_dao')
class TestDeleteMethods():
    """Class for testing the data manager delete() method."""
    def on_succeed_delete_mode(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_pof topic was broadcast when deleting "
              "a failure mode.")

    def on_succeed_delete_mechanism(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_pof topic was broadcast when deleting "
              "a failure mechanism.")

    def on_succeed_delete_opload(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_pof topic was broadcast when deleting "
              "an operating load.")

    def on_succeed_delete_opstress(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_delete_pof topic was broadcast when deleting "
              "an operating stress.")

    def on_succeed_delete_test_method(self, tree):
        assert isinstance(tree, Tree)
        print(
            "\033[36m\nsucceed_delete_pof topic was broadcast when deleting a "
            "test method.")

    def on_fail_delete_pof(self, error_message):
        assert error_message == (
            '_do_delete: Attempted to delete non-existent PoF record with '
            'ID 300.')
        print("\033[35m\nfail_delete_pof topic was broadcast.")

    @pytest.mark.integration
    def test_do_delete_test_method(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting a test method."""
        pub.subscribe(self.on_succeed_delete_test_method, 'succeed_delete_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_delete('4.1.1.1.t')

        assert DUT.tree.get_node('4.1.1.1.t') is None

        pub.unsubscribe(self.on_succeed_delete_test_method,
                        'succeed_delete_pof')

    @pytest.mark.integration
    def test_do_delete_opstress(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting an operating stress."""
        pub.subscribe(self.on_succeed_delete_opstress, 'succeed_delete_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_delete('4.1.1.1.s')

        assert DUT.tree.get_node('4.1.1.1.s') is None

        pub.unsubscribe(self.on_succeed_delete_opstress, 'succeed_delete_pof')

    @pytest.mark.integration
    def test_do_delete_opload(self, test_program_dao):
        """_do_delete() should send the success message with the treelib Tree
        when successfully deleting on operating load."""
        pub.subscribe(self.on_succeed_delete_opload, 'succeed_delete_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_delete('4.1.1')

        assert DUT.tree.get_node('4.1.1') is None

        pub.unsubscribe(self.on_succeed_delete_opload, 'succeed_delete_pof')

    @pytest.mark.integration
    def test_do_delete_mechanism(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_mechanism, 'succeed_delete_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_delete('4.1')

        assert DUT.tree.get_node('4.1') is None

        pub.unsubscribe(self.on_succeed_delete_mechanism, 'succeed_delete_pof')

    @pytest.mark.integration
    def test_do_delete_mode(self, test_program_dao):
        """_do_delete() should send the success message with the treelib
        Tree."""
        pub.subscribe(self.on_succeed_delete_mode, 'succeed_delete_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_delete('4')

        assert DUT.tree.get_node('4') is None

        pub.unsubscribe(self.on_succeed_delete_mode, 'succeed_delete_pof')

    @pytest.mark.integration
    def test_do_delete_non_existent_id(self, test_program_dao):
        """_do_delete() should send the fail message when attempting to delete
        a node ID that doesn't exist in the tree."""
        pub.subscribe(self.on_fail_delete_pof, 'fail_delete_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_delete('300')

        pub.unsubscribe(self.on_fail_delete_pof, 'fail_delete_pof')


@pytest.mark.usefixtures('test_program_dao')
class TestInsertMethods():
    """Class for testing the data manager insert() method."""
    def on_succeed_insert_opload(self, node_id, tree):
        assert isinstance(tree, Tree)
        assert node_id == '5.1.2'
        print("\033[36m\nsucceed_insert_opload topic was broadcast.")

    def on_fail_insert_opload(self, error_message):
        assert error_message == (
            'An error occurred when attempting to add an operating load to '
            'failure mechanism ID 40.')
        print("\033[35m\nfail_insert_opload topic was broadcast.")

    def on_succeed_insert_opstress(self, node_id, tree):
        assert isinstance(tree, Tree)
        assert node_id == '5.1.1.2.s'
        print("\033[36m\nsucceed_insert_opstress topic was broadcast.")

    def on_fail_insert_opstress(self, error_message):
        assert error_message == ('An error occurred when attempting to add an '
                                 'operating stress to operating load ID 40.')
        print("\033[35m\nfail_insert_opstress topic was broadcast.")

    def on_succeed_insert_test_method(self, node_id, tree):
        assert isinstance(tree, Tree)
        assert node_id == '5.1.1.2.t'
        print("\033[36m\nsucceed_insert_test_method topic was broadcast.")

    def on_fail_insert_test_method(self, error_message):
        assert error_message == ('An error occurred when attempting to add a '
                                 'test method to operating load ID 40.')
        print("\033[35m\nfail_insert_test_method topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert_opload(self, test_program_dao):
        """_do_insert_opload() should send the success message after
        successfully inserting an operating load."""
        pub.subscribe(self.on_succeed_insert_opload, 'succeed_insert_opload')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        DUT._do_insert_opload('5.1')

        assert isinstance(
            DUT.tree.get_node('5.1.1').data['opload'], RAMSTKOpLoad)
        assert DUT.tree.get_node('5.1.1').data['opload'].load_id == 1
        assert DUT.tree.get_node('5.1.1').data['opload'].description == ''

        pub.unsubscribe(self.on_succeed_insert_opload, 'succeed_insert_opload')

    @pytest.mark.integration
    def test_do_insert_opload_no_mechanism(self, test_program_dao):
        """_do_insert_opload() should send the fail message if attempting to
        add an operating load to a non-existent mechanism ID."""
        pub.subscribe(self.on_fail_insert_opload, 'fail_insert_opload')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_insert_opload('4.40')

        assert DUT.tree.get_node('4.40') is None

        pub.unsubscribe(self.on_fail_insert_opload, 'fail_insert_opload')

    @pytest.mark.integration
    def test_do_insert_opstress(self, test_program_dao):
        """_do_insert_opstress() should send the success message after
        successfully inserting an operating stress."""
        pub.subscribe(self.on_succeed_insert_opstress,
                      'succeed_insert_opstress')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_insert_opstress('5.1.1')

        assert isinstance(
            DUT.tree.get_node('5.1.1.1.s').data['opstress'], RAMSTKOpStress)
        assert DUT.tree.get_node('5.1.1.1.s').data['opstress'].stress_id == 1
        assert DUT.tree.get_node(
            '5.1.1.1.s').data['opstress'].description == ''

        pub.unsubscribe(self.on_succeed_insert_opstress,
                        'succeed_insert_opstress')

    @pytest.mark.integration
    def test_do_insert_opstress_no_load(self, test_program_dao):
        """_do_insert_opstress() should send the fail message if attempting to
        add a control to a non-existent operating load ID."""
        pub.subscribe(self.on_fail_insert_opstress, 'fail_insert_opstress')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_insert_opstress('4.1.40')

        assert DUT.tree.get_node('4.1.40') is None

        pub.unsubscribe(self.on_fail_insert_opstress, 'fail_insert_opstress')

    @pytest.mark.integration
    def test_do_insert_test_method(self, test_program_dao):
        """_do_insert_testmethod() should send the success message after
        successfully inserting a test method."""
        pub.subscribe(self.on_succeed_insert_test_method,
                      'succeed_insert_test_method')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_insert_testmethod('5.1.1')

        assert isinstance(
            DUT.tree.get_node('5.1.1.1.t').data['testmethod'],
            RAMSTKTestMethod)
        assert DUT.tree.get_node('5.1.1.1.t').data['testmethod'].test_id == 1
        assert DUT.tree.get_node(
            '5.1.1.1.t').data['testmethod'].description == ''

        pub.unsubscribe(self.on_succeed_insert_test_method,
                        'succeed_insert_test_method')

    @pytest.mark.integration
    def test_do_insert_test_method_no_cause(self, test_program_dao):
        """_do_insert_testmethod() should send the fail message if attempting
        to add an action to a non-existent cause ID."""
        pub.subscribe(self.on_fail_insert_test_method,
                      'fail_insert_test_method')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT._do_insert_testmethod('4.1.40')

        assert DUT.tree.get_node('4.1.40') is None

        pub.unsubscribe(self.on_fail_insert_test_method,
                        'fail_insert_test_method')


@pytest.mark.usefixtures('test_program_dao')
class TestGetterSetter():
    """Class for testing methods that get or set."""
    def on_succeed_get_mode_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['mode_id'] == 5
        # When this script is run by itself, the first response is expected.
        # When run with make test as part of the complete test suite,
        # the test_fmea.py script will have previously updated the description
        # to the second.
        try:
            assert attributes['description'] == 'System Test Failure Mode #2'
        except AssertionError:
            assert attributes['description'] == 'Test failure mode'
        assert attributes['critical_item'] == 0
        print("\033[36m\nsucceed_get_mode_attributes topic was broadcast.")

    def on_succeed_get_mechanism_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['mechanism_id'] == 1
        # When this script is run by itself, the first response is expected.
        # When run with make test as part of the complete test suite,
        # the test_fmea.py script will have previously updated the description
        # to the second.
        try:
            assert attributes['description'] == ('Test Failure Mechanism #1 '
                                                 'for Mode ID 5')
        except AssertionError:
            assert attributes['description'] == ('Test failure mechanism, '
                                                 'updated')
        print(
            "\033[36m\nsucceed_get_mechanism_attributes topic was broadcast.")

    def on_succeed_get_opload_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['load_id'] == 1
        assert attributes['description'] == ''
        print("\033[36m\nsucceed_get_opload_attributes topic was broadcast.")

    def on_succeed_get_opstress_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['stress_id'] == 1
        assert attributes['description'] == ''
        print("\033[36m\nsucceed_get_opstress_attributes topic was broadcast.")

    def on_succeed_get_test_method_attrs(self, attributes):
        assert isinstance(attributes, dict)
        assert attributes['test_id'] == 1
        assert attributes['description'] == ''
        print(
            "\033[36m\nsucceed_get_test_method_attributes topic was broadcast."
        )

    def on_succeed_get_pof_tree(self, tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node('5').data['mode'], RAMSTKMode)
        assert isinstance(
            tree.get_node('5.1').data['mechanism'], RAMSTKMechanism)
        print("\033[36m\nsucceed_get_pof_tree topic was broadcast")

    @pytest.mark.integration
    def test_do_get_mode_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of mode attributes on
        success."""
        pub.subscribe(self.on_succeed_get_mode_attrs,
                      'succeed_get_mode_attributes')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_get_attributes('5', 'mode')

        assert isinstance(DUT.tree.get_node('5').data['mode'], RAMSTKMode)

        pub.unsubscribe(self.on_succeed_get_mode_attrs,
                        'succeed_get_mode_attributes')

    @pytest.mark.integration
    def test_do_get_mechanism_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of mechanism attributes on
        success."""
        pub.subscribe(self.on_succeed_get_mechanism_attrs,
                      'succeed_get_mechanism_attributes')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_get_attributes('5.1', 'mechanism')

        assert isinstance(
            DUT.tree.get_node('5.1').data['mechanism'], RAMSTKMechanism)

        pub.unsubscribe(self.on_succeed_get_mechanism_attrs,
                        'succeed_get_mechanism_attributes')

    @pytest.mark.integration
    def test_do_get_opload_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of operating load
        attributes on success."""
        pub.subscribe(self.on_succeed_get_opload_attrs,
                      'succeed_get_opload_attributes')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_get_attributes('5.1.1', 'opload')

        assert isinstance(
            DUT.tree.get_node('5.1.1').data['opload'], RAMSTKOpLoad)

        pub.unsubscribe(self.on_succeed_get_opload_attrs,
                        'succeed_get_opload_attributes')

    @pytest.mark.integration
    def test_do_get_opstress_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of operating stress
        attributes on success."""
        pub.subscribe(self.on_succeed_get_opstress_attrs,
                      'succeed_get_opstress_attributes')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_get_attributes('5.1.1.1.s', 'opstress')

        assert isinstance(
            DUT.tree.get_node('5.1.1.1.s').data['opstress'], RAMSTKOpStress)

        pub.unsubscribe(self.on_succeed_get_opstress_attrs,
                        'succeed_get_opstress_attributes')

    @pytest.mark.integration
    def test_do_get_test_method_attributes(self, test_program_dao):
        """do_get_attributes() should return a dict of test method attributes
        on success."""
        pub.subscribe(self.on_succeed_get_test_method_attrs,
                      'succeed_get_test_method_attributes')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_get_attributes('5.1.1.1.t', 'testmethod')

        assert isinstance(
            DUT.tree.get_node('5.1.1.1.t').data['testmethod'],
            RAMSTKTestMethod)

        pub.unsubscribe(self.on_succeed_get_test_method_attrs,
                        'succeed_get_test_method_attributes')

    @pytest.mark.integration
    def test_do_set_opload_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        operating load attributes."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        DUT.do_set_attributes(node_id=['5.1.1', -1],
                              package={'damage_model': 'Fancy math model'})
        DUT.do_set_attributes(node_id=['5.1.1', -1],
                              package={'description': 'Jared Kushner'})
        assert DUT.do_select('5.1.1',
                             table='opload').description == 'Jared Kushner'
        assert DUT.do_select(
            '5.1.1', table='opload').damage_model == ('Fancy math model')

        pub.unsubscribe(DUT.do_set_attributes, 'request_set_pof_attributes')

    @pytest.mark.integration
    def test_do_set_opstress_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        control attributes."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        DUT.do_set_attributes(node_id=['5.1.1.1.s', -1],
                              package={'load_history': 'Waterfall histogram'})
        DUT.do_set_attributes(node_id=['5.1.1.1.s', -1],
                              package={'description': 'Lock and chain'})
        assert DUT.do_select('5.1.1.1.s',
                             table='opstress').description == 'Lock and chain'
        assert DUT.do_select(
            '5.1.1.1.s',
            table='opstress').load_history == ('Waterfall histogram')

        pub.unsubscribe(DUT.do_set_attributes, 'request_set_pof_attributes')

    @pytest.mark.integration
    def test_do_set_test_method_attributes(self, test_program_dao):
        """do_set_attributes() should return None when successfully setting
        test method attributes."""
        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        DUT.do_set_attributes(node_id=['5.1.1.1.t', -1],
                              package={'description': 'Kick his ass'})
        DUT.do_set_attributes(node_id=['5.1.1.1.t', -1],
                              package={'remarks': 'Doyle Rowland'})
        assert DUT.do_select('5.1.1.1.t',
                             table='testmethod').description == 'Kick his ass'
        assert DUT.do_select('5.1.1.1.t',
                             table='testmethod').remarks == 'Doyle Rowland'

        pub.unsubscribe(DUT.do_set_attributes, 'request_set_pof_attributes')

    @pytest.mark.integration
    def test_on_get_tree_data_manager(self, test_program_dao):
        """on_get_tree() should return the PoF treelib Tree."""
        pub.subscribe(self.on_succeed_get_pof_tree, 'succeed_get_pof_tree')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_get_tree()

        pub.unsubscribe(self.on_succeed_get_pof_tree, 'succeed_get_pof_tree')


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods():
    """Class for testing update() and update_all() methods."""
    def on_succeed_update_pof(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_pof topic was broadcast")

    def on_fail_update_pof(self, error_message):
        assert error_message == (
            'do_update: Attempted to save non-existent PoF record ID 100.')
        print("\033[35m\nfail_update_pof topic was broadcast")

    def on_fail_update_pof_no_data(self, error_message):
        assert error_message == ('do_update: No data package found for PoF '
                                 'record ID 5.1.1.')
        print("\033[35m\nfail_update_pof topic was broadcast")

    def on_fail_update_pof_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for PoF record '
            'ID 5.1.1 was the wrong type.')
        print("\033[35m\nfail_update_pof topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """do_update() should return a zero error code on success."""
        pub.subscribe(self.on_succeed_update_pof, 'succeed_update_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        DUT.tree.get_node('5').data['mode'].description = 'Test failure mode'
        DUT.tree.get_node('5').data['mode'].operator_actions = (
            'Take evasive actions.')
        DUT.tree.get_node('5.1').data[
            'mechanism'].description = 'Test failure mechanism, updated'
        DUT.tree.get_node(
            '5.1.1').data['opload'].description = 'Test Operating Load'
        DUT.tree.get_node('5.1.1').data['opload'].damage_model = ''
        DUT.do_update('5')

        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        assert DUT.tree.get_node('5').data['mode'].description == (
            'Test failure mode')
        assert DUT.tree.get_node('5').data['mode'].operator_actions == (
            'Take evasive actions.')
        assert DUT.tree.get_node('5.1').data['mechanism'].description == (
            'Test failure mechanism, updated')
        assert DUT.tree.get_node('5.1.1').data['opload'].description == (
            'Test Operating Load')

        pub.unsubscribe(self.on_succeed_update_pof, 'succeed_update_pof')

    @pytest.mark.integration
    def test_do_update_non_existent_id(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a PoF ID
        that doesn't exist."""
        pub.subscribe(self.on_fail_update_pof, 'fail_update_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})
        DUT.do_update(100)

        pub.unsubscribe(self.on_fail_update_pof, 'fail_update_pof')

    @pytest.mark.integration
    def test_do_update_no_data_package(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a FMEA
        ID that has no data package."""
        pub.subscribe(self.on_fail_update_pof_no_data, 'fail_update_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        DUT.tree.get_node('5.1.1').data.pop('opload')

        DUT.do_update('5.1.1')

        pub.unsubscribe(self.on_fail_update_pof_no_data, 'fail_update_pof')

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should return a non-zero error code when passed a
        Requirement ID that doesn't exist."""
        pub.subscribe(self.on_fail_update_pof_wrong_data_type,
                      'fail_update_pof')

        DUT = dmPoF()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all({'revision_id': 1, 'hardware_id': 1})

        _opload = DUT.do_select('5.1.1', table='opload')
        _pri = _opload.priority_id
        _opload.priority_id = {1: 2}

        DUT.do_update('5.1.1')

        _opload.priority_id = _pri

        pub.unsubscribe(self.on_fail_update_pof_wrong_data_type,
                        'fail_update_pof')
