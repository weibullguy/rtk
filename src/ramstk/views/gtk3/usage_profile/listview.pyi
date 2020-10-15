from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf, Gtk as Gtk, _ as _
from ramstk.views.gtk3.widgets import RAMSTKListView as RAMSTKListView, RAMSTKPanel as RAMSTKPanel
from treelib import Tree as Tree
from typing import Any, Dict

class UsageProfilePanel(RAMSTKPanel):
    _dic_attributes: Any = ...
    _dic_element_keys: Any = ...
    _dic_headings: Any = ...
    _title: Any = ...
    def __init__(self) -> None: ...
    def do_set_callbacks(self) -> None: ...
    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None: ...
    def _do_load_environment(self, **kwargs: Dict[str, Any]) -> Gtk.TreeIter: ...
    def _do_load_mission(self, **kwargs: Dict[str, Any]) -> Gtk.TreeIter: ...
    def _do_load_phase(self, **kwargs: Dict[str, Any]) -> Gtk.TreeIter: ...
    def _do_load_tree(self, tree: Tree, row: Gtk.TreeIter=...) -> None: ...
    def _on_module_switch(self, module: str=...) -> None: ...
    _record_id: Any = ...
    _parent_id: Any = ...
    _dic_attribute_keys: Any = ...
    _dic_attribute_updater: Any = ...
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...

class UsageProfile(RAMSTKListView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _lst_callbacks: Any = ...
    _lst_col_order: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None: ...
    def __do_request_delete(self, level: str) -> None: ...
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None: ...