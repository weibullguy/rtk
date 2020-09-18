from ramstk.configuration import RAMSTKSiteConfiguration as RAMSTKSiteConfiguration, RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import GObject as GObject, Gdk as Gdk, GdkPixbuf as GdkPixbuf, Gtk as Gtk
from ramstk.views.gtk3.assistants import CreateProject as CreateProject, EditOptions as EditOptions, EditPreferences as EditPreferences, ExportProject as ExportProject, ImportProject as ImportProject, OpenProject as OpenProject
from ramstk.views.gtk3.books import RAMSTKListBook as RAMSTKListBook, RAMSTKModuleBook as RAMSTKModuleBook, RAMSTKWorkBook as RAMSTKWorkBook
from typing import Any, TypeVar

Tconfiguration = TypeVar('Tconfiguration', RAMSTKUserConfiguration, RAMSTKSiteConfiguration)

def destroy(__widget: Gtk.Widget, __event: Gdk.Event=...) -> None: ...

class RAMSTKDesktop(Gtk.Window):
    RAMSTK_USER_CONFIGURATION: Any = ...
    menubar: Any = ...
    progressbar: Any = ...
    statusbar: Any = ...
    toolbar: Any = ...
    icoStatus: Any = ...
    nbkListBook: Any = ...
    nbkModuleBook: Any = ...
    nbkWorkBook: Any = ...
    def __init__(self, configuration: Tconfiguration, logger: RAMSTKLogManager) -> None: ...