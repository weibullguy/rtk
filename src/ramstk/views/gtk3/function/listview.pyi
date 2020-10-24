from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKListView as RAMSTKListView
from typing import Any

class FunctionHardware(RAMSTKListView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _view_type: str = ...
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None: ...
