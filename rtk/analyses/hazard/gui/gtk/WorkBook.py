#!/usr/bin/env python
"""
############################
Hazard Module Work Book View
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.hazard.gui.gtk.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys
from lxml import etree

# Modules required for the GUI.
import pango
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class WorkView(gtk.HBox):                   # pylint: disable=R0902
    """
    The Work Book view displays all the attributes for the selected
    Hazard Analysis.  The attributes of a Hazard Analysis Work Book view are:
    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Hazard Analysis module.

        :param rtk.analyses.hazard.Hazard controller: the Hazard Analysis data
                                                      controller.
        """

        gtk.HBox.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize public scalar attributes.
        self.dtcHazard = controller

        self.btnCalculateHazard = _widg.make_button(width=35,
                                                    image='calculate')
        self.btnAddHazard = _widg.make_button(width=35, image='add')
        self.btnDeleteHazard = _widg.make_button(width=35, image='remove')
        self.btnSaveHazard = _widg.make_button(width=35, image='save')

        self.tvwHazard = gtk.TreeView()

        self.show_all()

    def create_page(self):
        """
        Creates the page for displaying the hazard analysis for the selected
        Hardware item.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _path = "/root/tree[@name='Risk']/column/usertitle"
        _heading = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path)

        _path = "/root/tree[@name='Risk']/column/datatype"
        _datatype = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path)

        _path = "/root/tree[@name='Risk']/column/widget"
        _widget = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path)

        _path = "/root/tree[@name='Risk']/column/position"
        _position = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path)

        _path = "/root/tree[@name='Risk']/column/editable"
        _editable = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path)

        _path = "/root/tree[@name='Risk']/column/visible"
        _visible = etree.parse(_conf.RTK_FORMAT_FILE[17]).xpath(_path)

        # Create a list of GObject datatypes to pass to the model.
        _types = []
        for i in range(len(_position)):
            _types.append(_datatype[i].text)

        _gobject_types = []
        _gobject_types = [gobject.type_from_name(_types[i])
                          for i in range(len(_types))]

        # Create the gtk.TreeModel() for the hazard analysis worksheet.
        _model = gtk.TreeStore(*_gobject_types)
        self.tvwHazard.set_model(_model)
        self.tvwHazard.set_tooltip_text(_(u"Displays the hazard analysis for "
                                          u"the selected assembly."))
        self.tvwHazard.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        _columns = int(len(_heading))
        for i in range(_columns):
            _column = gtk.TreeViewColumn()
            #self._col_order.append(int(_position_[i].text))

            if _widget[i].text == 'combo':
                _cell = gtk.CellRendererCombo()
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)

                _cellmodel.append([""])
                if i == 3:
                    for j in range(len(_conf.RTK_HAZARDS)):
                        _cellmodel.append([_conf.RTK_HAZARDS[j][0] +
                                           ", " + _conf.RTK_HAZARDS[j][1]])
                elif i == 6 or i == 10 or i == 14 or i == 18:
                    for j in range(len(_conf.RTK_SEVERITY)):
                        _cellmodel.append([_conf.RTK_SEVERITY[j][1]])
                elif i == 7 or i == 11 or i == 15 or i == 19:
                    for j in range(len(_conf.RTK_FAILURE_PROBABILITY)):
                        _cellmodel.append([_conf.RTK_FAILURE_PROBABILITY[j][1]])

                # Prevent users from adding new values.
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.connect('changed', self._on_cell_edit,
                              int(_position[i].text))
            elif _widget[i].text == 'spin':
                _cell = gtk.CellRendererSpin()
                _adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
                _cell.set_property('adjustment', _adjustment)
                _cell.set_property('digits', 2)
            else:
                _cell = gtk.CellRendererText()

            _cell.set_property('editable', int(_editable[i].text))
            if int(_editable[i].text) == 0:
                _cell.set_property('background', 'light gray')
            else:
                _cell.set_property('background', 'white')
                _cell.set_property('foreground', 'black')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.connect('edited', self._on_cell_edit,
                              int(_position[i].text))

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" +
                              _heading[i].text.replace("  ", "\n") + "</span>")
            _label.set_use_markup(True)
            _label.show_all()

            _column.set_widget(_label)

            _column.set_visible(int(_visible[i].text))
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=int(_position[i].text))

            _column.set_cell_data_func(_cell, _widg.format_cell,
                                       (int(_position[i].text),
                                        _datatype[i].text))
            _column.set_resizable(True)
            _column.connect('notify::width', _widg.resize_wrap, _cell)

            if i > 0:
                _column.set_reorderable(True)

            self.tvwHazard.append_column(_column)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.pack_start(_bbox, False, True)

        _vbox = gtk.VBox()

        self.pack_end(_vbox, True, True)

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwHazard)

        _frame = _widg.make_frame(label=_(u"Hazards Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddHazard, False, False)
        _bbox.pack_start(self.btnDeleteHazard, False, False)
        _bbox.pack_start(self.btnCalculateHazard, False, False)
        _bbox.pack_start(self.btnSaveHazard, False, False)
        #_bbox.pack_start(self.btnTrickledown, False, False)

        self.btnCalculateHazard.set_tooltip_text(_(u"Calculates the hazard "
                                                   u"risk index (HRI) and "
                                                   u"user-defined "
                                                   u"calculations for the "
                                                   u"selected hazard "
                                                   u"analysis."))
        self.btnSaveHazard.set_tooltip_text(_(u"Saves the selected hazard "
                                              u"analysis."))
        #self.btnTrickledown.set_tooltip_text(_(u"Sets the reliability, hazard "
        #                                       u"rate and MTBF goal of the "
        #                                       u"immediately subordinate "
        #                                       u"hardware items to the "
        #                                       u"values calculated by the "
        #                                       u"alloction."))

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAddHazard.connect('clicked',
                                      self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnDeleteHazard.connect('clicked',
                                         self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnCalculateHazard.connect('clicked',
                                            self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnSaveHazard.connect('clicked',
                                       self._on_button_clicked, 3))
        #self._lst_handler_id.append(
        #    self.btnTrickledown.connect('clicked',
        #                                self._on_button_clicked, 4))

        return False

    def load_page(self, controller, hardware_id, path=None):
        """
        Loads the Hazard Analysis gtk.TreeModel() with hazard information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = self.tvwHazard.get_model()
        _model.clear()

        # Find all the hazards for the selected Hardware Item.
        _hazards = [self.dtcHazard.dicHazard[_a]
                    for _a in self.dtcHazard.dicHazard.keys()
                    if self.dtcHazard.dicHazard[_a].hardware_id == hardware_id]

        parent_row = None
        for _hazard in _hazards:
            _hardware = controller.dicHardware[hardware_id]
            _hazard_rate = _hardware.hazard_rate_logistics
            _name = _hardware.name
            _ass_sev = _conf.RTK_SEVERITY[_hazard.assembly_severity - 1][1]
            _ass_prob = _conf.RTK_FAILURE_PROBABILITY[_hazard.assembly_probability - 1][1]
            _ass_sev_f = _conf.RTK_SEVERITY[_hazard.assembly_severity_f - 1][1]
            _ass_prob_f = _conf.RTK_FAILURE_PROBABILITY[_hazard.assembly_probability_f - 1][1]
            _sys_sev = _conf.RTK_SEVERITY[_hazard.system_severity - 1][1]
            _sys_prob = _conf.RTK_FAILURE_PROBABILITY[_hazard.system_probability - 1][1]
            _sys_sev_f = _conf.RTK_SEVERITY[_hazard.system_severity_f - 1][1]
            _sys_prob_f = _conf.RTK_FAILURE_PROBABILITY[_hazard.system_probability_f - 1][1]
            _data = [_hazard.hazard_id, _name, _hazard_rate,
                     _hazard.potential_hazard, _hazard.potential_cause,
                     _hazard.assembly_effect, _ass_sev, _ass_prob,
                     _hazard.assembly_hri, _hazard.assembly_mitigation,
                     _ass_sev_f, _ass_prob_f, _hazard.assembly_hri_f,
                     _hazard.system_effect, _sys_sev, _sys_prob,
                     _hazard.system_hri, _hazard.system_mitigation,
                     _sys_sev_f, _sys_prob_f, _hazard.system_hri_f,
                     _hazard.remarks, _hazard.function_1, _hazard.function_2,
                     _hazard.function_3, _hazard.function_4,
                     _hazard.function_5, _hazard.result_1, _hazard.result_2,
                     _hazard.result_3, _hazard.result_4, _hazard.result_5,
                     _hazard.user_blob_1, _hazard.user_blob_2,
                     _hazard.user_blob_3, _hazard.user_float_1,
                     _hazard.user_float_2, _hazard.user_float_3,
                     _hazard.user_int_1, _hazard.user_int_2,
                     _hazard.user_int_3]
            _piter = _model.append(parent_row, _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwHazard.get_column(0)
        self.tvwHazard.set_cursor(path, None, False)
        self.tvwHazard.row_activated(path, _column)
        self.tvwHazard.expand_all()

        return False

    def _on_button_clicked(self, __button, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:                      # Add hazard to analysis.
            # Add the hazard.
            (_results,
             _error_code, _last_id) = self.dtcHazard.add_hazard(
                 self._hardware_model.hardware_id)

            # Get the Hazard gtk.TreeModel().
            _model = self.tvwHazard.get_model()

            # Get the attributes of the newly added hazard.
            _attributes = self.dtcHazard.dicHazard[
                (self._hardware_model.hardware_id, _last_id)].get_attributes()

            # Get some hardware information.
            _hazard_rate = self._hardware_model.hazard_rate_logistics
            _name = self._hardware_model.name

            # Add the new hazard to the gtk.TreeView().
            _data = [_last_id, _name, _hazard_rate, _attributes[2],
                     _attributes[3], _attributes[4], '', '', _attributes[7],
                     _attributes[8], '', '', _attributes[11], _attributes[12],
                     '', '', _attributes[15], _attributes[16], '', '',
                     _attributes[19], _attributes[20], _attributes[21],
                     _attributes[22], _attributes[23], _attributes[24],
                     _attributes[25], _attributes[26], _attributes[27],
                     _attributes[28], _attributes[29], _attributes[30],
                     _attributes[31], _attributes[32], _attributes[33],
                     _attributes[34], _attributes[35], _attributes[36],
                     _attributes[37], _attributes[38], _attributes[39]]
            _model.append(None, _data)
        elif index == 1:                    # Delete selected hazard from analysis.
            (_model, _row) = self.tvwHazard.get_selection().get_selected()
            _hazard_id = _model.get_value(_row, 0)
            (_results,
             _error_code) = self.dtcHazard.delete_hazard(
                 self._hardware_model.hardware_id, _hazard_id)
            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self._load_hazard_analysis_page(
                    self._hardware_model.hardware_id, _path)
        elif index == 2:                    # Calculate hazard analysis.
            _hardware_id = self._hardware_model.hardware_id
            _model = self.tvwHazard.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                _hazard_id = _model.get_value(_row, 0)
                self.dtcHazard.calculate_hazard(_hardware_id, _hazard_id)
                _hazard = self.dtcHazard.dicHazard[(_hardware_id, _hazard_id)]
                _model.set_value(_row, 8, _hazard.assembly_hri)
                _model.set_value(_row, 12, _hazard.assembly_hri_f)
                _model.set_value(_row, 16, _hazard.system_hri)
                _model.set_value(_row, 20, _hazard.system_hri_f)
                _row = _model.iter_next(_row)
        elif index == 3:                    # Save hazard analysis.
            self.dtcHazard.save_all_hazards()

        return False

    def _on_cell_edit(self, cell, path, new_text, index):
        """
        Responds to edited signals from the Hazard gtk.TreeView().

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that called this
                                      method.
        :param str path: the path of the selected gtk.TreeIter().
        :param str new_text: the new text in the gtk.CellRenderer() that called
                             this method.
        :param int index: the position of the gtk.CellRenderer() in the
                          gtk.TreeModel().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwHazard.get_model()

        try:
            _cellmodel = cell.get_property('model')
            new_text = _cellmodel.get(new_text, 0)[0]
            _hardware_id = self._hardware_model.hardware_id
            _hazard_id = _model[path][0]
            _hazard = self.dtcHazard.dicHazard[(_hardware_id, _hazard_id)]
            if index in [6, 10, 14, 18]:
                try:
                    _score = [_s for _s in _conf.RTK_SEVERITY
                              if _s[1] == new_text][0][4]
                except IndexError:
                    _score = 0
            elif index in [7, 11, 15, 19]:
                try:
                    _score = [_s for _s in _conf.RTK_FAILURE_PROBABILITY
                              if _s[1] == new_text][0][2]
                except IndexError:
                    _score = 0

            if index == 3:
                _hazard.potential_hazard = new_text
            elif index == 6:
                _hazard.assembly_severity = _score
            elif index == 7:
                _hazard.assembly_probability = _score
            elif index == 10:
                _hazard.assembly_severity_f = _score
            elif index == 11:
                _hazard.assembly_probability_f = _score
            elif index == 14:
                _hazard.system_severity = _score
            elif index == 15:
                _hazard.system_probability = _score
            elif index == 18:
                _hazard.system_severity_f = _score
            elif index == 19:
                _hazard.system_probability_f = _score

        except TypeError:
            _convert = gobject.type_name(_model.get_column_type(index))

            if new_text is None:
                _model[path][index] = not cell.get_active()
            elif _convert == 'gchararray':
                _model[path][index] = str(new_text)
            elif _convert == 'gint':
                _model[path][index] = int(new_text)
            elif _convert == 'gfloat':
                _model[path][index] = float(new_text)

        return False
