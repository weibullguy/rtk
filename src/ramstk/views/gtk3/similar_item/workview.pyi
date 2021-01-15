# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.assistants import EditFunction as EditFunction
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

class MethodPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _method_id: int = ...
    _title: Any = ...
    _tree: Any = ...
    cmbSimilarItemMethod: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def _do_set_tree(self, tree: treelib.Tree) -> None:
        ...

    def __do_load_combobox(self) -> None:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...

    def __on_method_changed(self, combo: RAMSTKComboBox) -> None:
        ...


class SimilarItemPanel(RAMSTKPanel):
    _dic_quality: Dict[int, str] = ...
    _dic_environment: Dict[int, str] = ...
    _dic_attribute_updater: Any = ...
    _dic_hardware_attrs: Any = ...
    _dic_row_loader: Any = ...
    _method_id: int = ...
    _hardware_tree: Any = ...
    _selected_hardware_id: int = ...
    _title: Any = ...
    tree: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_combobox(self) -> None:
        ...

    def do_refresh_functions(self, row: Gtk.TreeIter,
                             function: List[str]) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...

    def _do_load_hardware_attrs(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    _tree_loaded: bool = ...

    def _do_load_tree(self) -> None:
        ...

    def _do_set_columns_editable(self) -> None:
        ...

    def _do_set_tree(self, tree: treelib.Tree) -> None:
        ...

    def _on_method_changed(self, method_id: int) -> None:
        ...

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        ...

    def _on_select_hardware(self, attributes: Dict[str, Any]) -> None:
        ...

    def __do_get_environment(self, environment_id: int) -> str:
        ...

    def __do_get_quality(self, quality_id: int) -> str:
        ...

    def __do_load_similar_item(self,
                               node: Any = ...,
                               row: Gtk.TreeIter = ...) -> Gtk.TreeIter:
        ...

    def __do_set_properties(self) -> None:
        ...


class SimilarItem(RAMSTKWorkView):
    _module: str = ...
    _tablabel: str = ...
    _tabtooltip: str = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlMethod: Any = ...
    _pnlPanel: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    _record_id: Any = ...
    _parent_id: Any = ...

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        ...

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_edit_function(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_rollup(self, __button: Gtk.ToolButton) -> None:
        ...

    def __make_ui(self) -> None:
        ...