# -*- coding: utf-8 -*-
#
#       ramstk.controllers.revision.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRevision


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Revision data manager.

    This class manages the revision data from the RAMSTKRevision,
    RAMSTKFailureDefinition, RAMSTKMission, RAMSTKMissionPhase, and
    RAMSKTEnvironment data models.
    """

    _tag = 'revisions'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Revision data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'revision': ['revision_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_revision_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_revision_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_revision')
        pub.subscribe(super().do_update, 'request_update_revision')

        pub.subscribe(self.do_get_tree, 'request_get_revision_tree')
        pub.subscribe(self.do_select_all, 'request_retrieve_revisions')

        pub.subscribe(self._do_delete, 'request_delete_revision')
        pub.subscribe(self._do_insert_revision, 'request_insert_revision')

    def do_get_tree(self) -> None:
        """Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_revision_tree', tree=self.tree)

    def do_select_all(self) -> None:
        """Retrieve all the Revision data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _revision in self.dao.do_select_all(
                RAMSTKRevision,
                key=None,
                value=None,
                order=RAMSTKRevision.revision_id):

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data={'revision': _revision})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_revisions',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a revision.

        :param node_id: the node (revision) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'revision')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_revision',
                tree=self.tree,
            )
        except (DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent revision ID '
                '{0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_revision',
                error_message=_error_msg,
            )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_insert_revision(self, parent_id: int = 0) -> None:
        """Add a new revision.

        :param parent_id: the ID of the parent entity.  Unused in this
            method as revisions have no parent.  Included to keep method
            generic and compatible with PyPubSub MDS.
        :return: None
        :rtype: None
        :raise: AttributeError if not connected to a RAMSTK program database.
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_revision', 'revision_id')
            _revision = RAMSTKRevision()
            _revision.revision_id = _last_id + 1
            _revision.name = 'New Revision'

            self.dao.do_insert(_revision)

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data={'revision': _revision})
            self.last_id = _revision.revision_id
            pub.sendMessage(
                'succeed_insert_revision',
                node_id=self.last_id,
                tree=self.tree,
            )
        except (AttributeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = ('{0}: Failed to insert revision into program '
                               'database.'.format(_method_name))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_revision",
                error_message=_error_msg,
            )
