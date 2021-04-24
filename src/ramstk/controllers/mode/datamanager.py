# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mode.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mode Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKMode


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mode data manager."""

    _tag = "modes"
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Mode data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "mode": ["revision_id", "hardware_id", "mode_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mode_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mode_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_mode")
        pub.subscribe(super().do_update, "request_update_mode")

        pub.subscribe(self.do_select_all, "selected_revision")
        pub.subscribe(self.do_get_tree, "request_get_mode_tree")

        pub.subscribe(self._do_delete, "request_delete_mode")
        pub.subscribe(self._do_insert_mode, "request_insert_mode")

    def do_get_tree(self) -> None:
        """Retrieve the Mode treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_mode_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Mode data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            function or hardware item.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]
        self._parent_id = attributes["hardware_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _mode in self.dao.do_select_all(
            RAMSTKMode,
            key=["revision_id", "hardware_id"],
            value=[self._revision_id, self._parent_id],
        ):
            self.tree.create_node(
                tag="mode",
                identifier=_mode.mode_id,
                parent=self._root,
                data={"mode": _mode},
            )
            self.last_id = _mode.mode_id

        pub.sendMessage(
            "succeed_retrieve_modes",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a Mode element.

        :param node_id: the node (Mode element) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_mode",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent mode ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_mode",
                error_message=_error_msg,
            )

    def _do_insert_mode(self) -> None:
        """Add a new failure mode.

        :return: None
        :rtype: None
        """
        try:
            _last_id: int = self.dao.get_last_id("ramstk_mission", "mission_id")
            _mode = RAMSTKMode()
            _mode.revision_id = self._revision_id
            _mode.hardware_id = self._parent_id
            _mode.mode_id = _last_id + 1

            self.dao.do_insert(_mode)

            self.tree.create_node(
                tag="mode",
                identifier=_mode.mode_id,
                parent=self._root,
                data={"mode": _mode},
            )

            self.last_id = max(self.last_id, _mode.mode_id)

            pub.sendMessage(
                "succeed_insert_mode",
                node_id=_mode.mode_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mode",
                error_message=_error.msg,
            )
