# -*- coding: utf-8 -*-
#
#       ramstk.controllers.failure_definition.datamanager.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Definition Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFailureDefinition


class DataManager(RAMSTKDataManager):
    """Contains attributes and methods of the Failure Definition data manager.

    This class manages the failure definition data from the
    RAMSTKFailureDefinition data models.
    """

    _tag = 'failure_definitions'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Failure Definition data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey: Dict[str, List[str]] = {
            'failure_definition': ['revision_id', 'definition_id']
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_failure_definition_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_failure_definition_attributes')
        pub.subscribe(super().do_set_attributes,
                      'lvw_editing_failure_definition')
        pub.subscribe(super().do_update, 'request_update_failure_definition')

        pub.subscribe(self.do_get_tree, 'request_get_failure_definition_tree')
        pub.subscribe(self.do_select_all, 'selected_revision')

        pub.subscribe(self._do_delete, 'request_delete_failure_definitions')
        pub.subscribe(self._do_insert_failure_definition,
                      'request_insert_failure_definitions')

    def do_get_tree(self) -> None:
        """Retrieve the failure definition treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_failure_definition_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all Failure Definitions from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _failure_definition in self.dao.do_select_all(
                RAMSTKFailureDefinition,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKFailureDefinition.definition_id):

            self.tree.create_node(
                tag='definition',
                identifier=_failure_definition.definition_id,
                parent=self._root,
                data={'failure_definition': _failure_definition})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_failure_definitions',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a failure definition.

        :param node_id: the failure definition ID to remove.
        :return: None
        """
        try:
            super().do_delete(node_id, 'failure_definition')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_failure_definition',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = ('{1}: Attempted to delete non-existent failure '
                               'definition ID {0}.'.format(
                                   str(node_id), _method_name))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_failure_definition',
                error_message=_error_msg,
            )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_insert_failure_definition(self, parent_id: int = 0) -> None:
        """Add a new failure definition for the selected revision.

        :param parent_id: the ID of the parent entity.  Unused in this
            method as failure definitions are not hierarchical.  Included to
            keep method generic and compatible with PyPubSub MDS.
        :return: None
        :rtype: None
        """
        try:
            _failure_definition = RAMSTKFailureDefinition()
            _failure_definition.revision_id = self._revision_id
            _failure_definition.definition_id = self.last_id + 1

            self.dao.do_insert(_failure_definition)

            self.last_id = _failure_definition.definition_id

            self.tree.create_node(
                tag='definition',
                identifier=self.last_id,
                parent=self._root,
                data={'failure_definition': _failure_definition},
            )

            pub.sendMessage(
                'succeed_insert_failure_definition',
                node_id=self.last_id,
                tree=self.tree,
            )
        except DataAccessError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempting to add failure definition to non-existent '
                'revision {0}.'.format(self._revision_id, _method_name))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_failure_definition",
                error_message=_error_msg,
            )
