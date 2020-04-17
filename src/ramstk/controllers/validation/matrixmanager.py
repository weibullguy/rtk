# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.matrixmanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Controller Package matrix manager."""

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import (
    RAMSTKHardware, RAMSTKRequirement, RAMSTKValidation
)


class MatrixManager(RAMSTKMatrixManager):
    """
    Contain the attributes and methods of the Validation matrix manager.

    This class manages the validation matrices for Requirements and Validation.
    Attributes of the validation Matrix Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the validation item being analyzed.
    """
    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs):
        """Initialize an instance of the validation matrix manager."""
        super().__init__(
            column_tables={
                # 'vldtn_rqrmnt':
                # [RAMSTKRequirement, 'requirement_id', 'requirement_code'],
                'vldtn_hrdwr': [RAMSTKHardware, 'hardware_id', 'comp_ref_des']
            },
            row_table=RAMSTKValidation)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        # // TODO: Update Requirement matrixmanager to respond to hardware.
        # //
        # // The Requirement module matrixmanager is currently only responding
        # // to Requirement module pubsub messages.  Ensure the Requirement
        # // module matrix manager is updated to respond to Hardware module
        # // pubsub messages when the Hardware module is refactored.
        pub.subscribe(self.do_create_rows, 'succeed_retrieve_validations')
        pub.subscribe(self._do_create_validation_matrix_columns,
                      'succeed_retrieve_hardware')
        pub.subscribe(self._on_delete_validation,
                      'succeed_delete_validation')
        # pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        # pub.subscribe(self._on_delete_requirement,
        #               'succeed_delete_requirement')
        pub.subscribe(self._on_insert_validation, 'succeed_insert_validation')
        # pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')
        # pub.subscribe(self._on_insert_requirement,
        #               'succeed_insert_requirement')
        pub.subscribe(self.do_update, 'request_update_validation_matrix')

    def _do_create_validation_matrix_columns(self,
                                             tree: treelib.Tree) -> None:
        """
        Create the Validation data matrix columns.

        :param tree: the treelib Tree() containing the correlated workflow
            module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._col_tree = tree

        if tree.get_node(0).tag == 'hardware':
            super().do_create_columns('vldtn_hrdwr')
            pub.sendMessage('request_select_matrix',
                            matrix_type='vldtn_hrdwr')

    def _on_delete_hardware(self, node_id):
        """
        Delete the node ID column from the Validation::Hardware matrix.

        :param int node_id: the hardware treelib Node ID that was deleted.
            Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_delete_column(self, node_id,
                                                    'vldtn_hrdwr')

    def _on_delete_requirement(self, node_id):
        """
        Delete the node ID column from the Validation::Requirements matrix.

        :param int node_id: the requirement treelib Node ID that was deleted.
            Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_delete_column(self, node_id,
                                                    'vldtn_rqrmnt')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_validation(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Delete the matrix row associated with the deleted validation.

        :param int node_id: the treelib Tree() node ID associated with the
            deleted validation.
        :param tree: the treelib Tree() containing the remaining validation
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    def _on_insert_hardware(self, node_id):
        """
        Insert the node ID column to the Validation::Hardware matrix.

        :param int node_id: the hardware treelib Node ID that is to be
            inserted.  Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_insert_column(self, node_id,
                                                    'vldtn_hrdwr')

    def _on_insert_requirement(self, node_id):
        """
        Insert the node ID column to the Hardware::Requirements matrix.

        :param int node_id: the requirement treelib Node ID that is to be
            inserted.  Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_insert_column(self, node_id,
                                                    'vldtn_rqrmnt')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_validation(self, node_id: int, tree: treelib.Tree) -> None:
        """

        :param int node_id: the treelib Tree() node ID associated with the
            inserted validation.
        :param tree: the treelib Tree() containing the remaining validation
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)
