# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mission.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mission Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKMission


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mission data manager.

    This class manages the usage profile data from the RAMSTKMission
    data models.
    """

    _tag = "missions"

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a RAMSTKFailureDefinition, data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "mission": ["revision_id", "mission_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mission_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mission_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_usage_profile")
        pub.subscribe(super().do_update, "request_update_mission")

        pub.subscribe(self.do_select_all, "selected_revision")
        pub.subscribe(self.do_get_tree, "request_get_mission_tree")

        pub.subscribe(self._do_delete, "request_delete_mission")
        pub.subscribe(self._do_insert_mission, "request_insert_mission")

    def do_get_tree(self) -> None:
        """Retrieve the mission treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_mission_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Mission data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _mission in self.dao.do_select_all(
            RAMSTKMission, key=["revision_id"], value=[self._revision_id]
        ):
            self.tree.create_node(
                tag="mission",
                identifier=_mission.mission_id,
                parent=self._root,
                data={"mission": _mission},
            )
            self.last_id = _mission.mission_id

        pub.sendMessage(
            "succeed_retrieve_missions",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a usage profile element.

        :param node_id: the usage profile element ID to remove.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, "mission")

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_mission",
                tree=self.tree,
            )
        except (DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent mission ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_mission",
                error_message=_error_msg,
            )

    def _do_insert_mission(self) -> None:
        """Add a new mission for revision ID.

        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id("ramstk_mission", "mission_id")
            _mission = RAMSTKMission()
            _mission.revision_id = self._revision_id
            _mission.mission_id = _last_id + 1

            self.dao.do_insert(_mission)

            self.tree.create_node(
                tag="mission",
                identifier=_mission.mission_id,
                parent=self._root,
                data={"mission": _mission},
            )

            self.last_id = max(self.last_id, _mission.mission_id)

            pub.sendMessage(
                "succeed_insert_mission",
                node_id=_mission.mission_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mission",
                error_message=_error.msg,
            )
