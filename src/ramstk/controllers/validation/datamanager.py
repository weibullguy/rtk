# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKValidation


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Validation data manager.

    This class manages the validation data from the RAMSTKValidation and
    RAMSKTProgramStatus data models.
    """

    _tag: str = 'validations'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Validation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_status: Dict[Any, float] = {}
        self._pkey = {'validation': ['revision_id', 'validation_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_validation_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_validation_attributes')
        pub.subscribe(super().do_set_attributes, 'mvw_editing_validation')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_validation')
        pub.subscribe(super().do_update, 'request_update_validation')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_get_tree, 'request_get_validations_tree')

        pub.subscribe(self._do_delete, 'request_delete_validation')
        pub.subscribe(self._do_insert_validation, 'request_insert_validation')

    def do_get_tree(self) -> None:
        """Retrieve the validation treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_validations_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all Validation BoM data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Requirement.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _validation in self.dao.do_select_all(
                RAMSTKValidation,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKValidation.validation_id):

            self.tree.create_node(tag='validation',
                                  identifier=_validation.validation_id,
                                  parent=self._root,
                                  data={'validation': _validation})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_validations',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a Validation task.

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
            super().do_delete(node_id, 'validation')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_validation',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent validation task ID '
                '{0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_validation',
                error_message=_error_msg,
            )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_insert_validation(self, parent_id: int) -> None:
        """Add a new validation task.

        :param parent_id: unused in this method, but required for consistent
            argument list to _do_insert_{0} methods.
        :return: None
        :rtype: None
        """
        _last_id = self.dao.get_last_id('ramstk_validation', 'validation_id')
        try:
            _validation = RAMSTKValidation()
            _validation.revision_id = self._revision_id
            _validation.validation_id = _last_id + 1
            _validation.name = "New Validation Task"

            self.dao.do_insert(_validation)

            self.last_id = _validation.validation_id

            self.tree.create_node(tag='validation',
                                  identifier=_validation.validation_id,
                                  parent=self._root,
                                  data={'validation': _validation})

            pub.sendMessage(
                'succeed_insert_validation',
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
                "fail_insert_validation",
                error_message=_error.msg,
            )
