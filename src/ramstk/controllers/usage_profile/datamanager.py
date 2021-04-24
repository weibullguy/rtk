# -*- coding: utf-8 -*-
#
#       ramstk.controllers.usage_profile.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Usage Profile data manager.

    This class manages the usage profile data from the RAMSTKMission,
    RAMSTKMissionPhase, and RAMSKTEnvironment data models.
    """

    _tag = "usage_profiles"

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a RAMSTKFailureDefinition, data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._environment_tree: Tree = Tree()
        self._mission_tree: Tree = Tree()
        self._mission_phase_tree: Tree = Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_environment_tree, "succeed_retrieve_environments")
        pub.subscribe(self.do_set_mission_tree, "succeed_retrieve_missions")
        pub.subscribe(self.do_set_mission_phase_tree, "succeed_retrieve_mission_phases")
        pub.subscribe(self.do_set_environment_tree, "succeed_delete_environment")
        pub.subscribe(self.do_set_mission_tree, "succeed_delete_mission")
        pub.subscribe(self.do_set_mission_phase_tree, "succeed_delete_mission_phase")

        pub.subscribe(self._on_insert, "succeed_insert_environment")
        pub.subscribe(self._on_insert, "succeed_insert_mission")
        pub.subscribe(self._on_insert, "succeed_insert_mission_phase")

    def do_set_environment_tree(self, tree: Tree) -> None:
        """Set the environment treelib Tree().

        :param tree: the environment package treelib Tree().
        :return: None
        :rtype: None
        """
        self._environment_tree = tree
        self.on_select_all()

    def do_set_mission_tree(self, tree: Tree) -> None:
        """Set the mission treelib Tree().

        :param tree: the mission package treelib Tree().
        :return: None
        :rtype: None
        """
        self._mission_tree = tree
        self.on_select_all()

    def do_set_mission_phase_tree(self, tree: Tree) -> None:
        """Set the mission phase treelib Tree().

        :param tree: the mission phase package treelib Tree().
        :return: None
        :rtype: None
        """
        self._mission_phase_tree = tree
        self.on_select_all()

    def on_select_all(self) -> None:
        """Build the usage profile treelib Tree().

        This method builds the hierarchical treelib Tree() from the individual
        mission, mission phase, and environment trees.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        if (
            self._mission_tree.depth() > 0
            and self._mission_phase_tree.depth() > 0
            and self._environment_tree.depth() > 0
        ):
            self._do_load_missions()

            pub.sendMessage(
                "succeed_retrieve_usage_profile",
                tree=self.tree,
            )

    def _do_load_environments(self, phase_id: int, parent_id: str) -> None:
        """Load the environments into the tree for the passed phase ID.

        :param phase_id: the mission phase ID to load the environments for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._environment_tree.all_nodes()[1:]:
            _environment = _node.data["environment"]
            _node_id = "{}.{}".format(parent_id, _environment.environment_id)

            if _environment.phase_id == phase_id:
                self.tree.create_node(
                    tag="environment",
                    identifier=_node_id,
                    parent=parent_id,
                    data={"usage_profile": _environment},
                )

    def _do_load_missions(self) -> None:
        """Load the missions into the tree for the passed mission ID.

        :return: None
        :rtype: None
        """
        for _node in self._mission_tree.all_nodes()[1:]:
            _mission = _node.data["mission"]
            _node_id = "{}".format(_mission.mission_id)

            self.tree.create_node(
                tag="mission",
                identifier=_node_id,
                parent=self._root,
                data={"usage_profile": _mission},
            )

            self._do_load_mission_phases(_mission.mission_id)

    def _do_load_mission_phases(self, mission_id: int) -> None:
        """Load the mission phases into the tree for the passed mission ID.

        :param mission_id: the mission ID to add the new mission phase.
        :return: None
        :rtype: None
        """
        for _node in self._mission_phase_tree.all_nodes()[1:]:
            _mission_phase = _node.data["mission_phase"]
            _node_id = "{}.{}".format(mission_id, _mission_phase.phase_id)

            if _mission_phase.mission_id == mission_id:
                self.tree.create_node(
                    tag="mission_phase",
                    identifier=_node_id,
                    parent="{}".format(mission_id),
                    data={"usage_profile": _mission_phase},
                )

                self._do_load_environments(_mission_phase.phase_id, _node_id)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert(self, tree: Tree, node_id: int) -> None:
        """Wrap _do_set_tree() on insert.

        succeed_insert_<module> messages have node_id in the broadcast data
        so this method is needed to wrap the _do_set_tree() method.

        :param tree: the treelib Tree() passed by the calling message.
        :param node_id: the node ID of the element that was inserted.
            Unused in this method but required for compatibility with the
            'succeed_insert_<module>' message data.
        :return: None
        :rtype: None
        """
        _module: str = tree.get_node(0).tag

        _function = {
            "missions": self.do_set_mission_tree,
            "mission_phases": self.do_set_mission_phase_tree,
            "environments": self.do_set_environment_tree,
        }[_module]

        # noinspection PyArgumentList
        _function(tree)
