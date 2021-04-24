# -*- coding: utf-8 -*-
#
#       ramstk.controllers.allocation.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Controller Package analysis manager."""

# Standard Library Imports
import inspect
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import allocation
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the Allocation analysis manager.

    This class manages the allocation analysis for allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the allocation Analysis Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the allocation item being analyzed.
    """

    # Define private scalar class attributes.
    _system_hazard_rate: float = 0.0

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[Any, Any]) -> None:
        """Initialize an instance of the allocation analysis manager.

        :param configuration: the RAMSTKUserConfiguration instance associated
            with the current instance of the RAMSTK application.
        """
        super().__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._node_hazard_rate: float = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_get_all_attributes,
                      'succeed_get_allocation_attributes')
        pub.subscribe(super().on_get_tree, 'succeed_get_allocation_tree')
        pub.subscribe(super().on_get_tree, 'succeed_retrieve_allocation')
        pub.subscribe(super().on_get_tree, 'succeed_update_allocation')

        pub.subscribe(self._do_calculate_allocation,
                      'request_allocate_reliability')
        pub.subscribe(self._do_calculate_allocation_goals,
                      'request_calculate_allocation_goals')
        pub.subscribe(self._do_calculate_allocation,
                      'request_calculate_allocation')
        pub.subscribe(self._on_get_hardware_attributes,
                      'succeed_get_all_hardware_attributes')

    def _do_calculate_agree_allocation(self, node: treelib.Node) -> None:
        """Allocate reliability using the AGREE method.

        :param node: the treelib.Node() whose reliability is to be allocated.
        :return: None
        :rtype: None
        """
        _parent_goal = node.data['allocation'].reliability_goal
        _method_id = node.data['allocation'].allocation_method_id

        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)

            _attributes: Dict[str,
                              Any] = _node.data['allocation'].get_attributes()
            _attributes['allocation_method_id'] = _method_id

            (_attributes['n_sub_elements'], _attributes['n_sub_systems']
             ) = self._do_calculate_agree_total_elements(node)

            _attributes = allocation.do_allocate_reliability(
                _parent_goal, 0, **_attributes)

            _node.data['allocation'].hazard_rate_alloc = _attributes[
                'hazard_rate_alloc']
            _node.data['allocation'].mtbf_alloc = _attributes['mtbf_alloc']
            _node.data['allocation'].reliability_alloc = _attributes[
                'reliability_alloc']

            _parent_goal = _node.data['allocation'].reliability_goal

    def _do_calculate_agree_total_elements(
            self, node: treelib.Node) -> Tuple[int, int]:
        """Calculate the total number of elements for the AGREE method.

        :param node: the treelib.Node() of the allocation item whose goal is
            to be allocated.
        :return: _n_sub_elements, _n_sub_systems; the number of
            subelements and subsystems comprising the selected node.
        :rtype: tuple
        """
        _n_sub_elements = 0
        _n_sub_systems = 0
        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)
            _n_sub_elements += _node.data['allocation'].n_sub_elements
            _n_sub_systems += _node.data['allocation'].n_sub_systems

        return _n_sub_elements, _n_sub_systems

    def _do_calculate_allocation(self, node_id: int) -> None:
        """Allocate a parent reliability goal to it's children.

        :param node_id: the node (allocation) ID of the allocation item whose
            goal is to be allocated.
        :return: None
        :rtype: None
        """
        _node: treelib.Node = self._tree.get_node(node_id)

        self._do_calculate_allocation_goals(_node)

        if _node.data['allocation'].allocation_method_id == 1:  # Equal
            self._do_calculate_equal_allocation(_node)
        elif _node.data['allocation'].allocation_method_id == 2:  # AGREE
            self._do_calculate_agree_allocation(_node)
        elif _node.data['allocation'].allocation_method_id == 3:  # ARINC
            self._do_calculate_arinc_allocation(_node)
        elif _node.data['allocation'].allocation_method_id == 4:  # FOO
            self._do_calculate_foo_allocation(_node)
        else:
            return

        # Let everyone know we succeeded calculating the hardware and
        # auto-save the results.
        pub.sendMessage(
            'succeed_calculate_allocation',
            tree=self._tree,
        )

    @staticmethod
    def _do_calculate_allocation_goals(node: treelib.Node) -> None:
        """Calculate the allocation goals.

        :param node: the treelib.Node() whose goals are to be calculated.
        :return: None
        :rtype: None
        """
        _attributes: Dict[str, Any] = node.data['allocation'].get_attributes()
        _attributes = allocation.do_calculate_goals(**_attributes)

        node.data['allocation'].hazard_rate_goal = _attributes[
            'hazard_rate_goal']
        node.data['allocation'].mtbf_goal = _attributes['mtbf_goal']
        node.data['allocation'].reliability_goal = _attributes[
            'reliability_goal']

    def _do_calculate_arinc_allocation(self, node: treelib.Node) -> None:
        """Allocate reliability using the ARINC method.

        :param node: the treelib.Node() whose reliability is to be allocated.
        :return: None
        :rtype: None
        """
        _parent_goal = node.data['allocation'].hazard_rate_goal
        _method_id = node.data['allocation'].allocation_method_id

        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)

            _attributes = _node.data['allocation'].get_attributes()
            _attributes['allocation_method_id'] = _method_id

            _attributes[
                'weight_factor'] = self._do_calculate_arinc_weight_factor(
                    _node)
            _attributes = allocation.do_allocate_reliability(
                _parent_goal, 0, **_attributes)

            _node.data['allocation'].mtbf_alloc = _attributes['mtbf_alloc']
            _node.data['allocation'].hazard_rate_alloc = _attributes[
                'hazard_rate_alloc']
            _node.data['allocation'].reliability_alloc = _attributes[
                'reliability_alloc']

            _parent_goal = _node.data['allocation'].hazard_rate_goal

    def _do_calculate_arinc_weight_factor(self, node: treelib.Node) -> float:
        """Calculate the weight factor for the allocation at node ID.

        The ARINC weight factor is the quotient of the allocation item's hazard
        rate and the overall system hazard rate.

        :param node: the treelib.Node() of the allocation record whose weight
            factor is being allocated.
        :return: _weight_factor; the weighting factor for the passed node.
        :rtype: float
        """
        _weight_factor = 0.0

        try:
            _weight_factor = (self._node_hazard_rate
                              / self._system_hazard_rate)
        except ZeroDivisionError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{0}: Failed to allocate reliability for '
                          'allocation record ID {1}.  System hazard rate was '
                          '0.0.').format(_method_name, str(node.identifier))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage('fail_calculate_allocation',
                            error_message=_error_msg)

        return _weight_factor

    def _do_calculate_equal_allocation(self, node: treelib.Node) -> None:
        """Allocate reliability using equal apportionment.

        :param node: the treelib.Node() whose reliability is to be allocated.
        :return: None
        :rtype: None
        """
        _parent_goal = node.data['allocation'].reliability_goal
        _method_id = node.data['allocation'].allocation_method_id

        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)

            _attributes = _node.data['allocation'].get_attributes()
            _attributes['allocation_method_id'] = _method_id

            _attributes['weight_factor'] = (
                1.0 / _node.data['allocation'].n_sub_systems)
            _attributes = allocation.do_allocate_reliability(
                _parent_goal, 0, **_attributes)

            _node.data['allocation'].mtbf_alloc = _attributes['mtbf_alloc']
            _node.data['allocation'].hazard_rate_alloc = _attributes[
                'hazard_rate_alloc']
            _node.data['allocation'].reliability_alloc = _attributes[
                'reliability_alloc']

            _parent_goal = _node.data['allocation'].reliability_goal

    def _do_calculate_foo_allocation(self, node: treelib.Node) -> None:
        """Allocate reliability using the FOO method.

        :param node: the treelib.Node() whose reliability is to be allocated.
        :return: None
        :rtype: None
        """
        _parent_goal = node.data['allocation'].hazard_rate_goal
        _method_id = node.data['allocation'].allocation_method_id
        _cum_weight = self._do_calculate_foo_cumulative_weight(node.identifier)

        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)

            _attributes = _node.data['allocation'].get_attributes()
            _attributes['allocation_method_id'] = _method_id

            _attributes = allocation.do_allocate_reliability(
                _parent_goal, _cum_weight, **_attributes)

            _node.data['allocation'].weight_factor = _attributes[
                'weight_factor']
            _node.data['allocation'].percent_weight_factor = _attributes[
                'percent_weight_factor']
            _node.data['allocation'].mtbf_alloc = _attributes['mtbf_alloc']
            _node.data['allocation'].hazard_rate_alloc = _attributes[
                'hazard_rate_alloc']
            _node.data['allocation'].reliability_alloc = _attributes[
                'reliability_alloc']

    def _do_calculate_foo_cumulative_weight(self, node_id: int) -> int:
        """Calculate the cumulative weight for the FOO method.

        :param node_id: the node (allocation) ID of the allocation item whose
            goal is to be allocated.
        :return: _cum_weight; the cumulative weighting factor for the
            allocation item to be allocated.
        """
        _cum_weight = 0
        for _node in self._tree.children(node_id):
            _attributes = _node.data['allocation'].get_attributes()
            _attributes['weight_factor'] = (_attributes['int_factor']
                                            * _attributes['soa_factor']
                                            * _attributes['op_time_factor']
                                            * _attributes['env_factor'])
            _cum_weight += _attributes['weight_factor']

        return _cum_weight

    def _do_get_allocation_goal(self) -> Dict[str, Any]:
        """Retrieve the proper allocation goal.

        :return: _goal; the allocation goal measure.
        :rtype: float
        """
        return allocation.get_allocation_goal(**self._attributes)

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set hazard rate attributes when a hardware item is selected.

        :param attributes: the attributes dict for the selected hardware item.
        :return: None
        :rtype: None
        """
        self._node_hazard_rate = attributes['hazard_rate_active']
        if attributes['hardware_id'] == 1:
            self._system_hazard_rate = attributes['hazard_rate_active']
