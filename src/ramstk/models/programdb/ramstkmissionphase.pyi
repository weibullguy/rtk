# Standard Library Imports
from typing import Any

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable

class RAMSTKMissionPhase(RAMSTK_BASE, RAMSTKBaseTable):
    __defaults__: Any = ...
    __tablename__: str = ...
    __table_args__: Any = ...
    revision_id: Any = ...
    mission_id: Any = ...
    phase_id: Any = ...
    description: Any = ...
    name: Any = ...
    phase_start: Any = ...
    phase_end: Any = ...
    revision: relationship = ...
    mission: relationship = ...
    environment: relationship = ...
    is_mission: bool = ...
    is_phase: bool = ...
    is_env: bool = ...

    def get_attributes(self):
        ...
