# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKOpStress as RAMSTKOpStress

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _root: int = ...
    _pkey: Any = ...
    _hardware_id: int = ...
    _mode_id: int = ...
    _mechanism_id: int = ...
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_get_tree(self) -> None: ...
    _revision_id: Any = ...
    _parent_id: Any = ...
    last_id: Any = ...
    def do_select_all(self, attributes: Dict[str, Any]) -> None: ...
    def _do_delete(self, node_id: int) -> None: ...
    def _do_insert_opstress(self, parent_id: int) -> None: ...
