# Stubs for ramstk.views.gtk3.desktop (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk
from typing import Any, List

def destroy(__widget: Gtk.Widget, __event: Gdk.Event=...) -> None: ...

class RAMSTKDesktop(Gtk.Window):
    RAMSTK_USER_CONFIGURATION: Any = ...
    _lst_handler_id: List[int] = ...
    _n_screens: int = ...
    _height: float = ...
    _width: float = ...
    menubar: Gtk.MenuBar = ...
    progressbar: Gtk.ProgressBar = ...
    statusbar: Gtk.Statusbar = ...
    toolbar: Gtk.Toolbar = ...
    icoStatus: Gtk.StatusIcon = ...
    nbkListBook: Any = ...
    nbkModuleBook: Any = ...
    nbkWorkBook: Any = ...
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...
    def __make_menu(self) -> None: ...
    def __make_toolbar(self) -> None: ...
    def __make_ui(self) -> None: ...
    def __set_callbacks(self) -> None: ...
    def __set_properties(self) -> None: ...
    def _do_request_close_project(self) -> None: ...
    def _on_request_open(self) -> None: ...
    def _do_request_save_project(self) -> None: ...
    def _do_set_status(self) -> None: ...

    def add(self, _vbox):
        pass

    def show_all(self):
        pass

    def _do_set_status_icon(self):
        pass

    def connect(self, param, destroy):
        pass

    def __make_menu_edit(self):
        pass

    def __make_menu_tools(self):
        pass
