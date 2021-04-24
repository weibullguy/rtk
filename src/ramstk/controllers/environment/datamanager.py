# -*- coding: utf-8 -*-
#
#       ramstk.controllers.environment.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Environment Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKEnvironment


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Environment data manager.

    This class manages the data from the RAMSKTEnvironment data models.
    """

    _tag = "environments"

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize an Environment data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "environment": ["revision_id", "phase_id", "environment_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_environment_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_environment_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_usage_profile")
        pub.subscribe(super().do_update, "request_update_environment")

        pub.subscribe(self.do_select_all, "selected_revision")
        pub.subscribe(self.do_get_tree, "request_get_environment_tree")

        pub.subscribe(self._do_delete, "request_delete_environment")
        pub.subscribe(self._do_insert_environment, "request_insert_environment")

    def do_get_tree(self) -> None:
        """Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_environment_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Environment data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _environment in self.dao.do_select_all(
            RAMSTKEnvironment, key=["revision_id"], value=[self._revision_id]
        ):
            self.tree.create_node(
                tag="environment",
                identifier=_environment.environment_id,
                parent=self._root,
                data={"environment": _environment},
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_environments",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove an environment element.

        :param node_id: the environment ID to remove.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, "environment")

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_environment",
                tree=self.tree,
            )
        except (DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent environment ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_environment",
                error_message=_error_msg,
            )

    def _do_insert_environment(self, phase_id: int) -> None:
        """Add a new environment for phase ID.

        :param phase_id: the mission phase ID to add the new environment.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id("ramstk_environment", "environment_id")
            _environment = RAMSTKEnvironment()
            _environment.revision_id = self._revision_id
            _environment.phase_id = phase_id
            _environment.environment_id = _last_id + 1

            self.dao.do_insert(_environment)

            self.tree.create_node(
                tag="environment",
                identifier=_environment.environment_id,
                parent=self._root,
                data={"environment": _environment},
            )

            self.last_id = max(self.last_id, _environment.environment_id)

            pub.sendMessage(
                "succeed_insert_environment",
                node_id=self.last_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_environment",
                error_message=_error.msg,
            )
