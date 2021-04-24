# -*- coding: utf-8 -*-
#
#       ramstk.controllers.pof.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""PoF Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the PoF data manager.

    This class manages the PoF data from the RAMSTKMode,
    RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod
    data models.
    """

    _tag = "pofs"

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a PoF data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._mechanism_tree: Tree = Tree()
        self._opload_tree: Tree = Tree()
        self._opstress_tree: Tree = Tree()
        self._test_method_tree: Tree = Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_mechanism_tree, "succeed_retrieve_mechanisms")
        pub.subscribe(self.do_set_opload_tree, "succeed_retrieve_oploads")
        pub.subscribe(self.do_set_opstress_tree, "succeed_retrieve_opstresss")
        pub.subscribe(self.do_set_test_method_tree, "succeed_retrieve_test_methods")
        pub.subscribe(self.do_set_mechanism_tree, "succeed_delete_mechanism")
        pub.subscribe(self.do_set_opload_tree, "succeed_delete_opload")
        pub.subscribe(self.do_set_opstress_tree, "succeed_delete_opstress")
        pub.subscribe(self.do_set_test_method_tree, "succeed_delete_test_method")

        pub.subscribe(self._on_insert, "succeed_insert_mechanism")
        pub.subscribe(self._on_insert, "succeed_insert_opload")
        pub.subscribe(self._on_insert, "succeed_insert_opstress")
        pub.subscribe(self._on_insert, "succeed_insert_test_method")

    def do_set_mechanism_tree(self, tree: Tree) -> None:
        """Set the failure mechanism treelib Tree().

        :param tree: the failure mechanism package treelib Tree().
        :return: None
        :rtype: None
        """
        self._mechanism_tree = tree
        self.on_select_all()

    def do_set_opload_tree(self, tree: Tree) -> None:
        """Set the operating load treelib Tree().

        :param tree: the operating load package treelib Tree().
        :return: None
        :rtype: None
        """
        self._opload_tree = tree
        self.on_select_all()

    def do_set_opstress_tree(self, tree: Tree) -> None:
        """Set the operating stress treelib Tree().

        :param tree: the operating stress package treelib Tree().
        :return: None
        :rtype: None
        """
        self._opstress_tree = tree
        self.on_select_all()

    def do_set_test_method_tree(self, tree: Tree) -> None:
        """Set the test method treelib Tree().

        :param tree: the test method package treelib Tree().
        :return: None
        :rtype: None
        """
        self._test_method_tree = tree
        self.on_select_all()

    def on_select_all(self) -> None:
        """Build the physics of failure treelib Tree().

        This method builds the hierarchical treelib Tree() from the individual
        mechanism, opload, opstress, and test method trees.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        if self._mechanism_tree.depth() > 0:
            self._do_load_mechanisms()

            pub.sendMessage(
                "succeed_retrieve_pof",
                tree=self.tree,
            )

    def _do_load_mechanisms(self) -> None:
        """Load the missions into the tree for the passed mission ID.

        :return: None
        :rtype: None
        """
        for _node in self._mechanism_tree.all_nodes()[1:]:
            _mechanism = _node.data["mechanism"]
            _node_id = "{}".format(_mechanism.mechanism_id)

            self.tree.create_node(
                tag="mechanism",
                identifier=_node_id,
                parent=self._root,
                data={"pof": _mechanism},
            )

            self._do_load_oploads(_mechanism.mechanism_id)

    def _do_load_oploads(self, mechanism_id: int) -> None:
        """Load the operating loads into the tree for the passed mechanism ID.

        :param mechanism_id: the failure mechanism ID to add the new operating load.
        :return: None
        :rtype: None
        """
        for _node in self._opload_tree.all_nodes()[1:]:
            _opload = _node.data["opload"]
            _node_id = "{}.{}".format(mechanism_id, _opload.load_id)

            if _opload.mechanism_id == mechanism_id:
                self.tree.create_node(
                    tag="opload",
                    identifier=_node_id,
                    parent="{}".format(mechanism_id),
                    data={"pof": _opload},
                )

                self._do_load_opstress(_opload.load_id, _node_id)
                self._do_load_test_method(_opload.load_id, _node_id)

    def _do_load_opstress(self, load_id: int, parent_id: str) -> None:
        """Load the operating stresses into the tree for the passed load ID.

        :param load_id: the operating load ID to load the operating stresses for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._opstress_tree.all_nodes()[1:]:
            _opstress = _node.data["opstress"]
            _node_id = "{}.{}s".format(parent_id, _opstress.stress_id)

            if _opstress.load_id == load_id:
                self.tree.create_node(
                    tag="opstress",
                    identifier=_node_id,
                    parent=parent_id,
                    data={"pof": _opstress},
                )

    def _do_load_test_method(self, load_id: int, parent_id: str) -> None:
        """Load the operating stresses into the tree for the passed load ID.

        :param load_id: the operating load ID to load the operating stresses for.
        :param parent_id: the parent node ID.
        :return: None
        :rtype: None
        """
        for _node in self._test_method_tree.all_nodes()[1:]:
            _test_method = _node.data["test_method"]
            _node_id = "{}.{}t".format(parent_id, _test_method.test_id)

            if _test_method.load_id == load_id:
                self.tree.create_node(
                    tag="test_method",
                    identifier=_node_id,
                    parent=parent_id,
                    data={"pof": _test_method},
                )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert(self, tree: Tree, node_id: int) -> None:
        """Wrap _do_set_<module>_tree() on insert.

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
            "mechanisms": self.do_set_mechanism_tree,
            "oploads": self.do_set_opload_tree,
            "opstresss": self.do_set_opstress_tree,
            "test_method": self.do_set_test_method_tree,
        }[_module]

        # noinspection PyArgumentList
        _function(tree)
