# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mechanism.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Mechanism Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKMechanism


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mechanism data manager.

    This class manages the Mechanism data from the RAMSTKMode,
    RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod
    data models.
    """

    _tag = "mechanisms"
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Mechanism data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "mechanism": ["revision_id", "hardware_id", "mode_id", "mechanism_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mechanism_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mechanism_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_mechanism")
        pub.subscribe(super().do_update, "request_update_mechanism")

        pub.subscribe(self.do_select_all, "selected_mode")
        pub.subscribe(self.do_get_tree, "request_get_mechanism_tree")

        pub.subscribe(self._do_delete, "request_delete_mechanism")
        pub.subscribe(self._do_insert_mechanism, "request_insert_mechanism")

    def do_get_tree(self) -> None:
        """Retrieve the Mechanism treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_mechanism_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Mechanism data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes["revision_id"]
        self._hardware_id = attributes["hardware_id"]
        self._parent_id = attributes["mode_id"]

        for _mechanism in self.dao.do_select_all(
            RAMSTKMechanism,
            key=["revision_id", "hardware_id", "mode_id"],
            value=[self._revision_id, self._hardware_id, self._parent_id],
        ):
            self.tree.create_node(
                tag="mechanism",
                identifier=_mechanism.mechanism_id,
                parent=self._root,
                data={"mechanism": _mechanism},
            )
            self.last_id = _mechanism.mechanism_id

        pub.sendMessage(
            "succeed_retrieve_mechanisms",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a Mechanism element.

        :param node_id: the node (Mechanism element) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_mechanism",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent Mechanism ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_mechanism",
                error_message=_error_msg,
            )

    def _do_insert_mechanism(self) -> None:
        """Add a failure Mechanism.

        :return: None
        :rtype: None
        """
        try:
            _mechanism = RAMSTKMechanism()
            _mechanism.revision_id = self._revision_id
            _mechanism.hardware_id = self._hardware_id
            _mechanism.mode_id = self._parent_id
            _mechanism.mechanism_id = self.last_id + 1

            self.dao.do_insert(_mechanism)

            self.tree.create_node(
                tag="mechanism",
                identifier=_mechanism.mechanism_id,
                parent=self._root,
                data={"mechanism": _mechanism},
            )

            self.last_id = max(self.last_id, _mechanism.mechanism_id)

            pub.sendMessage(
                "succeed_insert_mechanism",
                node_id=_mechanism.mechanism_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mechanism",
                error_message=_error.msg,
            )
