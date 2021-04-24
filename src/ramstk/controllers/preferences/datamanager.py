# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.preferences.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Preferences Package Data Model."""

# Standard Library Imports
from typing import Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKProgramInfo


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Options data manager.

    This class manages the user-configurable Preferences and Options
    data from the Site and Program databases.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = 'preferences'
    _root = 0

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._pkey: Dict[str, List[str]] = {
            'programinfo': ['revision_id'],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_preference_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_preference_attributes')
        pub.subscribe(super().do_update, 'request_update_preference')

        pub.subscribe(self.do_get_tree, 'request_get_preferences_tree')

        pub.subscribe(self._do_select_all, 'succeed_connect_program_database')

    def do_get_tree(self) -> None:
        """Retrieve the Options treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_options_tree', tree=self.tree)

    def _do_select_all(self, dao: BaseDatabase) -> None:
        """Retrieve all the Options data from the RAMSTK Program database.

        :param dao: the RAMSTK option attributes for the
            selected Revision.
        :return: None
        :rtype: None
        """
        self.dao = dao

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        # noinspection PyUnresolvedReferences
        for _preference in self.dao.do_select_all(RAMSTKProgramInfo):
            self.tree.create_node(tag='programinfo',
                                  identifier=1,
                                  parent=self._root,
                                  data={'programinfo': _preference})

        pub.sendMessage(
            'succeed_retrieve_preferences',
            tree=self.tree,
        )
