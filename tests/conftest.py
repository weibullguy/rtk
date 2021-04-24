# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK test suite configuration module."""

# Standard Library Imports
import csv
import gettext
import glob
import os
import platform
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from distutils import dir_util

# Third Party Imports
import psycopg2
import pytest
import toml
import xlwt
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKSiteConfiguration, RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase

_ = gettext.gettext

TEMPDIR = tempfile.gettempdir()

try:
    VIRTUAL_ENV = glob.glob(os.environ["VIRTUAL_ENV"])[0]
except KeyError:
    if platform.system() == "Linux":
        VIRTUAL_ENV = os.getenv("HOME") + "/.local"
    elif platform.system() == "Windows":
        VIRTUAL_ENV = os.getenv("TEMP")
    else:
        print(("The {0:s} system platform is not supported.").format(platform.system()))
        sys.exit(1)

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_DIR = VIRTUAL_ENV + "/share/RAMSTK"
DATA_DIR = CONF_DIR + "/layouts"
ICON_DIR = CONF_DIR + "/icons"
TMP_DIR = VIRTUAL_ENV + "/tmp"
LOG_DIR = TMP_DIR + "/logs"
TEST_PROGRAM_DB_PATH = TMP_DIR + "/TestProgramDB.ramstk"
TEST_COMMON_DB_PATH = TEMPDIR + "/TestCommonDB.ramstk"
TEST_COMMON_DB_URI = "sqlite:///" + TEST_COMMON_DB_PATH

DEBUG_LOG = LOG_DIR + "/RAMSTK_debug.log"
USER_LOG = LOG_DIR + "/RAMSTK_user.log"
IMPORT_LOG = LOG_DIR + "/RAMSTK_import.log"

HEADERS = {
    "Function": [
        "Revision ID",
        "Function ID",
        "Level",
        "Function Code",
        "Function Name",
        "Parent",
        "Remarks",
        "Safety Critical",
        "Type",
    ],
    "Requirement": [
        "Revision ID",
        "Requirement ID",
        "Derived?",
        "Requirement",
        "Figure Number",
        "Owner",
        "Page Number",
        "Parent ID",
        "Priority",
        "Requirement Code",
        "Specification",
        "Requirement Type",
        "Validated?",
        "Validated Date",
    ],
    "Hardware": [
        "Revision ID",
        "Hardware ID",
        "Alt. Part Num.",
        "CAGE Code",
        "Category",
        "Comp. Ref. Des.",
        "Unit Cost",
        "Cost Type",
        "Description",
        "Duty Cycle",
        "Fig. Num.",
        "LCN",
        "Level",
        "Supplier",
        "Mission Time",
        "Name",
        "NSN",
        "Page Num.",
        "Parent ID",
        "Part?",
        "PN",
        "Quantity",
        "Ref. Des.",
        "Remarks",
        "Repairable?",
        "Specification",
        "SubCat",
        "Tagged",
        "Year of Manufacture",
        "App. ID",
        "Area",
        "Capacitance",
        "Configuration",
        "Construction ID",
        "Contact Form",
        "Constact Gauge",
        "Contact Rating ID",
        "Operating Current",
        "Rated Current",
        "Current Ratio",
        "Active Environment",
        "Dormant Environment",
        "Family",
        "Feature Size",
        "Operating Freq.",
        "Insert ID",
        "Insulation ID",
        "Manufacturing ID",
        "Matching",
        "Num. Active Pins",
        "Num. Ckt. Planes",
        "Num. Cycles",
        "Num. Elements",
        "Hand Soldered",
        "Wave Soldered",
        "Operating Life",
        "Overstressed?",
        "Package ID",
        "Operating Power",
        "Rated Power",
        "Power Ratio",
        "Overstress Reason",
        "Resistance",
        "Specification ID",
        "Tech. ID",
        "Active Temp.",
        "Case Temp.",
        "Dormant Temp.",
        "Hot Spot Temp.",
        "Junction Temp.",
        "Knee Temp.",
        "Max. Rated Temp.",
        "Min. Rated Temp.",
        "Temperature Rise",
        "Theta JC",
        "Type",
        "AC Operating Voltage",
        "DC Operating Voltage",
        "ESD Withstand Volts",
        "Rated Voltage",
        "Voltage Ratio",
        "Weight",
        "Years in Prod.",
        "Add. Adj. Factor",
        "Fail. Dist. ID",
        "h(t) Method",
        "h(t) Model",
        "Specified h(t)",
        "h(t) Type",
        "Location",
        "Specified MTBF",
        "Mult. Adj. Factor",
        "Quality",
        "R(t) Goal",
        "R(t) Goal Measure",
        "Scale Parameter",
        "Shape Parameter",
        "Surv. Analysis",
        "Altitude, Operating",
        "Balance ID",
    ],
    "Validation": [
        "Revision ID",
        "Validation ID",
        "Maximum Acceptable",
        "Mean Acceptable",
        "Minimum Acceptable",
        "Acceptable Variance",
        "s-Confidence",
        "Avg. Task Cost",
        "Max. Task Cost",
        "Min. Task Cost",
        "Start Date",
        "Finish Date",
        "Description",
        "Unit of Measure",
        "Task Name",
        "Status",
        "Type",
        "Task Spec.",
        "Average Task Time",
        "Maximum Task Time",
        "Minimum Task Time",
    ],
}

# Row data for the Function import test file.
ROW_DATA = [
    [
        1,
        5,
        1,
        "PRESS-001",
        "Maintain system pressure.",
        0,
        "This is a function that is about system pressure.  This remarks box "
        "also needs to be larger.",
        1,
        0,
    ],
    [
        1,
        6,
        1,
        "FLOW-001",
        "Maintain system flow.",
        0,
        "These are remarks associated with the function FLOW-001.  The "
        "remarks box needs to be bigger.",
        0,
        0,
    ],
    [
        1,
        10,
        0,
        "Gotta do something",
        "Fig. 1",
        2,
        "3.2-1",
        0,
        4,
        "GEN-001",
        "Spec. 12",
        4,
        0,
        "2019-08-18",
    ],
    [
        1,
        10,
        "",
        "",
        0,
        "S1",
        47.28,
        1,
        "System That Was Imported",
        87.0,
        "",
        "",
        1,
        "",
        72.0,
        "Imported System",
        "",
        "",
        0,
        0,
        "",
        1,
        "S1",
        "Remarks in a binary field.",
        1,
        "",
        0,
        0,
        2018,
        0,
        0.0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0.0,
        0.0,
        0.0,
        4,
        1,
        0,
        0.0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0,
        0.0,
        0.0,
        0.0,
        "Overstress Reason",
        0.0,
        0,
        0,
        30.0,
        30.0,
        25.0,
        0.0,
        0.0,
        40.0,
        125.0,
        0.0,
        0.0,
        0.0,
        0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0,
        0,
        0,
        0.0,
        0,
        0.0,
        0.0,
        1.0,
        2,
        0.95,
        0,
        0.0,
        0.0,
        0,
        12000,
        1,
    ],
    [
        1,
        12,
        832.5,
        799.0,
        612.3,
        226.4,
        0.9,
        350.00,
        500.00,
        275.00,
        "2019-08-18",
        "2019-09-01",
        "Validation task that was imported by test suite.",
        0,
        "",
        "",
        0,
        "",
        120.0,
        140.0,
        95.0,
    ],
]


@pytest.fixture(scope="function")
def make_shibboly():
    """Create a read-only directory."""
    if os.path.exists("/tmp/shibboly"):
        shutil.rmtree("/tmp/shibboly")

    os.mkdir("/tmp/shibboly", 0o0444)


@pytest.fixture(scope="session")
def make_config_dir():
    """Create a configuration directory if one doesn't exist.

    This creates a configuration directory in the virtual environment
    base to allow testing certain functions/methods that look for a user
    configuration directory otherwise defaulting to the site-wide
    configuration directory.
    """
    _config_dir = VIRTUAL_ENV + "/share/RAMSTK"
    if not os.path.exists(_config_dir):
        os.mkdir(_config_dir)

    dir_util.copy_tree(os.getcwd() + "/data/icons/", _config_dir + "/icons/")

    dir_util.copy_tree(os.getcwd() + "/data/layouts/", _config_dir + "/layouts/")

    yield _config_dir

    shutil.rmtree(VIRTUAL_ENV + "/share/RAMSTK")


@pytest.fixture(scope="session")
def make_home_config_dir():
    """Create a configuration directory to mimic a user's configuration
    directory."""
    _config_dir = VIRTUAL_ENV + "/tmp/.config/RAMSTK"
    if not os.path.exists(VIRTUAL_ENV + "/tmp/"):
        os.mkdir(VIRTUAL_ENV + "/tmp/")
    os.mkdir(VIRTUAL_ENV + "/tmp/.config")
    os.mkdir(_config_dir)
    os.mkdir(_config_dir + "/layouts")
    os.mkdir(_config_dir + "/icons")
    os.mkdir(_config_dir + "/log")
    os.mkdir(VIRTUAL_ENV + "/tmp/analyses")
    os.mkdir(VIRTUAL_ENV + "/tmp/analyses/ramstk")
    shutil.copyfile(
        "./data/sqlite_program_db.sql", _config_dir + "/sqlite_program_db.sql"
    )
    shutil.copyfile(
        "./data/postgres_program_db.sql", _config_dir + "/postgres_program_db.sql"
    )

    yield _config_dir

    shutil.rmtree(VIRTUAL_ENV + "/tmp/.config")
    shutil.rmtree(VIRTUAL_ENV + "/tmp/analyses")


@pytest.fixture(scope="function")
def test_simple_program_database():
    """Create a simple test database using postgres."""
    # This temporary database has two tables (RAMSTKRevision and
    # RAMSTKSiteInfo) and is used primarily to test the connect, insert,
    # insert_many, delete, and update methods of the database drivers.
    test_simple_db = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": "simple_program_db",
    }

    # Create the simple test database.
    conn = psycopg2.connect(
        host=test_simple_db["host"],
        dbname="postgres",
        user=test_simple_db["user"],
        password=test_simple_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(test_simple_db["database"]))
    )
    cursor.close()
    conn.close()

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_simple_db)

    yield dao

    dao.do_disconnect()
    conn = psycopg2.connect(
        host=test_simple_db["host"],
        dbname="postgres",
        user=test_simple_db["user"],
        password=test_simple_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM "
            "pg_stat_activity WHERE pg_stat_activity.datname = "
            "'simple_program_db';"
        )
    )
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(test_simple_db["database"])
        )
    )
    cursor.close()
    conn.close()


@pytest.fixture(scope="session")
def test_simple_database():
    """Create a simple test database using postgres."""
    # This temporary database has two tables (RAMSTKRevision and
    # RAMSTKSiteInfo) and is used primarily to test the connect, insert,
    # insert_many, delete, and update methods of the database drivers.
    test_simple_db = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": "simple_test_db",
    }

    # Create the simple test database.
    conn = psycopg2.connect(
        host=test_simple_db["host"],
        dbname="postgres",
        user=test_simple_db["user"],
        password=test_simple_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(test_simple_db["database"])
        )
    )
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(test_simple_db["database"]))
    )
    cursor.close()
    conn.close()

    # Populate the test database.
    conn = psycopg2.connect(
        host=test_simple_db["host"],
        dbname=test_simple_db["database"],
        user=test_simple_db["user"],
        password=test_simple_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_session(autocommit=True)

    cursor = conn.cursor()
    cursor.execute(open("./tests/__data/test_simple_db.sql", "r").read())
    cursor.close()
    conn.close()

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_simple_db)

    yield dao

    dao.do_disconnect()


@pytest.fixture(scope="function")
def test_license_file():
    """Create a license key file for testing."""
    _cwd = os.getcwd()
    _license_file = open(_cwd + "/license.key", "w")
    _license_file.write("apowdigfb3rh9214839qu\n")
    _license_file.write("2019-08-07")
    _license_file.close()

    yield _license_file

    os.remove(_cwd + "/license.key")


@pytest.fixture(scope="session")
def test_common_dao():
    """Create a test DAO object for testing against an RAMSTK Common DB."""
    test_common_db = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": "TestCommonDB",
    }

    # Create the test database.
    conn = psycopg2.connect(
        host=test_common_db["host"],
        dbname="postgres",
        user=test_common_db["user"],
        password=test_common_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(test_common_db["database"])
        )
    )
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(test_common_db["database"]))
    )
    cursor.close()
    conn.close()

    # Populate the test database.
    conn = psycopg2.connect(
        host=test_common_db["host"],
        dbname=test_common_db["database"],
        user=test_common_db["user"],
        password=test_common_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_session(autocommit=True)

    cursor = conn.cursor()
    cursor.execute(open("./data/postgres_common_db.sql", "r").read())
    cursor.close()
    conn.close()

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_common_db)

    yield dao

    dao.do_disconnect()

    conn = psycopg2.connect(
        host=test_common_db["host"],
        dbname="postgres",
        user=test_common_db["user"],
        password=test_common_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(test_common_db["database"])
        )
    )
    cursor.close()
    conn.close()


@pytest.fixture(scope="class")
def test_program_dao():
    """Create a test DAO object for testing against an RAMSTK Program DB."""
    # This will create a RAMSTK Program database using the
    # test_program_db.sql file in tests/__data for each group of tests collected in a
    # class.  Group tests in the class in such a way as to produce predictable behavior
    # (e.g., all the tests for select() and select_all()).
    test_program_db = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": "TestProgramDB",
    }

    # Create the test database.
    conn = psycopg2.connect(
        host=test_program_db["host"],
        dbname="postgres",
        user=test_program_db["user"],
        password=test_program_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(test_program_db["database"])
        )
    )
    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(test_program_db["database"])
        )
    )
    cursor.close()
    conn.close()

    # Populate the test database.
    conn = psycopg2.connect(
        host=test_program_db["host"],
        dbname=test_program_db["database"],
        user=test_program_db["user"],
        password=test_program_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.set_session(autocommit=True)

    cursor = conn.cursor()
    cursor.execute(open("./tests/__data/test_program_db.sql", "r").read())
    cursor.close()
    conn.close()

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()
    dao.do_connect(test_program_db)

    yield dao

    dao.do_disconnect()

    conn = psycopg2.connect(
        host=test_program_db["host"],
        dbname="postgres",
        user=test_program_db["user"],
        password=test_program_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(test_program_db["database"])
        )
    )
    cursor.close()
    conn.close()


@pytest.fixture(scope="function")
def test_bald_dao():
    test_program_db = {
        "dialect": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
        "database": "ramstk_program_db2",
    }

    # Use the RAMSTK DAO to connect to the fresh, new test database.
    dao = BaseDatabase()

    yield dao

    conn = psycopg2.connect(
        host=test_program_db["host"],
        dbname="postgres",
        user=test_program_db["user"],
        password=test_program_db["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier("ramstk_program_db2")
        )
    )
    cursor.close()
    conn.close()


@pytest.fixture(scope="session")
def test_toml_site_configuration():
    """Create a toml site configuration file."""
    _site_config = RAMSTKSiteConfiguration()
    _site_config.RAMSTK_SITE_CONF = VIRTUAL_ENV + "/share/RAMSTK/Site.toml"
    _dic_site_configuration = {
        "title": "RAMSTK Site Configuration",
        "backend": {
            "dialect": "sqlite",
            "host": "localhost",
            "port": "3306",
            "database": VIRTUAL_ENV + "/share/RAMSTK/ramstk_common.ramstk",
            "user": "johnny.tester",
            "password": "clear.text.password",
        },
    }

    toml.dump(_dic_site_configuration, open(_site_config.RAMSTK_SITE_CONF, "w"))

    yield _site_config


@pytest.fixture(scope="session")
def test_toml_user_configuration(make_home_config_dir):
    """Create a toml user configuration file."""
    _user_config = RAMSTKUserConfiguration()
    _user_config._INSTALL_PREFIX = VIRTUAL_ENV
    _user_config.RAMSTK_HOME_DIR = VIRTUAL_ENV + "/tmp"
    _user_config.RAMSTK_CONF_DIR = VIRTUAL_ENV + "/tmp/.config/RAMSTK"
    _user_config.RAMSTK_PROG_CONF = _user_config.RAMSTK_CONF_DIR + "/RAMSTK.toml"
    _user_config.RAMSTK_DATA_DIR = _user_config.RAMSTK_CONF_DIR + "/layouts"
    _user_config.RAMSTK_ICON_DIR = _user_config.RAMSTK_CONF_DIR + "/icons"
    _user_config.RAMSTK_LOG_DIR = _user_config.RAMSTK_CONF_DIR + "/logs"
    _user_config.RAMSTK_PROG_DIR = VIRTUAL_ENV + "/tmp/analyses/ramstk"
    _dic_user_configuration = {
        "title": "RAMSTK User Configuration",
        "general": {
            "firstrun": "True",
            "reportsize": "letter",
            "frmultiplier": "1000000.0",
            "calcreltime": "100.0",
            "decimal": "6",
            "modesource": "1",
            "moduletabpos": "top",
            "listtabpos": "bottom",
            "worktabpos": "bottom",
            "loglevel": "INFO",
        },
        "backend": {
            "dialect": "sqlite",
            "host": "localhost",
            "port": "3306",
            "database": "",
            "user": "",
            "password": "",
        },
        "directories": {
            "datadir": _user_config.RAMSTK_DATA_DIR,
            "icondir": _user_config.RAMSTK_ICON_DIR,
            "logdir": _user_config.RAMSTK_LOG_DIR,
            "progdir": _user_config.RAMSTK_PROG_DIR,
        },
        "layouts": {
            "allocation": "allocation.toml",
            "failure_definitions": "failure_definition.toml",
            "fmea": "fmea.toml",
            "function": "function.toml",
            "hardware": "hardware.toml",
            "hazard": "hazops.toml",
            "pof": "pof.toml",
            "requirement": "requirement.toml",
            "revision": "revision.toml",
            "similar_item": "similar_item.toml",
            "stakeholders": "stakeholder.toml",
            "usage_profile": "usage_profile.toml",
            "validation": "validation.toml",
        },
        "colors": {
            "allocationbg": "#FFFFFF",
            "allocationfg": "#000000",
            "failure_definitionbg": "#FFFFFF",
            "failure_definitionfg": "#000000",
            "fmeabg": "#FFFFFF",
            "fmeafg": "#000000",
            "functionbg": "#FFFFFF",
            "functionfg": "#000000",
            "hardwarebg": "#FFFFFF",
            "hardwarefg": "#000000",
            "hazardbg": "#FFFFFF",
            "hazardfg": "#000000",
            "pofbg": "#FFFFFF",
            "poffg": "#000000",
            "requirementbg": "#FFFFFF",
            "requirementfg": "#000000",
            "revisionbg": "#FFFFFF",
            "revisionfg": "#000000",
            "similar_itembg": "#FFFFFF",
            "similar_itemfg": "#000000",
            "stakeholderbg": "#FFFFFF",
            "stakeholderfg": "#000000",
            "validationbg": "#FFFFFF",
            "validationfg": "#000000",
        },
        "stress": {
            "integratedcircuit": [0.8, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            "semiconductor": [1.0, 1.0, 0.7, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            "resistor": [1.0, 1.0, 0.5, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            "capacitor": [1.0, 1.0, 1.0, 1.0, 0.6, 0.9, 10.0, 0.0, 125.0, 125.0],
            "inductor": [0.6, 0.9, 1.0, 1.0, 0.5, 0.9, 15.0, 0.0, 125.0, 125.0],
            "relay": [0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            "switch": [0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            "connection": [0.7, 0.9, 1.0, 1.0, 0.7, 0.9, 25.0, 0.0, 125.0, 125.0],
            "meter": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            "miscellaneous": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
        },
    }

    toml.dump(_dic_user_configuration, open(_user_config.RAMSTK_PROG_CONF, "w"))

    yield _user_config


@pytest.fixture
def test_csv_file_function():
    """Create and populate a *.csv file for testing Function imports."""
    _test_file = TMP_DIR + "/test_inputs_functions.csv"

    with open(_test_file, "w", newline="") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Function"])
        filewriter.writerow(ROW_DATA[0])
        filewriter.writerow(ROW_DATA[1])

    yield _test_file


@pytest.fixture
def test_text_file_function():
    """Create and populate a *.txt file for testing Function imports."""
    _test_file = TMP_DIR + "/test_inputs_functions.txt"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=" ", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Function"])
        filewriter.writerow(ROW_DATA[0])
        filewriter.writerow(ROW_DATA[1])

    yield _test_file


@pytest.fixture
def test_csv_file_requirement():
    """Create and populate a *.csv file for testing Requirement import
    mapping."""
    _test_file = TMP_DIR + "/test_inputs_requirements.csv"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Requirement"])
        filewriter.writerow(ROW_DATA[2])

    yield _test_file


@pytest.fixture
def test_csv_file_hardware():
    """Create and populate a *.csv file for testing Hardware import mapping."""
    _test_file = TMP_DIR + "/test_inputs_hardware.csv"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Hardware"])
        filewriter.writerow(ROW_DATA[3])

    yield _test_file


@pytest.fixture
def test_csv_file_validation():
    """Create and populate a *.csv file for testing Validation import
    mapping."""
    _test_file = TMP_DIR + "/test_inputs_validation.csv"

    with open(_test_file, "w") as _csv_file:
        filewriter = csv.writer(
            _csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        filewriter.writerow(HEADERS["Validation"])
        filewriter.writerow(ROW_DATA[4])

    yield _test_file


@pytest.fixture
def test_excel_file():
    """Create and populate a *.xls file for tests."""
    _test_file = TMP_DIR + "/test_inputs.xls"

    _book = xlwt.Workbook()
    _sheet = _book.add_sheet("Sheet 1", cell_overwrite_ok=True)

    _col_num = 1
    for _header in HEADERS["Function"]:
        _sheet.write(0, _col_num, _header)
        _col_num += 1

    _row_num = 1
    for _row in ROW_DATA[:2]:
        _col_num = 1
        for _data in enumerate(_row):
            _sheet.write(_row_num, _col_num, _data[1])
            _col_num += 1
        _row_num += 1

    _book.save(_test_file)

    yield _test_file


@pytest.fixture
def test_format_file():
    """Create and populate a RAMSTK layout format file."""
    _test_file = TMP_DIR + "/Test.xml"

    _root = ET.Element("root")
    _tree = ET.SubElement(_root, "tree", name="Test")
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 0"
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 1"
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 2"
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 3"

    _layout = ET.ElementTree(_root)
    _layout.write(_test_file)

    yield _test_file


@pytest.fixture(scope="class")
def test_export_dir():
    """Create a directroy for export testing."""
    # This simply creates the base name of the file and directory to create it
    # in.  A test would need to add the appropriate file extension.
    _test_export_dir = TMP_DIR + "/test_exports/"
    if os.path.exists(_test_export_dir):
        shutil.rmtree(_test_export_dir)

    os.makedirs(_test_export_dir)

    yield _test_export_dir
