# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Button.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Button Module."""

# Import the ramstk.Widget base class.
from .Widget import _, gtk  # pylint: disable=E0401


def do_make_buttonbox(self, **kwargs):
    """
    Create the buttonbox for RAMSTK Matrix Views.

    This method creates the base buttonbox used by all RAMSTK Matrix Views.
    Use a buttonbox for an RAMSTK Matrix View if there are only buttons to be
    added.

    :return: _buttonbox
    :rtype: :class:`gtk.ButtonBox`
    """
    _icons = kwargs['icons']
    _tooltips = kwargs['tooltips']
    _callbacks = kwargs['callbacks']
    _orientation = kwargs['orientation']
    _height = kwargs['height']
    _width = kwargs['width']

    if _orientation == 'horizontal':
        _buttonbox = gtk.HButtonBox()
    else:
        _buttonbox = gtk.VButtonBox()

    _buttonbox.set_layout(gtk.BUTTONBOX_START)

    i = 0
    for _icon in _icons:
        _image = gtk.Image()
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(
            self._dic_icons[_icon], _height, _width)
        _image.set_from_pixbuf(_icon)

        _button = gtk.Button()
        _button.set_image(_image)

        _button.props.width_request = _width
        _button.props.height_request = _height

        try:
            _button.set_tooltip_markup(_tooltips[i])
        except IndexError:
            _button.set_tooltip_markup("")

        try:
            _button.connect('clicked', _callbacks[i])
        except IndexError:
            _button.set_sensitive(False)

        _buttonbox.pack_start(_button)

        i += 1

    return _buttonbox


class RAMSTKButton(gtk.Button):
    """This is the RAMSTK Button class."""

    def __init__(self, height=40, width=200, label="", icon=None):
        """
        Create Button widgets.

        :keyword int height: the height of the gtk.Button().
                             Default is 40.
        :keyword int  width: the width of the gtk.Button().
                             Default is 200.
        :keyword str label: the text to display on the gtk.Button().
                            Default is an empty string.
        :keyword str icon: the image to display on the gtk.Button().
        :return: None
        """

        gtk.Button.__init__(self, label=label)

        if width == 0:
            width = 200

        if icon is not None:
            _image = gtk.Image()
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, height, width)
            _image.set_from_pixbuf(_icon)
            self.set_image(_image)

        self.props.width_request = width
        self.props.height_request = height

        self.show_all()


class RAMSTKCheckButton(gtk.CheckButton):
    """
    This is the RAMSTK Check Button class.
    """

    def __init__(self,
                 label="",
                 width=-1,
                 tooltip='RAMSTK WARNING: Missing tooltip.  '
                 'Please register an Enhancement type bug.'):
        """
        Method to create CheckButton widgets.

        :keyword str label: the text to display with the gtk.CheckButton().
                            Default is an empty string.
        :keyword int width: the desired width of the gtk.CheckButton().
                            Default is -1 or a natural request.
        :keyword str tooltip: the tooltip to display when hovering over the
                              CheckButton.
        :return: _checkbutton
        :rtype: :py:class:`gtk.CheckButton`
        """

        gtk.CheckButton.__init__(self, label=label, use_underline=True)

        self.set_tooltip_markup(tooltip)

        self.get_child().set_use_markup(True)
        self.get_child().set_line_wrap(True)
        self.get_child().props.width_request = width


class RAMSTKOptionButton(gtk.RadioButton):
    """
    This is the RAMSTK Option Button class.
    """

    def __init__(self, btngroup=None, btnlabel=_(u"")):
        """
        Method to create OptionButton widgets.

        :keyword str btngroup: the group the gtk.RadioButton() belongs to, if
                               any.  Default is None.
        :keyword str btnlabel: the text to place in the label on the
                               gtk.RadioButton().  Default is an empty string.
        :return: _optbutton
        :rtype: :py:class:`gtk.RadioButton`
        """

        gtk.RadioButton.__init__(self, group=btngroup, label=btnlabel)
