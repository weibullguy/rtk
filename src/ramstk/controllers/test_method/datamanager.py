# -*- coding: utf-8 -*-
#
#       ramstk.controllers.test_method.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test Method Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKTestMethod


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Test Method data manager.

    This class manages the Test Method data from the RAMSTKTestMethod
    data models.
    """

    _tag = "test_methods"
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Test Method data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "test_method": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "load_id",
                "test_id",
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
        pub.subscribe(super().do_get_attributes, "request_get_test_method_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_test_method_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_test_method")
        pub.subscribe(super().do_update, "request_update_test_method")

        pub.subscribe(self.do_select_all, "selected_load")
        pub.subscribe(self.do_get_tree, "request_get_test_method_tree")

        pub.subscribe(self._do_delete, "request_delete_test_method")
        pub.subscribe(self._do_insert_test_method, "request_insert_test_method")

    def do_get_tree(self) -> None:
        """Retrieve the Test Method treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_test_method_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Test Method data from the RAMSTK Program database.

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

        for _test_method in self.dao.do_select_all(
            RAMSTKTestMethod,
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
                tag="test_method",
                identifier=_test_method.test_id,
                parent=self._root,
                data={"test_method": _test_method},
            )
            self.last_id = _test_method.test_id

        pub.sendMessage(
            "succeed_retrieve_test_methods",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a Test Method element.

        :param node_id: the node (Test Method element) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_test_method",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent Test Method ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_test_method",
                error_message=_error_msg,
            )

    def _do_insert_test_method(self, parent_id: int) -> None:
        """Add a failure Test Method.

        :param parent_id: the operating load ID the failure Test Method is associated
            with.
        :return: None
        :rtype: None
        """
        try:
            _test_method = RAMSTKTestMethod()
            _test_method.revision_id = self._revision_id
            _test_method.hardware_id = self._hardware_id
            _test_method.mode_id = self._mode_id
            _test_method.mechanism_id = self._mechanism_id
            _test_method.load_id = parent_id
            _test_method.test_id = self.last_id + 1

            self.dao.do_insert(_test_method)

            self.tree.create_node(
                tag="test_method",
                identifier=_test_method.test_id,
                parent=self._root,
                data={"test_method": _test_method},
            )

            self.last_id = max(self.last_id, _test_method.test_id)

            pub.sendMessage(
                "succeed_insert_test_method",
                node_id=_test_method.test_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_test_method",
                error_message=_error.msg,
            )
