# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.frame.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 frame Module."""

# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject, Gtk

# RAMSTK Local Imports
from .label import RAMSTKLabel


class RAMSTKFrame(Gtk.Frame):
    """This is the RAMSTK Frame class."""

    def __init__(self) -> None:
        """
        Initialize an instance of the RAMSTK Frame.

        :keyword str label: the text to display in the RAMSTK Frame label.
            Default is an empty string.
        """
        GObject.GObject.__init__(self)

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set the RAMSTKFrame properties."""
        try:
            _title = kwargs['title']
        except KeyError:
            _title = ""
        try:
            _shadow = kwargs['shadow']
        except KeyError:
            _shadow = Gtk.ShadowType.ETCHED_OUT

        _label = RAMSTKLabel(_title)
        _label.show_all()
        self.set_label_widget(_label)

        self.set_shadow_type(_shadow)