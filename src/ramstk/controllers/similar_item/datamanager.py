# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.similar_item.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Similar Item Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKSimilarItem


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Similar Item data manager."""

    _tag = 'similar_items'
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Hardware data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            'similar_item': ['revision_id', 'hardware_id'],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_similar_item_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_similar_item_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_similar_item')
        pub.subscribe(super().do_set_tree, 'succeed_calculate_similar_item')
        pub.subscribe(super().do_update, 'request_update_similar_item')

        pub.subscribe(self.do_get_tree, 'request_get_similar_item_tree')
        pub.subscribe(self.do_select_all, 'selected_revision')

        pub.subscribe(self._do_delete, 'request_delete_hardware')
        pub.subscribe(self._do_insert_similar_item,
                      'request_insert_similar_item')

    def do_get_tree(self) -> None:
        """Retrieve the hardware treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_similar_item_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Hardware BoM data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _similar_item in self.dao.do_select_all(
                RAMSTKSimilarItem,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKSimilarItem.parent_id):

            self.tree.create_node(tag='similar_item',
                                  identifier=_similar_item.hardware_id,
                                  parent=_similar_item.parent_id,
                                  data={'similar_item': _similar_item})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_similar_item',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a similar item record.

        :param node_id: the similar item (hardware) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            # Delete the children (if any), then the parent node that was
            # passed.
            for _child in self.tree.children(node_id):
                super().do_delete(_child.identifier, 'similar_item')
            super().do_delete(node_id, 'similar_item')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_similar_item',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent similar item record '
                'with hardware ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_similar_item',
                error_message=_error_msg,
            )

    def _do_insert_similar_item(self,
                                hardware_id: int,
                                parent_id: int = 0) -> None:
        """Add a new similar item record.

        :param hardware_id: the ID of the hardware item to associate the
            allocation record.
        :param parent_id: the parent allocation item's ID.
        :return: None
        :rtype: None
        """
        try:
            _similar_item = RAMSTKSimilarItem()
            _similar_item.revision_id = self._revision_id
            _similar_item.hardware_id = hardware_id
            _similar_item.parent_id = parent_id

            self.dao.do_insert(_similar_item)

            self.last_id = _similar_item.hardware_id

            self.tree.create_node(tag='similar_item',
                                  identifier=_similar_item.hardware_id,
                                  parent=parent_id,
                                  data={'similar_item': _similar_item})

            pub.sendMessage(
                'succeed_insert_similar_item',
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
                "fail_insert_similar_item",
                error_message=_error.msg,
            )
