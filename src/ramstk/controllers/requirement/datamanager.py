# -*- coding: utf-8 -*-
#
#       ramstk.controllers.requirement.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRequirement


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Requirement data manager.

    This class manages the requirement data from the RAMSTKRequirement
    and RAMSTKStakeholder data models.
    """
    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = 'requirements'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Requirement data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'requirement': ['revision_id', 'requirement_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_requirement_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_requirement_attributes')
        pub.subscribe(super().do_set_attributes, 'mvw_editing_requirement')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_requirement')
        pub.subscribe(super().do_update, 'request_update_requirement')
        pub.subscribe(super().do_create_all_codes,
                      'request_create_all_requirement_codes')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_get_tree, 'request_get_requirements_tree')
        pub.subscribe(self.do_create_code, 'request_create_requirement_code')

        pub.subscribe(self._do_delete, 'request_delete_requirement')
        pub.subscribe(self._do_insert_requirement,
                      'request_insert_requirement')

    def do_create_code(self, node_id: int, prefix: str) -> None:
        """Request to create the requirement code.

        :param node_id: the Requirement ID to create the code for.
        :param prefix: the code prefix to use for the requested code.
        :return: None
        :rtype: None
        """
        try:
            _requirement = self.tree.get_node(node_id).data['requirement']
            _requirement.create_code(prefix=prefix)

            pub.sendMessage('succeed_create_code')
            pub.sendMessage(
                'succeed_create_requirement_code',
                requirement_code=_requirement.get_attributes()
                ['requirement_code'],
            )
        except (TypeError, AttributeError):
            if node_id != 0:
                _method_name: str = inspect.currentframe(  # type: ignore
                ).f_code.co_name
                pub.sendMessage(
                    'fail_create_requirement_code',
                    error_message=('{1}: No data package found for '
                                   'requirement ID {0:s}.').format(
                                       str(node_id), _method_name),
                )

    def do_get_tree(self) -> None:
        """Retrieve the requirement treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_requirements_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Requirement data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _requirement in self.dao.do_select_all(
                RAMSTKRequirement,
                key=['revision_id'],
                value=[self._revision_id],
                order=RAMSTKRequirement.requirement_id):

            self.tree.create_node(tag='requirement',
                                  identifier=_requirement.requirement_id,
                                  parent=_requirement.parent_id,
                                  data={'requirement': _requirement})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_requirements',
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a requirement.

        :param node_id: the node (requirement) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            # Delete the children (if any), then the parent node that was
            # passed.
            for _child in self.tree.children(node_id):
                super().do_delete(_child.identifier, 'requirement')
            super().do_delete(node_id, 'requirement')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_requirement',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent requirement ID {'
                '0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_requirement',
                error_message=_error_msg,
            )

    def _do_insert_requirement(self, parent_id: int = 0) -> None:
        """Add a new requirement.

        :param parent_id: the parent (requirement) ID the new requirement
            will be a child (derived) of.
        :return: None
        :rtype: None
        """
        try:
            _requirement = RAMSTKRequirement()
            _requirement.revision_id = self._revision_id
            _requirement.requirement_id = self.last_id + 1
            _requirement.parent_id = parent_id
            _requirement.description = 'New Requirement'

            self.dao.do_insert(_requirement)

            self.last_id = _requirement.requirement_id
            self.tree.create_node(tag='requirement',
                                  identifier=self.last_id,
                                  parent=parent_id,
                                  data={'requirement': _requirement})

            pub.sendMessage(
                'succeed_insert_requirement',
                node_id=self.last_id,
                tree=self.tree,
            )
        except NodeIDAbsentError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to insert child requirement under '
                'non-existent requirement ID {0}.').format(
                    str(parent_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_requirement",
                error_message=_error_msg,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_requirement",
                error_message=_error.msg,
            )
