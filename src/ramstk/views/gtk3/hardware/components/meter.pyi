# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel as RAMSTKAssessmentInputPanel
from .panels import RAMSTKAssessmentResultPanel as RAMSTKAssessmentResultPanel

class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    _dic_quality: Dict[int, List[List[str]]] = ...
    _dic_types: Dict[int, List[List[str]]] = ...
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _lst_tooltips: Any = ...
    cmbApplication: Any = ...
    cmbType: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def _do_set_sensitive(self) -> None:
        ...

    def __set_callbacks(self) -> None:
        ...


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    _dic_part_stress: Any = ...
    _lst_labels: Any = ...
    _lst_tooltips: Any = ...
    txtPiA: Any = ...
    txtPiF: Any = ...
    txtPiT: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def _do_set_sensitive(self) -> None:
        ...

    def __do_set_part_stress_sensitive(self) -> None:
        ...
