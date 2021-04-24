# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.allocation.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKAllocation


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Allocation data manager."""

    _tag: str = 'allocations'
    _root: int = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Allocation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            'allocation': ['revision_id', 'hardware_id'],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_allocation_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_allocation_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_allocation')
        pub.subscribe(super().do_set_tree, 'succeed_calculate_allocation')
        pub.subscribe(super().do_update, 'request_update_allocation')

        pub.subscribe(self.do_get_tree, 'request_get_allocation_tree')
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_set_all_attributes,
                      'succeed_calculate_allocation_goals')

        pub.subscribe(self._do_delete, 'request_delete_hardware')
        pub.subscribe(self._do_insert_allocation, 'request_insert_allocation')

    def do_get_tree(self) -> None:
        """Retrieve the allocation treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_allocation_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Allocation BoM data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _allocation in self.dao.do_select_all(
                RAMSTKAllocation,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKAllocation.parent_id):

            self.tree.create_node(tag='allocation',
                                  identifier=_allocation.hardware_id,
                                  parent=_allocation.parent_id,
                                  data={'allocation': _allocation})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_allocation',
            tree=self.tree,
        )

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the allocation
            item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes(node_id=[attributes['hardware_id'], -1],
                                      package={_key: attributes[_key]})

    def _do_delete(self, node_id: int) -> None:
        """Remove an Allocation record.

        :param node_id: the node (hardware) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            # Delete the children (if any), then the parent node that was
            # passed.
            for _child in self.tree.children(node_id):
                super().do_delete(_child.identifier, 'allocation')
            super().do_delete(node_id, 'allocation')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_allocation',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent allocation record '
                'with hardware ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_allocation',
                error_message=_error_msg,
            )

    def _do_insert_allocation(self,
                              hardware_id: int,
                              parent_id: int = 0) -> None:
        """Add a new allocation record.

        :param hardware_id: the ID of the hardware item to associate the
            allocation record.
        :param parent_id: the parent allocation item's ID.
        :return: None
        :rtype: None
        """
        try:
            _allocation = RAMSTKAllocation()
            _allocation.revision_id = self._revision_id
            _allocation.hardware_id = hardware_id
            _allocation.parent_id = parent_id

            self.dao.do_insert(_allocation)

            self.last_id = _allocation.hardware_id

            self.tree.create_node(tag='allocation',
                                  identifier=_allocation.hardware_id,
                                  parent=parent_id,
                                  data={'allocation': _allocation})

            pub.sendMessage(
                'succeed_insert_allocation',
                node_id=self.last_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_hardware",
                error_message=_error.msg,
            )
