# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 panel Module."""

# Standard Library Imports
import inspect
from typing import Any, Dict, List, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
import treelib
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import boolean_to_integer
from ramstk.views.gtk3 import Gtk, _

# RAMSTK Local Imports
from .button import RAMSTKCheckButton
from .combo import RAMSTKComboBox
from .entry import RAMSTKEntry, RAMSTKTextView
from .frame import RAMSTKFrame
from .label import RAMSTKLabel, do_make_label_group
from .plot import RAMSTKPlot
from .scrolledwindow import RAMSTKScrolledWindow
from .treeview import RAMSTKTreeView

register_matplotlib_converters()


class RAMSTKPanel(RAMSTKFrame):
    """The RAMSTKPanel class.

    Implementations of the RAMSTKPanel() class should provide the following
    methods:

    __do_set_callbacks() to set the callback method for the widgets in the
        panel.  The use of the public methods on_changed_combo(),
        on_changed_entry(), on_focus_out(), and on_toggled() in this
        meta-class shall be the preferred callback methods.
    __do_set_properties() to set the properties of the widgets in the panel.

    Implementations of the RAMSTKPanel() class may provide the following
    methods:

    _do_clear_panel() to clear the contents of the widgets in the panel.
        Connect this as a listener for the 'closed_program' signal.
    _do_load_panel() to load the attribute data into the widgets in the
        panel.  Connect this as a listener for the 'selected_<module>' for
        the work stream module the panel is associated with.

    There are three types of panels that can be created.  These are:

        * fixed: a panel containing a Gtk.Fixed() populated with labels
            and widgets.
        * plot: a panel containing a RAMSTKPlot().
        * treeview: a panel containing a RAMSTKTreeView().

    The attributes of a RAMSTKPanel are:

    :ivar _dic_attribute_keys: contains key:value pairs where the key is
        the nominal column number in the RAMSTKTreeView() where the attribute
        data is displayed.  The value is a list with the name of the attribute
        in position 0 and the attribute's data type in position 1.  An example
        entry in this dict might be:

            15: ['name', 'string']

        which indicates the nominal index of the Hardware RAMSTKTreeView()
        column at position 15 contains the data for attribute 'name' and
        this is 'string' data.  The nominal index is the default position of
        the column in a RAMSTKTreeView().  Refer to the layout file for the
        nominal position of each attribute for a given work stream module.
    :ivar _dic_attribute_updater: contains key:value pairs where the
        key is the name of the attribute and the value is a list with the
        method used to update a widget's display in position 0, the
        name of the signal to block while updating the widget in position 1,
        and the nominal column number in the RAMSTKTreeView() where the
        attribute data is displayed in position 2.  An example entry in this
        dict might be:

            'derived': [self.chkDerived.do_update, 'toggled', 2]

        which indicates the 'derived' attribute of the Requirement should use
        the do_update() method of the RAMSTKCheckButton() when the
        'toggled' signal is emitted and the nominal index for this
        attribute is 2.  The nominal index is the default position of the
        column in a RAMSTKTreeView().  Refer to the layout file for the
        nominal position of each attribute for a given work stream module.
    :ivar _dic_row_loader: contains the methods used to load the row data
        into a RAMSTKTreeView() where the key is the name of the module and
        the value is the method.  This is necessary for those views that
        combine different tables such as the usage profile or FMEA.  Having
        different loader methods for each type of entity may be needed to
        load the data for each entity in the correct order.  Most work
        stream modules will simple use the do_load_row() method of this
        meta-class.  Example entries in this dict might be:

        'mission': self.__do_load_mission
        'function': super().do_load_row

    :ivar _lst_labels: the list of text to display in the labels
        for each widget in a panel.
    :ivar _lst_widgets: the list of widgets to display in a panel.
    :ivar _parent_id: the ID of the parent entity for the selected work stream
        entity.  This is needed for hierarchical modules such as the
        function module.  For flat modules, this will always be zero.
    :ivar _record_id: the work stream module ID whose attributes
        this panel is displaying.
    :ivar _title: the title to place on the RAMSTKFrame() that is
        this panel's container.

    :ivar fmt: the formatting string for displaying float values.
    :ivar pltPlot: a RAMSTPlot() for the panels that embed a plot.
    :ivar tvwTreeView: a RAMSTKTreeView() for the panels that embed a
        treeview.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = ""

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize private dict instance attributes.
        # TODO: _dic_attribute_keys renamed to _dic_attribute_index?
        # This may be more descriptive of the information the dict holds.
        self._dic_attribute_keys: Dict[int, List[str]] = {}
        self._dic_attribute_updater: Dict[str, Any] = {}
        self._dic_row_loader: Dict[str, Any] = {}

        # Initialize private list instance attributes.
        self._lst_col_order: List[int] = []
        self._lst_labels: List[str] = []
        self._lst_widgets: List[object] = []

        # Initialize private scalar instance attributes.
        self._parent_id: int = -1
        self._record_id: int = -1
        self._title: str = ""
        self._tree_loaded: bool = False

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = "{0:0.6}"

        self.pltPlot: RAMSTKPlot = RAMSTKPlot()
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

        # Subscribe to PyPubSub messages.

    def do_clear_tree(self) -> None:
        """Clear the contents of a RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        try:
            _model.clear()
        except AttributeError:
            pass

    def do_expand_tree(self) -> None:
        """Expand the RAMSTKTreeView.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        try:
            _row = _model.get_iter_first()
        except AttributeError:
            _row = None

        self.tvwTreeView.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwTreeView.get_column(0)
            self.tvwTreeView.set_cursor(_path, None, False)

            self.tvwTreeView.row_activated(_path, _column)

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    def do_load_panel(
        self,
        tree: treelib.Tree = treelib.Tree(),
        node_id: Any = "",
        row: Gtk.TreeIter = None,
    ) -> None:
        """Load data into the RAMSTKPanel() widgets.

        :param tree: the module's treelib Tree().
        :param node_id: unused in this function.  Required so this method
            can be used as the subscriber for 'succeed_insert_{0}' messages.
        :param row: the parent row in the RAMSTKTreeView() to add the new item.
        :return: None
        """
        _node = tree.nodes[list(tree.nodes.keys())[0]]

        _new_row = self._do_load_row(_node, row)

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self.do_load_panel(_child_tree, row=_new_row)

        self.do_expand_tree()

        pub.sendMessage("request_set_cursor_active")

    def do_load_row(self, attributes: Dict[str, Any]) -> None:
        """Use the _do_load_row() method and populate the panel's
        _dic_row_loader attributes with the correct method(s) to load a row's
        data.

        This varies depending on the work stream module.
        """
        _model = self.tvwTreeView.get_model()

        _data = []
        for _key in self.tvwTreeView.korder:
            _data.append(attributes[self.tvwTreeView.korder[_key]])

        # Only load items that are immediate children of the selected item and
        # prevent loading the selected item itself in the worksheet.
        if not _data[1] == self._record_id and not self._tree_loaded:
            _model.append(None, _data)

    def do_load_tree(self, tree: treelib.Tree) -> None:
        """Load the RAMSTKTreeView().

        :param tree: the treelib Tree containing the module to load.
        :return: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

        try:
            _tag = tree.get_node(0).tag[:-1]
        except AttributeError:
            _tag = "UNK"

        try:
            self.tvwTreeView.do_load_tree(tree, _tag)
            self.tvwTreeView.expand_all()
            _row = _model.get_iter_first()
            if _row is not None:
                self.tvwTreeView.selection.select_iter(_row)
                self.show_all()
        except TypeError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while loading {1} data for Record "
                "ID {0} into the view.  One or more values from the "
                "database was the wrong type for the column it was trying to "
                "load."
            ).format(self._record_id, self._module, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
        except ValueError:
            _method_name = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while loading {1:s} data for Record "
                "ID {0:d} into the view.  One or more values from the "
                "database was missing."
            ).format(self._record_id, self._module, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def do_make_panel_fixed(self, **kwargs: Dict[str, Any]) -> None:
        """Create a panel with the labels and widgets on a Gtk.Fixed().

        :return: None
        :rtype: None
        """
        _justify = kwargs.get("justify", Gtk.Justification.RIGHT)

        _fixed: Gtk.Fixed = Gtk.Fixed()

        _y_pos: int = 5
        # noinspection PyTypeChecker
        (_x_pos, _labels) = do_make_label_group(
            self._lst_labels,
            bold=False,  # type: ignore
            justify=_justify,
            x_pos=5,  # type: ignore
            y_pos=5,  # type: ignore
        )
        for _idx, _label in enumerate(_labels):
            _fixed.put(_label, 5, _y_pos)

            _minimum: Gtk.Requisition = self._lst_widgets[  # type: ignore
                _idx
            ].get_preferred_size()[0]
            if _minimum.height <= 0:
                _minimum.height = self._lst_widgets[_idx].height  # type: ignore

            # RAMSTKTextViews are placed inside a scrollwindow so that's
            # what needs to be placed on the container.
            if isinstance(self._lst_widgets[_idx], RAMSTKTextView):
                _fixed.put(
                    self._lst_widgets[_idx].scrollwindow,  # type: ignore
                    _x_pos + 10,
                    _y_pos,
                )
                _y_pos += _minimum.height + 30
            elif isinstance(self._lst_widgets[_idx], RAMSTKCheckButton):
                _fixed.put(self._lst_widgets[_idx], _x_pos + 10, _y_pos)
                _y_pos += _minimum.height + 30
            else:
                _fixed.put(self._lst_widgets[_idx], _x_pos + 10, _y_pos)
                _y_pos += _minimum.height + 5

        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(_fixed)

        self.add(_scrollwindow)

    def do_make_panel_plot(self) -> None:
        """Create a panel with a RAMSTKPlot().

        :return: None
        :rtype: None
        """
        self._lst_widgets.append(self.pltPlot)

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.pltPlot.canvas)

        self.add(_scrollwindow)

    def do_make_panel_treeview(self) -> None:
        """Create a panel with a RAMSTKTreeView().

        :return: None
        """
        self._lst_widgets.append(self.tvwTreeView)

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwTreeView)

        self.add(_scrollwindow)

    def do_make_treeview(self, **kwargs: Dict[str, Any]) -> None:
        """Make the RAMSTKTreeView() instance for this panel.

        :return: None
        :rtype: None
        """
        _bg_color: str = kwargs.get("bg_color", "#FFFFFF")  # type: ignore
        _fg_color: str = kwargs.get("fg_color", "#000000")  # type: ignore
        _fmt_file: str = kwargs.get("fmt_file", "")  # type: ignore

        self.tvwTreeView.do_parse_format(_fmt_file)
        self.tvwTreeView.do_make_model()
        self.tvwTreeView.do_make_columns(
            colors={"bg_color": _bg_color, "fg_color": _fg_color}
        )

        self._lst_col_order = list(self.tvwTreeView.position.values())

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_refresh_tree(self, node_id: List, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This method is used to update a RAMSTKPanel() containing a
        RAMSTKTreeView() [generally the module view] whenever a work view
        widget is edited.  It is used to keep the data displayed in-sync.

        A dict 'package' is sent when a workview widget is edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The key in the 'package' is used to find the value in
        _dic_attribute_updater corresponding to the data being changed.
        Position 2 of the _dic_attribute_updater value list is the nominal
        position in the RAMSTKTreeView() containing the same attribute data
        as the one being changed.

        :param node_id: unused in this method.
        :param package: the key:value for the data being updated.
        :return: None
        """
        [[_key, _value]] = package.items()

        try:
            _position = self._lst_col_order[self._dic_attribute_updater[_key][2]]

            _model, _row = self.tvwTreeView.get_selection().get_selected()
            _model.set(_row, _position, _value)
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while refreshing {1} data for Record "
                "ID {0} in the view.  Key {3} does not exist in "
                "attribute dictionary."
            ).format(self._record_id, self._module, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
        except TypeError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while refreshing {1} data for Record "
                "ID {0} in the view.  Data {4} for {3} is the wrong "
                "type."
            ).format(self._record_id, self._module, _method_name, _key, _value)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def do_set_callbacks(self) -> None:
        """Set the callback methods for RAMSTKTreeView().

        :return: None
        """
        self.tvwTreeView.dic_handler_id["changed"] = self.tvwTreeView.selection.connect(
            "changed", self._on_row_change
        )

    def do_set_cell_callbacks(self, message: str, columns: List[int]) -> None:
        """Set the callback methods for RAMSTKTreeView() cells.

        :param message: the PyPubSub message to broadcast on a
            successful edit.
        :param columns: the list of column numbers whose cells should
            have a callback function assigned.
        :return: None
        """
        for _idx in columns:
            _cell = self.tvwTreeView.get_column(self._lst_col_order[_idx]).get_cells()
            try:
                _cell[0].connect("edited", self.on_cell_edit, _idx, message)
            except TypeError:
                _cell[0].connect("toggled", self.on_cell_toggled, _idx, message)

    def do_set_headings(self) -> None:
        """Set the treeview headings depending on the selected row.

        It's used when the tree displays an aggregation of models such as
        the FMEA or PoF.  This method applies the appropriate headings when
        a row is selected.

        :return: None
        :rtype: None
        """
        _columns = self.tvwTreeView.get_columns()
        i = 0
        for _key in self.tvwTreeView.headings:
            _label = RAMSTKLabel(
                "<span weight='bold'>" + self.tvwTreeView.headings[_key] + "</span>"
            )
            _label.do_set_properties(
                height=-1, justify=Gtk.Justification.CENTER, wrap=True
            )
            _label.show_all()
            _columns[i].set_widget(_label)
            _columns[i].set_visible(self.tvwTreeView.visible[_key])

            i += 1

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**kwargs)

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
        self.tvwTreeView.set_rubber_banding(True)

    def on_cell_edit(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_text: str,
        position: int,
        message: str,
    ) -> None:
        """Handle edits of the RAMSTKTreeview() in a treeview panel.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        """
        try:
            _keys = list(self.tvwTreeView.position.keys())
            _vals = list(self.tvwTreeView.position.values())
            _col = _keys[_vals.index(position)]
            _key = self.tvwTreeView.korder[_col]
            _position = self.tvwTreeView.position[_col]

            _new_text = self.tvwTreeView.do_edit_cell(cell, path, new_text, _position)
            pub.sendMessage(
                message,
                node_id=[self._record_id, ""],
                package={_key: _new_text},
            )
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while editing {1} data for record "
                "ID {0} in the view.  One or more keys could not be found in "
                "the attribute dictionary."
            ).format(self._record_id, self._module, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    # pylint: disable=unused-argument
    def on_cell_toggled(
        self, cell: Gtk.CellRenderer, path: str, position: int, message: str
    ) -> None:
        """Handle edits of the FMEA Work View RAMSTKTreeview() toggle cells.

        :param cell: the Gtk.CellRenderer() that was toggled.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was toggled.
        :param position: the column position of the toggled
            Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        :rtype: None
        """
        _new_text = boolean_to_integer(cell.get_active())

        try:
            _keys = list(self.tvwTreeView.position.keys())
            _vals = list(self.tvwTreeView.position.values())
            _col = _keys[_vals.index(position)]
            _key = self.tvwTreeView.korder[_col]

            if not self.tvwTreeView.do_edit_cell(cell, path, _new_text, position):
                pub.sendMessage(
                    message, node_id=[self._record_id, ""], package={_key: _new_text}
                )
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while editing {1} data for record "
                "ID {0} in the view.  One or more keys could not be found in "
                "the attribute dictionary."
            ).format(self._record_id, self._module, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def on_changed_combo(
        self, combo: RAMSTKComboBox, index: int, message: str
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKComboBox() widgets.

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param combo: the RAMSTKComboBox() that called the method.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the attribute from the calling Gtk.Widget().
        :param message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the work stream module's attribute name
            and the new value from the RAMSTKComboBox().  The value {'': -1}
            will be returned when a KeyError or ValueError is raised by this
            method.
        """
        _key: str = ""
        _new_text: int = -1

        combo.handler_block(combo.dic_handler_id["changed"])

        try:
            _key = self._dic_attribute_keys[index][0]

            _new_text = int(combo.get_active())

            # Only if something is selected should we send the message.
            # Otherwise attributes get updated to a value of -1 which isn't
            # correct.  And it sucks trying to figure out why, so leave the
            # conditional unless you have a more elegant (and there prolly
            # is) solution.
            if _new_text > -1:
                pub.sendMessage(
                    message, node_id=[self._record_id, -1], package={_key: _new_text}
                )
        except (KeyError, ValueError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while editing {1} data for record "
                "ID {0} in the view.  Key {3} does not exist in "
                "attribute dictionary."
            ).format(self._record_id, self._module, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

        combo.handler_unblock(combo.dic_handler_id["changed"])

        return {_key: _new_text}

    def on_changed_entry(
        self, entry: RAMSTKEntry, index: int, message: str
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param entry: the RAMSTKEntry() that called the method.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKEntry() or RAMSTKTextView().
        :param message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': ''} will be returned when a KeyError or ValueError is raised
            by this method.
        :rtype: dict
        """
        entry.handler_block(entry.dic_handler_id["changed"])

        _package: Dict[str, Any] = self.__do_read_text(
            entry, self._dic_attribute_keys[index]
        )

        entry.handler_unblock(entry.dic_handler_id["changed"])

        pub.sendMessage(message, node_id=[self._record_id, -1], package=_package)

        return _package

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_changed_textview(
        self, buffer: Gtk.TextBuffer, index: int, message: str, textview: RAMSTKTextView
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKTextView() widgets.

        This method is called by:

            * Gtk.TextBuffer() 'changed' signal

        :param buffer: the Gtk.TextBuffer() calling this method.  This
            parameter is unused in this method.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKTextView().
        :param message: the PyPubSub message to broadcast.
        :param textview: the RAMSTKTextView() calling this method.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKTextView(). The value {'': ''} will be
            returned when a KeyError or ValueError is raised by this method.
        """
        textview.handler_block(textview.dic_handler_id["changed"])

        _package: Dict[str, Any] = self.__do_read_text(
            textview, self._dic_attribute_keys[index]
        )

        textview.handler_unblock(textview.dic_handler_id["changed"])

        pub.sendMessage(message, node_id=[self._record_id, -1], package=_package)

        return _package

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_delete(self, tree: treelib.Tree) -> None:
        """Update the RAMSTKTreeView after deleting a line item.

        :param tree: the treelib Tree() containing the workflow module data.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()
        _model.remove(_row)

        _row = _model.get_iter_first()
        if _row is not None:
            self.tvwTreeView.selection.select_iter(_row)
            self.show_all()

        pub.sendMessage("request_set_cursor_active")

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """Update the panel's Gtk.Widgets() when attributes are changed.

        This method is used to update a RAMSTKPanel() containing a
        Gtk.Fixed() populated with widgets [generally the work view]
        whenever a module view RAMSTKTreeView() is edited.  It is used to keep
        the data displayed in-sync.

        A dict 'package' is sent when a module view RAMSTKTreeView() is
        edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The key in the 'package' is used to find the value in
        _dic_attribute_updater corresponding to the data being changed.
        Position 0 of the _dic_attribute_updater value list is the method
        used to update the widget and position 1 is the name of the signal
        to block during the update.

        :param node_id: the list of IDs of the work stream module item
            being edited.  This unused parameter is part of the PyPubSub
            message data package that this method responds to so it must
            remain in the argument list.
        :param package: a dict containing the attribute name as key and
            the new attribute value as the value.
        :return: None
        """
        [[_key, _value]] = package.items()

        try:
            # pylint: disable=unused-variable
            (_function, _signal, __) = self._dic_attribute_updater.get(  # type: ignore
                _key
            )
            _function(_value, _signal)  # type: ignore
        except TypeError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while updating {1} data for record "
                "ID {0} in the view.  Data for key {3} is the wrong "
                "type."
            ).format(self._record_id, self._module, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def on_insert(self, data: Any) -> None:
        """Add row to module view for newly added work stream element.

        :param data: the data package for the work stream element to add.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        # When inserting a child record, the selected row becomes the parent
        # row.
        if self._record_id == self._parent_id:
            _prow = _row
        # When inserting a sibling record, use the parent of the selected
        # row.
        else:
            _prow = _model.iter_parent(_row)

        self.tvwTreeView.do_insert_row(data, _prow)

        pub.sendMessage("request_set_cursor_active")

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        """Get the attributes for the newly selected row.

        :param selection: the Gtk.TreeSelection() for the new row.
        :return: _attributes; the dict of attributes and value for the item
            in the selected row.  The key is the attribute name, the value is
            the attribute value.  Pulling them from the RAMSTKTreeView()
            ensures uncommitted changes are always selected.
        """
        selection.handler_block(self.tvwTreeView.dic_handler_id["changed"])

        _attributes: Dict[str, Any] = {}

        _model, _row = selection.get_selected()
        if _row is not None:
            for _key in self._dic_attribute_updater:
                _attributes[_key] = _model.get_value(
                    _row, self._lst_col_order[self._dic_attribute_updater[_key][2]]
                )

        selection.handler_unblock(self.tvwTreeView.dic_handler_id["changed"])

        return _attributes

    def on_toggled(
        self, checkbutton: RAMSTKCheckButton, index: int, message: str
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKCheckButton() widgets.

        :param checkbutton: the RAMSTKCheckButton() that was toggled.
        :param index: the position in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKCheckButton().
        :param message: the PyPubSub message to broadcast.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': -1} will be returned when a KeyError is raised by this method.
        """
        _key: str = ""
        _new_text: int = -1

        try:
            _key = self._dic_attribute_keys[index][0]

            _new_text = int(checkbutton.get_active())
            checkbutton.do_update(_new_text, signal="toggled")

            pub.sendMessage(
                message, node_id=[self._record_id, -1, ""], package={_key: _new_text}
            )

        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while updating {1} data for record "
                "ID {0} in the view.  Key {3} does not exist in "
                "attribute dictionary."
            ).format(self._record_id, self._module, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

        return {_key: _new_text}

    def _do_load_row(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Determine which type of row to load and loads the data.

        :param node: the usage profile treelib Node() whose data is to be
            loaded.
        :param row: the parent row for the row to be loaded.
        :return: _new_row; the row that was just added to the usage profile
            treeview.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # The root node will have no data package, so this indicates the need
        # to clear the tree in preparation for the load.
        try:
            _method = self._dic_row_loader[node.tag]
            # noinspection PyArgumentList
            _new_row = _method(node, row)
        except KeyError:
            self.do_clear_tree()

        return _new_row

    # pylint: disable=unused-variable
    def _do_load_treerow(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a row into the RAMSTKTreeView().

        :param node: the treelib Node() with the data to load.
        :param row: the parent row of the row to load.
        :return: _new_row; the row that was just populated with data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None
        _data: List[Any] = []

        try:
            # pylint: disable=unused-variable
            [[__, _entity]] = node.data.items()
            _attributes = _entity.get_attributes()
            _model = self.tvwTreeView.get_model()
            for _col, _attr in self.tvwTreeView.korder.items():
                _pos = self.tvwTreeView.position[_col]
                _data.insert(_pos, _attributes[_attr])

            _new_row = _model.append(row, _data)
        except (AttributeError, TypeError, ValueError) as _error:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = (
                "{3}: An error occurred when loading {4} {0}.  "
                "This might indicate it was missing it's data package, some "
                "of the data in the package was missing, or some of the data "
                "was the wrong type.  Row data was: {1}.  Error was: {2}."
                ""
            ).format(str(node.identifier), _data, _error, _method_name, self._module)
            pub.sendMessage(
                "do_log_warning_msg",
                logger_name="WARNING",
                message=_error_msg,
            )
            _new_row = None

        return _new_row

    def __do_read_text(self, entry: RAMSTKEntry, keys: List[str]) -> Dict[str, Any]:
        """Read the text in a RAMSTKEntry() or Gtk.TextBuffer().

        :param entry: the RAMSTKEntry() or Gtk.TextBuffer() to read.
        :param keys: the list containing the key and data type for the entry to
            be read.
        :return: {_key, _new_text}; a dict containing the attribute key and
            the new value (text) for that key.
        """
        _key: str = ""
        _new_text: Any = ""

        try:
            _key = str(keys[0])

            if str(keys[1]) == "float":
                _new_text = float(entry.do_get_text())
            elif str(keys[1]) == "integer":
                _new_text = int(entry.do_get_text())
            elif str(keys[1]) == "string":
                _new_text = str(entry.do_get_text())

        except (KeyError, ValueError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while reading {1} data for record "
                "ID {0} in the view.  Key {3} does not exist in "
                "attribute dictionary."
            ).format(self._record_id, self._module, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

        return {_key: _new_text}
