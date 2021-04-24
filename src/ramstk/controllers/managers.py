# -*- coding: utf-8 -*-
#
#       ramstk.controllers.manager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package managers."""

# Standard Library Imports
import inspect
from typing import Any, Dict, List

# Third Party Imports
# noinspection PyPackageRequirements
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError


class RAMSTKAnalysisManager:
    """Contain the attributes and methods of an analysis manager.

    This class manages the analyses for RAMSTK modules.  Attributes of the
    analysis manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    :ivar tree: the treelib Tree() used to hold a copy of the data manager's
        tree.  This do not remain in-sync automatically.
    :type tree: :class:`treelib.Tree`
    :ivar RAMSTK_USER_CONFIGURATION: the instance of the
        RAMSTKUserConfiguration class associated with this analysis manager.
    :type RAMSTK_USER_CONFIGURATION: :class:`ramstk.RAMSTKUserConfiguration`
    """

    RAMSTK_USER_CONFIGURATION = None

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        """Initialize an instance of the hardware analysis manager.

        :param configuration: the RAMSTKUserConfiguration instance associated
            with the current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.RAMSTKUserConfiguration`
        """
        # Initialize private dictionary attributes.
        self._attributes: Dict[str, Any] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

    def on_get_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes for the analysis manager.

        :param attributes: the data manager's attributes dict.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def on_get_tree(self, tree: treelib.Tree) -> None:
        """Set the analysis manager's treelib Tree().

        :param tree: the data manager's treelib Tree().
        :return: None
        :rtype: None
        """
        self._tree = tree


class RAMSTKDataManager:
    """The meta-class for all RAMSTK Data Managers.

    :ivar tree: the treelib Tree()that will contain the structure of the RAMSTK
        module being modeled.
    :type tree: :class:`treelib.Tree`
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _root = 0
    _tag = ''

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize an RAMSTK data model instance."""
        # Initialize private dictionary attributes.
        self._pkey: Dict[str, List[str]] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id: int = 0
        self._revision_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao: BaseDatabase = BaseDatabase()
        self.last_id: int = 0
        self.tree: treelib.Tree = treelib.Tree()

        # Add the root to the Tree().  This is necessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        self.tree.create_node(tag=self._tag, identifier=self._root)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_connect, 'succeed_connect_program_database')
        pub.subscribe(self.do_set_tree,
                      'succeed_calculate_{}'.format(self._tag))
        pub.subscribe(self.do_update_all,
                      'request_update_all_{}'.format(self._tag))
        pub.subscribe(self.do_update_all, 'request_save_project')

    def do_connect(self, dao: BaseDatabase) -> None:
        """Connect data manager to a database.

        :param dao: the BaseDatabase() instance (data access object)
            representing the connected RAMSTK Program database.
        :type dao: :class:`ramstk.db.base.BaseDatabase`
        """
        self.dao = dao

    def do_create_all_codes(self, prefix: str) -> None:
        """Create codes for all MODULE data table records.

        :param prefix: the string to use as a prefix for each code.
        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            # noinspection PyUnresolvedReferences
            self.do_create_code(_node.identifier, prefix)  # type: ignore

    def do_delete(self, node_id: int, table: str) -> None:
        """Remove a RAMSTK data table record.

        :param node_id: the node ID to be removed from the RAMSTK Program
            database.
        :param table: the key in the module's treelib Tree() data package
            for the RAMSTK data table to remove the record from.
        :return: None
        :rtype: None
        """
        return self.dao.do_delete(self.do_select(node_id, table))

    def do_get_attributes(self, node_id: int, table: str) -> None:
        """Retrieve the RAMSTK data table attributes for node ID.

        :param node_id: the node ID in the treelib Tree to get the
            attributes for.
        :param table: the RAMSTK data table to retrieve the attributes from.
        :return: None
        :rtype: None
        """
        try:
            pub.sendMessage(
                'succeed_get_{0}_attributes'.format(table),
                attributes=self.do_select(node_id,
                                          table=table).get_attributes(),
            )
        except AttributeError:
            _method_name = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{0}: No attributes found for record ID {1} in '
                          '{2} table.'.format(_method_name, node_id, table))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_get_{0}_attributes'.format(table),
                error_message=_error_msg,
            )

    def do_select(self, node_id: Any, table: str) -> Any:
        """Retrieve the RAMSTK data table record for the Node ID passed.

        :param node_id: the Node ID of the data package to retrieve.
        :param table: the name of the RAMSTK data table to retrieve the
            attributes from.
        :return: the instance of the RAMSTK<MODULE> data table that was
            requested or None if the requested Node ID does not exist.
        :raise: KeyError if passed the name of a table that isn't managed by
            this manager.
        """
        try:
            _entity = self.tree.get_node(node_id).data[table]
        except (AttributeError, treelib.tree.NodeIDAbsentError, TypeError):
            _method_name = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{2}: No data package for node ID {0} in module {1}.'.format(
                    node_id, table, _method_name))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            _entity = None

        return _entity

    def do_set_attributes(self, node_id: List, package: Dict[str,
                                                             Any]) -> None:
        """Set the attributes of the record associated with node ID.

        :param node_id: the ID of the record in the RAMSTK Program database
            table whose attributes are to be set.
        :param package: the key:value pair of the attribute to set.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        for _table in self._pkey:
            try:
                _attributes = self.do_select(node_id[0],
                                             table=_table).get_attributes()
            except (AttributeError, KeyError):
                _method_name = inspect.currentframe(  # type: ignore
                ).f_code.co_name
                _error_msg: str = (
                    '{2}: No data package for node ID {0} in module '
                    '{1}.'.format(node_id[0], _table, _method_name))
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                _attributes = {}

            for _field in self._pkey[_table]:
                try:
                    _attributes.pop(_field)
                except KeyError:
                    pass

            if _key in _attributes:
                _attributes[_key] = _value

                self.do_select(node_id[0],
                               table=_table).set_attributes(_attributes)

        # noinspection PyUnresolvedReferences
        self.do_get_tree()  # type: ignore

    def do_set_tree(self, tree: treelib.Tree) -> None:
        """Set the MODULE treelib Tree().

        This method is generally used to respond to events such as successful
        calculations of the entire system.

        :param tree: the treelib Tree() to assign to the tree attribute.
        :return: None
        :rtype: None
        """
        self.tree = tree

    def do_update(self, node_id: int, table: str) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node ID of the record to save.
        :param table: the table in the database to update.
        :return: None
        :rtype: None
        """
        _method_name: str = inspect.currentframe(  # type: ignore
        ).f_code.co_name

        try:
            self.dao.do_update(self.tree.get_node(node_id).data[table])
            pub.sendMessage(
                'succeed_update_{}'.format(table),
                tree=self.tree,
            )
        except AttributeError:
            _error_msg: str = (
                '{1}: Attempted to save non-existent {2} with {2} ID {0}.'
            ).format(str(node_id), _method_name, table.replace('_', ' '))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_{}'.format(table),
                error_message=_error_msg,
            )
        except KeyError:
            _error_msg = ('{1}: No data package found for {2} ID {0}.').format(
                str(node_id), _method_name, table.replace('_', ' '))
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_{}'.format(table),
                error_message=_error_msg,
            )
        except (DataAccessError, TypeError):
            if node_id != 0:
                _error_msg = ('{1}: The value for one or more attributes for '
                              '{2} ID {0} was the wrong type.').format(
                                  str(node_id), _method_name,
                                  table.replace('_', ' '))
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                pub.sendMessage(
                    'fail_update_{}'.format(table),
                    error_message=_error_msg,
                )

    # noinspection PyUnresolvedReferences
    # pylint: disable=no-value-for-parameter
    def do_update_all(self) -> None:
        """Update all MODULE data table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            try:
                self.do_update(_node.identifier,
                               table=self._tag[:-1])  # type: ignore
            except TypeError:
                self.do_update(_node.identifier)  # type: ignore

        pub.sendMessage('succeed_update_all')
