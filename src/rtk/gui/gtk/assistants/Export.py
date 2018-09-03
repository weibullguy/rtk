#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.Export.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007, 2018 Doyle "weibullguy" Rowland
"""Export Assistant Module."""

import os

# Export other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk import RTKMessageDialog
from rtk.gui.gtk.rtk.Widget import _, gobject, gtk, set_cursor

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007, 2018 Doyle "weibullguy" Rowland'


class RAMSTKExport(rtk.RTKFileChooser):
    """Assistant to walk user through the process of exporting records."""

    def __init__(self, controller, module, tree):
        """
        Initialize an instance of the Export Assistant.

        :param __widget: the gtk.Widget() that called this class.
        :type __widget: :class:`gtk.Widget`
        :param controller: the RAMSTK master data controller.
        :type controller: :class:`rtk.RTK.RTK`
        :param str module: the RAMSTK module to export.
        """
        rtk.RTKFileChooser.__init__(self, _(u"RAMSTK Export"),
                                    controller.RTK_CONFIGURATION.RTK_PROG_DIR)

        # Initialize private dict variables.

        # Initialize private list variables.

        # Initialize private scalar variables.
        self._mdcRTK = controller
        self._dtc_data_controller = self._mdcRTK.dic_controllers['exports']
        self._module = module
        self._tree = tree

        # Initialize public dict variables.

        # Initialize public list variables.

        # Initialize public scalar variables.

        self._do_select_file()

    def _do_quit(self):
        """
        Quit the RAMSTK Export Assistant.

        :return: None
        :rtype: None
        """
        self.destroy()

        return None

    def _do_request_export(self, filetype, filename):
        """
        Request the data controller insert new records.

        :param str filetype: the type of file to export data.  Current options
                             are:

                             - Text
                             - Excel

        :param str filename: the absolute path to the file to export data.
        :return: None
        :rtype: None
        """
        set_cursor(self._mdcRTK, gtk.gdk.WATCH)

        self._dtc_data_controller.request_do_load_output(
            self._module, self._tree)
        self._dtc_data_controller.request_do_export(filetype, filename)

        set_cursor(self._mdcRTK, gtk.gdk.LEFT_PTR)

        return None

    def _do_select_file(self):
        """
        Select the input file to export data to.

        :return: None
        :rtype: None
        """
        _cansave = False
        (_filename, _extension) = self.do_run()

        if _filename is not None:
            if _extension == '.csv':
                _filetype = 'csv'
            elif _extension == '.txt':
                _filetype = 'text'
            elif _extension in ['.xls', '.xlsm', '.xlsx']:
                _filetype = 'excel'

            if os.path.exists(_filename) == True:
                _prompt = _(u"File {0:s} already exists.  "
                            u"Overwrite?").format(_filename)
                _icon = self._mdcRTK.RTK_CONFIGURATION.RTK_ICON_DIR + \
                        '/32x32/warning.png'
                _dialog = RTKMessageDialog(_prompt, _icon, 'question')
                _response = _dialog.do_run()
                if _response == gtk.RESPONSE_YES:
                    _dialog.destroy()
                    _cansave = True
                else:
                    _dialog.destroy()
            else:
                _cansave = True

            if _cansave:
                self._do_request_export(_filetype, _filename)
            else:
                self._do_select_file()

        self._do_quit()

        return None