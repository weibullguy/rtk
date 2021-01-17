# Standard Library Imports
import gettext
from typing import Any

# RAMSTK Package Imports
from ramstk.utilities import dir_exists as dir_exists
from ramstk.utilities import file_exists as file_exists
from ramstk.utilities import get_install_prefix as get_install_prefix

_ = gettext.gettext
RAMSTK_ACTIVE_ENVIRONMENTS: Any
RAMSTK_DORMANT_ENVIRONMENTS: Any
RAMSTK_ALLOCATION_MODELS: Any
RAMSTK_HR_TYPES: Any
RAMSTK_HR_MODELS: Any
RAMSTK_HR_DISTRIBUTIONS: Any
RAMSTK_CONTROL_TYPES: Any
RAMSTK_COST_TYPES: Any
RAMSTK_MTTR_TYPES: Any
RAMSTK_CRITICALITY: Any
RAMSTK_FAILURE_PROBABILITY: Any
RAMSTK_SW_DEV_ENVIRONMENTS: Any
RAMSTK_SW_DEV_PHASES: Any
RAMSTK_SW_LEVELS: Any
RAMSTK_SW_APPLICATION: Any
RAMSTK_SW_TEST_METHODS: Any
RAMSTK_LIFECYCLE: Any
RAMSTK_S_DIST: Any


class RAMSTKSiteConfiguration:
    _INSTALL_PREFIX: Any = ...
    RAMSTK_COM_INFO: Any = ...
    RAMSTK_COM_BACKEND: str = ...
    RAMSTK_SITE_DIR: Any = ...
    RAMSTK_SITE_CONF: Any = ...

    def __init__(self) -> None:
        ...

    def do_create_site_configuration(self) -> None:
        ...

    def get_site_configuration(self) -> None:
        ...

    def set_site_configuration(self) -> None:
        ...

    def set_site_directories(self) -> None:
        ...


class RAMSTKUserConfiguration:
    _lst_colors: Any = ...
    _lst_format_files: Any = ...
    _lst_categories: Any = ...
    _INSTALL_PREFIX: Any = ...
    RAMSTK_ACTION_CATEGORY: Any = ...
    RAMSTK_ACTION_STATUS: Any = ...
    RAMSTK_AFFINITY_GROUPS: Any = ...
    RAMSTK_CATEGORIES: Any = ...
    RAMSTK_DAMAGE_MODELS: Any = ...
    RAMSTK_DETECTION_METHODS: Any = ...
    RAMSTK_FAILURE_MODES: Any = ...
    RAMSTK_HAZARDS: Any = ...
    RAMSTK_INCIDENT_CATEGORY: Any = ...
    RAMSTK_INCIDENT_STATUS: Any = ...
    RAMSTK_INCIDENT_TYPE: Any = ...
    RAMSTK_LOAD_HISTORY: Any = ...
    RAMSTK_MANUFACTURERS: Any = ...
    RAMSTK_MEASURABLE_PARAMETERS: Any = ...
    RAMSTK_MEASUREMENT_UNITS: Any = ...
    RAMSTK_MODULES: Any = ...
    RAMSTK_REQUIREMENT_TYPE: Any = ...
    RAMSTK_RPN_DETECTION: Any = ...
    RAMSTK_RPN_OCCURRENCE: Any = ...
    RAMSTK_RPN_SEVERITY: Any = ...
    RAMSTK_SEVERITY: Any = ...
    RAMSTK_STAKEHOLDERS: Any = ...
    RAMSTK_STRESS_LIMITS: Any = ...
    RAMSTK_SUBCATEGORIES: Any = ...
    RAMSTK_USERS: Any = ...
    RAMSTK_VALIDATION_TYPE: Any = ...
    RAMSTK_COLORS: Any = ...
    RAMSTK_FORMAT_FILE: Any = ...
    RAMSTK_PAGE_NUMBER: Any = ...
    RAMSTK_PROG_INFO: Any = ...
    RAMSTK_TABPOS: Any = ...
    RAMSTK_WORKGROUPS: Any = ...
    RAMSTK_FAILURE_PROBABILITY: Any = ...
    RAMSTK_RISK_POINTS: Any = ...
    RAMSTK_MODE: str = ...
    RAMSTK_MODE_SOURCE: int = ...
    RAMSTK_BACKEND: str = ...
    RAMSTK_REPORT_SIZE: str = ...
    RAMSTK_HR_MULTIPLIER: float = ...
    RAMSTK_DEC_PLACES: int = ...
    RAMSTK_MTIME: float = ...
    RAMSTK_GUI_LAYOUT: str = ...
    RAMSTK_METHOD: str = ...
    RAMSTK_LOCALE: str = ...
    RAMSTK_LOGLEVEL: str = ...
    RAMSTK_OS: str = ...
    RAMSTK_CONF_DIR: Any = ...
    RAMSTK_HOME_DIR: Any = ...
    RAMSTK_DATA_DIR: Any = ...
    RAMSTK_ICON_DIR: Any = ...
    RAMSTK_LOG_DIR: Any = ...
    RAMSTK_PROG_DIR: Any = ...
    RAMSTK_PROG_CONF: Any = ...
    RAMSTK_USER_LOG: Any = ...
    RAMSTK_IMPORT_LOG: Any = ...
    loaded: bool = ...

    def __init__(self) -> None:
        ...

    def _do_make_configuration_dir(self) -> None:
        ...

    def _do_make_data_dir(self) -> None:
        ...

    def _do_make_icon_dir(self) -> None:
        ...

    def _do_make_log_dir(self) -> None:
        ...

    def _do_make_program_dir(self) -> None:
        ...

    def do_create_user_configuration(self) -> None:
        ...

    def get_user_configuration(self) -> None:
        ...

    def set_user_configuration(self) -> None:
        ...

    def set_user_directories(self) -> None:
        ...
