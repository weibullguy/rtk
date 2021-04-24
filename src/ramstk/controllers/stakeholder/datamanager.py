# -*- coding: utf-8 -*-
#
#       ramstk.controllers.stakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKStakeholder


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Stakeholder data manager.

    This class manages the stakeholder data from the RAMSTKStakeholder
    and RAMSTKStakeholder data models.
    """

    _tag = 'stakeholders'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Stakeholder data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'stakeholder': ['revision_id', 'stakeholder_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_stakeholder_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_stakeholder_attributes')
        pub.subscribe(super().do_set_attributes, 'lvw_editing_stakeholder')
        pub.subscribe(super().do_update, 'request_update_stakeholders')

        pub.subscribe(self.do_get_tree, 'request_get_stakeholder_tree')
        pub.subscribe(self.do_select_all, 'selected_revision')

        pub.subscribe(self._do_delete, 'request_delete_stakeholder')
        pub.subscribe(self._do_insert_stakeholder,
                      'request_insert_stakeholder')

    def do_get_tree(self) -> None:
        """Retrieve the stakeholder treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_stakeholder_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Stakeholder data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _stakeholder in self.dao.do_select_all(
                RAMSTKStakeholder,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKStakeholder.stakeholder_id):
            _data_package = {'stakeholder': _stakeholder}

            self.tree.create_node(tag='stakeholder',
                                  identifier=_stakeholder.stakeholder_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_stakeholders',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a stakeholder.

        :param node_id: the node (stakeholder) ID to be removed from the RAMSTK
            Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'stakeholder')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_stakeholder',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent stakeholder input ID '
                '{0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_stakeholder',
                error_message=_error_msg,
            )

    def _do_insert_stakeholder(self) -> None:
        """Add a new stakeholder.

        :return: None
        :rtype: None
        """
        try:
            _stakeholder = RAMSTKStakeholder()
            _stakeholder.revision_id = self._revision_id
            _stakeholder.stakeholder_id = self.last_id + 1
            _stakeholder.description = 'New Stakeholder Input'

            self.dao.do_insert(_stakeholder)

            self.last_id = _stakeholder.stakeholder_id
            self.tree.create_node(tag='stakeholder',
                                  identifier=self.last_id,
                                  parent=0,
                                  data={'stakeholder': _stakeholder})

            pub.sendMessage(
                'succeed_insert_stakeholder',
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
                "fail_insert_stakeholder",
                error_message=_error.msg,
            )
