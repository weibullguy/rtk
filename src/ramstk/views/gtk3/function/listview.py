# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition List View Module."""

# Third Party Imports
import pandas as pd
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class FunctionHardware(RAMSTKListView):
    """
    Display all the Function-Hardware matrix for the selected Revision.

    The attributes of the Function-Hardware Matrix View are:
    """
    def __init__(self, configuration, logger, module='fnctn_hrdwr') -> None:
        """
        Initialize the List View for the Failure Definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger, module)
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_matrix, 'succeed_load_matrix')

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup("<span weight='bold'>"
                                  + _("Function-Hardware\nMatrix") + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays the Function-Hardware matrix for the selected "
              "revision."))

        super().make_ui(vtype='matrix',
                        icons=['refresh-view'],
                        tooltips=[_("Refresh the matrix view.")],
                        callbacks=[self._do_request_refresh])

    def __set_properties(self) -> None:
        """
        Set properties of the Function::Hardware Matrix View and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_tooltip_text(
            _("Displays the Function-Hardware matrix for the selected "
              "revision."))

    def _do_load_matrix(self, matrix_type: str, matrix: pd.DataFrame) -> None:
        """
        Load the RAMSTKMatrixView() with matrix data.

        :param str matrix_type: the type of matrix to load.
        :return: None
        :rtype: None
        """
        if self._module == matrix_type.capitalize():
            self.matrixview.matrixview.do_load_matrix(matrix)

    @staticmethod
    def _do_request_refresh(__button: Gtk.Button) -> None:
        """
        Refresh the RAMSTKMatrixView().

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_create_matrix')