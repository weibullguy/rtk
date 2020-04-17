# Stubs for ramstk.views.gtk3.requirement.workview (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import (RAMSTKButton, RAMSTKCheckButton,
    RAMSTKWorkView)
from typing import Any

class GeneralData(RAMSTKWorkView):
    btnValidateDate: RAMSTKButton = ...
    chkDerived: RAMSTKCheckButton = ...
    chkValidated: RAMSTKCheckButton = ...
    cmbOwner: RAMSTKComboBox = ...
    cmbRequirementType: RAMSTKComboBox = ...
    cmbPriority: RAMSTKComboBox = ...
    txtCode: RAMSTKEntry = ...
    txtFigNum: RAMSTKEntry = ...
    txtName: RAMSTKTextView = ...
    txtPageNum: RAMSTKEntry = ...
    txtSpecification: RAMSTKEntry = ...
    txtValidatedDate: RAMSTKEntry = ...
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module: str = ...) -> None:
        super().__init__(configuration, logger, module)
        ...

class RequirementAnalysis(RAMSTKWorkView):
    tvwClear: Gtk.TreeView = ...
    tvwComplete: Gtk.TreeView = ...
    tvwConsistent: Gtk.TreeView = ...
    tvwVerifiable: Gtk.TreeView = ...
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module: str = ...) -> None:
        super().__init__(configuration, logger, module)
        ...
