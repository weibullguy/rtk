# pylint: disable=unused-import
# -*- coding: utf-8 -*-
#
#       ramstk.db.__init__.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK database package."""

# Third Party Imports
from sqlalchemy.ext.declarative import declarative_base

# RAMSTK Local Imports
from .base import BaseDatabase

RAMSTK_BASE = declarative_base()