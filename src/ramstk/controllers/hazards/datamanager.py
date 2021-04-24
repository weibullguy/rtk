# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hazards.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hazards Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKHazardAnalysis


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Hazard data manager.

    This class manages the hazard data from the RAMSTKHazardAnalysis and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'hazards'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Hazard data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'hazard': ['revision_id', 'function_id', 'hazard_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_hazard_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_hazard_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_hazard')
        pub.subscribe(super().do_update, 'request_update_hazard')

        pub.subscribe(self.do_get_tree, 'request_get_hazard_tree')
        pub.subscribe(self.do_select_all, 'selected_function')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_hazard_attributes')

        pub.subscribe(self._do_delete, 'request_delete_hazard')
        pub.subscribe(self._do_insert_hazard, 'request_insert_hazard')

    def do_get_tree(self) -> None:
        """Retrieve the hazard treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_hazard_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Hazard data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Hazard.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        _function_id = attributes['function_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _hazard in self.dao.do_select_all(
                RAMSTKHazardAnalysis,
                key=['revision_id', 'function_id'],
                value=[self._revision_id, _function_id],
                order=RAMSTKHazardAnalysis.hazard_id):

            self.tree.create_node(tag='hazard',
                                  identifier=_hazard.hazard_id,
                                  parent=self._root,
                                  data={'hazard': _hazard})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            'succeed_retrieve_hazards',
            tree=self.tree,
        )

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the selected hazard.

        This is a helper method to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the hardware item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes(node_id=[attributes['hazard_id'], ''],
                                      package={_key: attributes[_key]})

    def _do_delete(self, node_id: int) -> None:
        """Remove a hazard.

        :param node_id: the node (hazard) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'hazard')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                'succeed_delete_hazard',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: Attempted to delete non-existent hazard '
                          'ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_hazard',
                error_message=_error_msg,
            )

    def _do_insert_hazard(self, parent_id: int = 0) -> None:
        """Add a new hazard to parent (function) ID.

        :param parent_id: the parent (function) ID to associate the new hazard
            with.
        :return: None
        :rtype: None
        """
        _last_id = self.dao.get_last_id('ramstk_hazard_analysis', 'hazard_id')
        try:
            _hazard = RAMSTKHazardAnalysis()
            _hazard.revision_id = self._revision_id
            _hazard.function_id = parent_id
            _hazard.hazard_id = _last_id + 1

            self.dao.do_insert(_hazard)

            self.tree.create_node(tag='hazard',
                                  identifier=_hazard.hazard_id,
                                  parent=self._root,
                                  data={'hazard': _hazard})

            self.last_id = _hazard.hazard_id

            pub.sendMessage(
                'succeed_insert_hazard',
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
                "fail_insert_hazard",
                error_message=_error.msg,
            )
