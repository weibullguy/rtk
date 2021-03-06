# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import pandas as pd
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKDateSelect as RAMSTKDateSelect
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFrame as RAMSTKFrame
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKPlot as RAMSTKPlot
from ramstk.views.gtk3.widgets import RAMSTKSpinButton as RAMSTKSpinButton
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS as ATTRIBUTE_KEYS

class TaskDescriptionPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _dic_task_types: Any = ...
    _dic_units: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    fmt: str = ...
    btnEndDate: Any = ...
    btnStartDate: Any = ...
    cmbTaskType: Any = ...
    cmbMeasurementUnit: Any = ...
    spnStatus: Any = ...
    txtTaskID: Any = ...
    txtCode: Any = ...
    txtMaxAcceptable: Any = ...
    txtMeanAcceptable: Any = ...
    txtMinAcceptable: Any = ...
    txtVarAcceptable: Any = ...
    txtSpecification: Any = ...
    txtTask: Any = ...
    txtEndDate: Any = ...
    txtStartDate: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_measurement_units(
            self, measurement_unit: Dict[int, Tuple[str, str]]) -> None:
        ...

    def do_load_validation_types(
            self, validation_type: Dict[int, Tuple[str, str]]) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def _do_make_task_code(self, combo: RAMSTKComboBox) -> None:
        ...

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class TaskEffortPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    fmt: str = ...
    txtMinTime: Any = ...
    txtExpTime: Any = ...
    txtMaxTime: Any = ...
    txtMinCost: Any = ...
    txtExpCost: Any = ...
    txtMaxCost: Any = ...
    txtMeanTimeLL: Any = ...
    txtMeanTime: Any = ...
    txtMeanTimeUL: Any = ...
    txtMeanCostLL: Any = ...
    txtMeanCost: Any = ...
    txtMeanCostUL: Any = ...
    _dic_switch: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    def _do_load_code(self, task_code: int) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def _do_make_task_code(self, task_type: str) -> str:
        ...

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        ...

    def _on_calculate_task(self, tree: treelib.Tree) -> None:
        ...

    def __do_adjust_widgets(self) -> None:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class ProgramEffortPanel(RAMSTKPanel):
    _lst_labels: Any = ...
    _title: Any = ...
    fmt: str = ...
    txtProjectTimeLL: Any = ...
    txtProjectTime: Any = ...
    txtProjectTimeUL: Any = ...
    txtProjectCostLL: Any = ...
    txtProjectCost: Any = ...
    txtProjectCostUL: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def __do_adjust_widgets(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class BurndownCurvePanel(RAMSTKPanel):
    _title: Any = ...

    def __init__(self) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    def _do_load_panel(self, attributes: Dict[str, pd.DataFrame]) -> None:
        ...

    def __do_load_assessment_milestones(self, assessed: pd.DataFrame,
                                        y_max: float) -> None:
        ...

    def __do_load_plan(self, plan: pd.DataFrame) -> None:
        ...


class GeneralData(RAMSTKWorkView):
    _module: str = ...
    _tablabel: str = ...
    _tabtooltip: str = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlTaskDescription: Any = ...
    _pnlTaskEffort: Any = ...
    _pnlProgramEffort: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        ...

    _record_id: Any = ...

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        ...

    def __make_ui(self) -> None:
        ...


class BurndownCurve(RAMSTKWorkView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlPanel: Any = ...
    _title: Any = ...
    pltPlot: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_set_cursor_active(self, attributes: Dict[str, Any]) -> None:
        ...

    _record_id: Any = ...

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        ...

    def __make_ui(self) -> None:
        ...
