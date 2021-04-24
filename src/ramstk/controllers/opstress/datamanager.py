# -*- coding: utf-8 -*-
#
#       ramstk.controllers.opstress.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Operating Load Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKOpStress


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the OpStress data manager.

    This class manages the OpStress data from the RAMSTKOpStress data
    model.
    """

    _tag = "opstresss"
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a OpStress data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "opstress": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "load_id",
                "stress_id",
            ],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id: int = 0
        self._mode_id: int = 0
        self._mechanism_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_opstress_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_opstress_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_opstress")
        pub.subscribe(super().do_update, "request_update_opstress")

        pub.subscribe(self.do_select_all, "selected_load")
        pub.subscribe(self.do_get_tree, "request_get_opstress_tree")

        pub.subscribe(self._do_delete, "request_delete_opstress")
        pub.subscribe(self._do_insert_opstress, "request_insert_opstress")

    def do_get_tree(self) -> None:
        """Retrieve the OpStress treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_opstress_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the OpStress data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes["revision_id"]
        self._hardware_id = attributes["hardware_id"]
        self._mode_id = attributes["mode_id"]
        self._mechanism_id = attributes["mechanism_id"]
        self._parent_id = attributes["load_id"]

        for _opstress in self.dao.do_select_all(
            RAMSTKOpStress,
            key=["revision_id", "hardware_id", "mode_id", "mechanism_id", "load_id"],
            value=[
                self._revision_id,
                self._hardware_id,
                self._mode_id,
                self._mechanism_id,
                self._parent_id,
            ],
        ):
            self.tree.create_node(
                tag="opstress",
                identifier=_opstress.stress_id,
                parent=self._root,
                data={"opstress": _opstress},
            )
            self.last_id = _opstress.stress_id

        pub.sendMessage(
            "succeed_retrieve_opstresss",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a OpStress element.

        :param node_id: the node (OpStress element) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_opstress",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent OpStress ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_opstress",
                error_message=_error_msg,
            )

    def _do_insert_opstress(self, parent_id: int) -> None:
        """Add a failure OpStress.

        :param parent_id: a list containing the the failure Mode ID and the failure
            Mechanism ID the new OpStress is associated with.
        :return: None
        :rtype: None
        """
        try:
            _opstress = RAMSTKOpStress()
            _opstress.revision_id = self._revision_id
            _opstress.hardware_id = self._hardware_id
            _opstress.mode_id = self._mode_id
            _opstress.mechanism_id = self._mechanism_id
            _opstress.load_id = parent_id
            _opstress.stress_id = self.last_id + 1

            self.dao.do_insert(_opstress)

            self.tree.create_node(
                tag="opstress",
                identifier=_opstress.stress_id,
                parent=self._root,
                data={"opstress": _opstress},
            )

            self.last_id = max(self.last_id, _opstress.stress_id)

            pub.sendMessage(
                "succeed_insert_opstress",
                node_id=_opstress.stress_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_opstress",
                error_message=_error.msg,
            )
