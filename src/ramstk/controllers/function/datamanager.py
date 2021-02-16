# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFunction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Function data manager.

    This class manages the function data from the RAMSTKFunction and
    RAMSTKHazardAnalysis data models.
    """

    # Define private scalar class attributes.
    _tag = 'functions'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Function data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'function': ['revision_id', 'function_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_function_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_function_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_function')
        pub.subscribe(super().do_update_all, 'request_update_all_functions')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update, 'request_update_function')
        pub.subscribe(self.do_get_tree, 'request_get_functions_tree')

        pub.subscribe(self._do_delete, 'request_delete_function')
        pub.subscribe(self._do_insert_function, 'request_insert_function')

    def do_get_tree(self) -> None:
        """Retrieve the function treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_functions_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Function data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Function.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _function in self.dao.do_select_all(
                RAMSTKFunction,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKFunction.function_id):

            self.tree.create_node(tag='function',
                                  identifier=_function.function_id,
                                  parent=_function.parent_id,
                                  data={'function': _function})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_functions',
            tree=self.tree,
        )

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node (function) ID of the function to save.
        :return: None
        :rtype: None
        """
        _method_name: str = inspect.currentframe(  # type: ignore
        ).f_code.co_name

        try:
            self.dao.do_update(self.tree.get_node(node_id).data['function'])
            pub.sendMessage(
                'succeed_update_function',
                tree=self.tree,
            )
        except AttributeError:
            _error_msg: str = (
                '{1}: Attempted to save non-existent function with function '
                'ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_failure_definition',
                error_message=_error_msg,
            )
        except KeyError:
            _error_msg = (
                '{1}: No data package found for function ID {0}.').format(
                    str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_failure_definition',
                error_message=_error_msg,
            )
        except (DataAccessError, TypeError):
            if node_id != 0:
                _error_msg = ('{1}: The value for one or more attributes for '
                              'function ID {0} was the wrong type.').format(
                                  str(node_id), _method_name)
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                pub.sendMessage(
                    'fail_update_failure_definition',
                    error_message=_error_msg,
                )

    def _do_delete(self, node_id: int) -> None:
        """Remove a function.

        :param node_id: the node (function) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'function')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_function',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent function ID {'
                '0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_function',
                error_message=_error_msg,
            )

    def _do_insert_function(self, parent_id: int = 0) -> None:
        """Add a new function as child of the parent ID function.

        :param parent_id: the parent (function) ID of the function to
            insert the child.  Default is to add a top-level function.
        :return: None
        :rtype: None
        """
        _method_name: str = inspect.currentframe(  # type: ignore
        ).f_code.co_name

        try:
            _last_id = self.dao.get_last_id('ramstk_function', 'function_id')

            _function = RAMSTKFunction()
            _function.revision_id = self._revision_id
            _function.function_id = _last_id + 1
            _function.name = 'New Function'
            _function.parent_id = parent_id

            self.dao.do_insert(_function)

            self.last_id = _function.function_id

            self.tree.create_node(tag='function',
                                  identifier=_function.function_id,
                                  parent=_function.parent_id,
                                  data={'function': _function})

            pub.sendMessage(
                'succeed_insert_function',
                node_id=self.last_id,
                tree=self.tree,
            )
        except NodeIDAbsentError:
            _error_msg: str = ('{1}: Attempted to insert child function under '
                               'non-existent function ID {0}.').format(
                                   str(parent_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_function",
                error_message=_error_msg,
            )
        except DataAccessError:
            _error_msg = ('{1}: A database error occurred when attempting to '
                          'add a child function to parent function ID '
                          '{0}.').format(str(parent_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_function",
                error_message=_error_msg,
            )
