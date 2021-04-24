# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKMissionPhase.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMissionPhase Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKMissionPhase(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_mission_phase in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mission.
    This table shares a One-to-Many relationship with
    ramstk_environment.
    """

    __defaults__ = {
        'description': '',
        'name': '',
        'phase_start': 0.0,
        'phase_end': 0.0
    }
    __tablename__ = 'ramstk_mission_phase'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    mission_id = Column(
        'fld_mission_id',
        Integer,
        ForeignKey('ramstk_mission.fld_mission_id'),
        nullable=False,
    )
    phase_id = Column(
        'fld_phase_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column('fld_description',
                         String,
                         default=__defaults__['description'])
    name = Column('fld_name', String(256), default=__defaults__['name'])
    phase_start = Column('fld_phase_start',
                         Float,
                         default=__defaults__['phase_start'])
    phase_end = Column('fld_phase_end',
                       Float,
                       default=__defaults__['phase_end'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision: relationship = relationship(
        'RAMSTKRevision',
        back_populates='phase',
    )
    mission: relationship = relationship(
        'RAMSTKMission',
        back_populates='phase',
    )
    environment: relationship = relationship(
        'RAMSTKEnvironment',
        back_populates='phase',
        cascade='delete',
    )

    is_mission = False
    is_phase = True
    is_env = False

    def get_attributes(self):
        """Retrieve current values of the Mission Phase data model attributes.

        :return: value of instance attributes
        :rtype: tuple
        """
        _values = {
            'mission_id': self.mission_id,
            'phase_id': self.phase_id,
            'description': self.description,
            'name': self.name,
            'phase_start': self.phase_start,
            'phase_end': self.phase_end,
        }

        return _values
