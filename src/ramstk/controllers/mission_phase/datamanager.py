# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mission_phase.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKMissionPhase


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Usage Profile data manager.

    This class manages the usage profile data from the
    RAMSTKMissionPhase data models.
    """

    _tag = "mission_phases"

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a RAMSTKMissionPhase data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "mission_phase": ["revision_id", "mission_id", "phase_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mission_phase_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mission_phase_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_mission_phase")
        pub.subscribe(super().do_update, "request_update_mission_phase")

        pub.subscribe(self.do_select_all, "selected_revision")
        pub.subscribe(self.do_get_tree, "request_get_mission_phase_tree")

        pub.subscribe(self._do_delete, "request_delete_mission_phase")
        pub.subscribe(self._do_insert_mission_phase, "request_insert_mission_phase")

    def do_get_tree(self) -> None:
        """Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_mission_phase_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Usage Profile data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _phase in self.dao.do_select_all(
            RAMSTKMissionPhase, key=["revision_id"], value=[self._revision_id]
        ):
            self.tree.create_node(
                tag="mission_phase",
                identifier=_phase.phase_id,
                parent=self._root,
                data={"mission_phase": _phase},
            )
            self.last_id = _phase.phase_id

        pub.sendMessage(
            "succeed_retrieve_mission_phases",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a usage profile element.

        :param node_id: the usage profile element ID to remove.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, "mission_phase")

            self.tree.remove_node(node_id)

            pub.sendMessage(
                "succeed_delete_mission_phase",
                tree=self.tree,
            )
        except (DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent mission phase ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_mission_phase",
                error_message=_error_msg,
            )

    def _do_insert_mission_phase(self, mission_id: int) -> None:
        """Add a new mission phase for mission ID.

        :param mission_id: the mission ID to add the new mission phase.
        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id("ramstk_mission_phase", "phase_id")
            _phase = RAMSTKMissionPhase()
            _phase.mission_id = mission_id
            _phase.phase_id = _last_id + 1

            self.dao.do_insert(_phase)

            self.tree.create_node(
                tag="mission_phase",
                identifier=_phase.phase_id,
                parent=self._root,
                data={"mission_phase": _phase},
            )

            self.last_id = max(self.last_id, _phase.phase_id)

            pub.sendMessage(
                "succeed_insert_mission_phase",
                node_id=_phase.phase_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mission_phase",
                error_message=_error.msg,
            )
