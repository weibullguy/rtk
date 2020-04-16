# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.matrix.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseMatrix Module."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import pandas as pd

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, _

# RAMSTK Local Imports
from . import treeview


# noinspection PyUnresolvedReferences
class RAMSTKMatrixView(Gtk.HBox):
    """
    The RAMSTK base widget for displaying RAMSTK Matrix views.

    The attributes of an RAMSTKBaseMatrix are:

    :ivar int _n_columns: the number of columns in the matrix.
    :ivar int _n_rows: the number rows in the matrix.
    :ivar list dic_icons: dictionary of icons to use in the various
        RAMSTKMatrix views.
    :ivar matrix: the RAMSTKDataMatrix to display in the Matrix View.
    :ivar matrixview: the Gtk.TreeView() displaying the RAMSTKDataMatrix.
    :type matrixview: :class:`Gtk.TreeView`
    """
    def __init__(self, module: str) -> None:
        """
        Initialize a RAMSTKMatrixView() instance.

        :return: None
        :rtype: None
        """
        GObject.GObject.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._matrix_type = module
        self._n_columns = 0
        self._n_rows = 0
        self._revision_id = None

        # Initialize public dictionary attributes.
        self.dic_icons = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.matrix = None
        self.matrixview = Gtk.TreeView()
        self.n_fixed_columns = 0

        # Subscribe to PyPubSub messages.

    @staticmethod
    def _do_make_combo_cell() -> Gtk.CellRendererCombo:
        """
        Make a Gtk.CellRendererCombo().

        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        _cell = Gtk.CellRendererCombo()
        _cellmodel = Gtk.ListStore(GObject.TYPE_STRING)
        _cellmodel.append([""])
        _cellmodel.append([_("Partial")])
        _cellmodel.append([_("Complete")])
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        return _cell

    @staticmethod
    def _resize_wrap(column: Gtk.TreeViewColumn, __param: Any,
                     cell: Gtk.CellRenderer) -> None:
        """
        Dynamically set the wrap-width property for a Gtk.CellRenderer().

        This method is called when the column width is resized.

        :param column: the Gtk.TreeViewColumn() being resized.
        :type column: :class:`Gtk.TreeViewColumn`
        :param GParamInt __param: the triggering parameter.
        :param cell: the Gtk.CellRenderer() that needs to be resized.
        :type cell: :class:`Gtk.CellRenderer`
        :return: None
        :rtype: None
        """
        _width = column.get_width()

        if _width > 0:
            _width += 10

        cell.set_property('wrap-width', _width)

    # pylint: disable=too-many-arguments
    def do_edit_cell(self,
                     cell: Gtk.CellRendererCombo,
                     path: str,
                     row: Gtk.TreeIter,
                     model: Gtk.TreeModel,
                     **kwargs) -> None:
        """
        Respond to `changed` signals for the Gtk.CellRendererCombo()s.

        :param cell: the Gtk.CellRendererCombo() calling this method.
        :type cell: :class:`Gtk.CellRendererCombo`
        :param str path: the path of the selected row in the RAMSTKMatrix.
        :param row: the Gtk.TreeIter() for the Gtk.CellRendererCombo() in the
            selected row in the RAMSTKMatrix.
        :type row: :class:`Gtk.TreeIter`
        :param int position: the position of the cell in the RAMSTKMatrix.
        :param int col_index: the column_item_id of the Matrix cell to be
            edited.
        :param model: the Gtk.TreeModel() associated with the RAMSTKMatrix.
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        try:
            _idx_column = kwargs['col_index']
        except KeyError:
            _idx_column = 0
        try:
            _position = kwargs['position']
        except KeyError:
            _position = 0

        _model = cell.get_property('model')

        _idx_row = model[path][0]
        if _model.get_value(row, 0) == 'Partial':
            self.matrix[_idx_column][_idx_row] = 1
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self._dic_icons[1], 22, 22)
        elif _model.get_value(row, 0) == 'Complete':
            self.matrix[_idx_column][_idx_row] = 2
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self._dic_icons[2], 22, 22)
        else:
            self.matrix[_idx_column][_idx_row] = 0
            _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self._dic_icons[0], 22, 22)

        model[path][_position - 1] = _pixbuf

    def do_load_matrix(self, matrix: pd.DataFrame,
                       column_headings: Dict[int, str],
                       row_headings: Dict[int, str]) -> None:
        """
        Load the RAMSTKMatrixView with the values from the data matrix.

        :param matrix: the data to display in the RAMSTKMatrixView() widget.
        :type matrix: :class:`pandas.DataFrame`
        :param dict column_headings: the dicionary containing the headings to
            use for the matrix columns.  Keys are the column <MODULE> IDs;
            values are a noun field associated with the key.
        :param dict row_headings: the dictionary containing the headings to
            use for the matrix rows.  Keys are the row <MODULE> IDs; values are
            a noun field associated with the key.
        :return: None
        :rtype: None
        """
        self.matrix = matrix
        self._n_columns = len(self.matrix.columns)
        self._n_rows = len(self.matrix.index)

        _gobject_types = [GObject.TYPE_INT, GObject.TYPE_STRING] + \
                         [GdkPixbuf.Pixbuf, GObject.TYPE_STRING] * \
                         (self._n_columns) + [GObject.TYPE_STRING]

        _model = Gtk.TreeStore(*_gobject_types)

        self.matrixview.set_model(_model)

        # The first column will contain a cell for the Function ID and Function
        # Code.  The Function ID will not be visible, but can be used for
        # program control.
        _id_cell = Gtk.CellRendererText()
        treeview.do_set_cell_properties(_id_cell, bg_color='light gray',
                                        visible=False)

        _code_cell = Gtk.CellRendererText()
        treeview.do_set_cell_properties(_code_cell, bg_color='light gray')
        _code_cell.set_alignment(0.9, 0.5)

        _column = treeview.do_make_column([_id_cell, _code_cell])
        _column.set_attributes(_id_cell, text=0)
        _column.set_attributes(_code_cell, markup=1)

        self.matrixview.append_column(_column)

        # The remaining columns will be Gtk.CellRendererCombo()'s for
        # displaying the interaction between Function and Hardware.
        j = 2
        for i in range(self._n_columns):  # pylint: disable=E0602
            _cell = self._do_make_combo_cell()
            treeview.do_set_cell_properties(_cell, editable=True)
            _cell.connect('changed', self.do_edit_cell, _model,
                          position=i + j + 1,
                          col_index=self.matrixview.columns[i])

            _pbcell = Gtk.CellRendererPixbuf()
            _pbcell.set_property('xalign', 0.5)
            _heading = column_headings[self.matrixview.columns[i]]
            _column = treeview.do_make_column([_pbcell, _cell],
                                              heading=_heading)
            _column.set_attributes(_pbcell, pixbuf=i + j)
            self.matrixview.append_column(_column)

            j += 1

        # Add one more column so the last column will not be extra wide.
        _column = treeview.do_make_column([Gtk.CellRendererText()])

        try:
            # pylint: disable=undefined-loop-variable
            _column.set_attributes(_cell, text=i + j + 1)
        except UnboundLocalError:
            _column.set_visible(False)

        self.matrixview.append_column(_column)

        # Now we load the data into the RAMSTK Matrix View.
        for i in list(self.matrix.index):
            _data = [i, "<span weight='bold'>" + row_headings[i] + "</span>"]
            for j in list(self.matrix.loc[i]):
                _pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons[j], 22, 22)
                _data.append(_pixbuf)
                _data.append(j)
            _data.append('')

            _model.append(None, _data)