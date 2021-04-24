# -*- coding: utf-8 -*-
#
#       ramstk.controllers.program_status.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Program Status Package Data Model."""

# Standard Library Imports
import inspect
from datetime import date
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKProgramStatus


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Program Status data manager.

    This class manages the validation data from the RAMSTKProgram Status
    and RAMSKTProgramStatus data models.
    """

    _tag: str = 'program_status'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Program Status data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_status: Dict[Any, List[float]] = {}
        self._pkey = {'program_status': ['revision_id', 'status_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_program_status_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_program_status_attributes')
        pub.subscribe(super().do_update, 'request_update_program_status')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_get_tree, 'request_get_program_status_tree')

        pub.subscribe(self._do_delete, 'request_delete_program_status')
        pub.subscribe(self._do_insert_program_status,
                      'request_insert_program_status')
        pub.subscribe(self._do_set_attributes,
                      'succeed_calculate_all_validation_tasks')

    def do_get_tree(self) -> None:
        """Retrieve the program status treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_program_status_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all Program Status data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _status in self.dao.do_select_all(
                RAMSTKProgramStatus,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKProgramStatus.date_status):

            self._dic_status[_status.date_status] = _status.status_id

            self.tree.create_node(tag='program_status',
                                  identifier=_status.status_id,
                                  parent=self._root,
                                  data={'program_status': _status})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_program_status',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a Program Status task.

        :param node_id: the node (validation) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        :raises: NodeIDAbsentError if the record is deleted from the
            database but there is no corresponding node in the tree.  This
            condition shouldn't happen, so it should be dealt with using the
            logger and a user dialog.
        """
        try:
            super().do_delete(node_id, 'program_status')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_program_status', tree=self.tree)
        except (AttributeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent program status ID '
                '{0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_program_status',
                error_message=_error_msg,
            )

    def _do_insert_program_status(self) -> None:
        """Add a new program status record.

        :return: None
        :rtype: None
        """
        _last_id = self.dao.get_last_id('ramstk_program_status', 'status_id')
        try:
            _status = RAMSTKProgramStatus()
            _status.revision_id = self._revision_id
            _status.status_id = _last_id + 1
            _status.date_status = date.today()

            self.dao.do_insert(_status)

            self.last_id = _status.status_id

            self._dic_status[_status.date_status] = _status.status_id

            self.tree.create_node(tag='program_status',
                                  identifier=_status.status_id,
                                  parent=self._root,
                                  data={'program_status': _status})

            pub.sendMessage(
                'succeed_insert_program_status',
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
                "fail_insert_program_status",
                error_message=_error.msg,
            )

    def _do_set_attributes(self, cost_remaining, time_remaining) -> None:
        """Set the program remaining cost and time.

        :param cost_remaining: total remaining cost of verification program.
        :param time_remaining: total remaining time of verification program.
        :return: None
        :rtype: None
        """
        try:
            _node_id = self._dic_status[date.today()]
        except KeyError:
            self._do_insert_program_status()
            _node_id = self.last_id

        self.tree.get_node(
            _node_id).data['program_status'].cost_remaining = cost_remaining
        self.tree.get_node(
            _node_id).data['program_status'].time_remaining = time_remaining

        self.do_update(_node_id, table='program_status')
