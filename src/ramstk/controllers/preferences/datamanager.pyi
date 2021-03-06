# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKProgramInfo as RAMSTKProgramInfo

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _root: int = ...
    _pkey: Any = ...

    def __init__(self, **kwargs: Any) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    dao: Any = ...

    def _do_select_all(self, dao: BaseDatabase) -> None:
        ...

    def do_update(self, node_id: str) -> None:
        ...
