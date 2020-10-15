from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog, RAMSTKModuleView as RAMSTKModuleView, RAMSTKPanel as RAMSTKPanel

class RequirementPanel(RAMSTKPanel):
    def __init__(self) -> None: ...
    def do_set_callbacks(self) -> None: ...

class ModuleView(RAMSTKModuleView):
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None: ...