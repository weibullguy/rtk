# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKRevision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2017 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKRevision Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKRevision(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_revision table in the RAMSTK Program database.

    This table shares a:
        * One-to-Many relationship with ramstk_environment.
        * One-to-Many relationship with ramstk_mission.
        * One-to-Many relationship with ramstk_failure_definition.
        * One-to-Many relationship with ramstk_function.
        * One-to-Many relationship with ramstk_requirement.
        * One-to-Many relationship with ramstk_hardware.
        * One-to-Many relationship with ramstk_software.
        * One-to-Many relationship with ramstk_validation.
        * One-to-Many relationship with ramstk_incident.
        * One-to-Many relationship with ramstk_survival.
        * One-to-Many relationship with ramstk_matrix.
        * One-to-Many relationship with ramstk_hazard_analysis.
        * One-to-Many relationship with ramstk_program_status.
    """

    __defaults__ = {
        'availability_logistics': 1.0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'cost_failure': 0.0,
        'cost_hour': 0.0,
        'hazard_rate_active': 0.0,
        'hazard_rate_dormant': 0.0,
        'hazard_rate_logistics': 0.0,
        'hazard_rate_mission': 0.0,
        'hazard_rate_software': 0.0,
        'mmt': 0.0,
        'mcmt': 0.0,
        'mpmt': 0.0,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.0,
        'name': '',
        'reliability_logistics': 1.0,
        'reliability_mission': 1.0,
        'remarks': '',
        'total_part_count': 1,
        'revision_code': '',
        'program_time': 0.0,
        'program_time_sd': 0.0,
        'program_cost': 0.0,
        'program_cost_sd': 0.0
    }
    __tablename__ = 'ramstk_revision'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    availability_logistics = Column(
        'fld_availability_logistics',
        Float,
        nullable=False,
        default=__defaults__['availability_logistics'])
    availability_mission = Column('fld_availability_mission',
                                  Float,
                                  nullable=False,
                                  default=__defaults__['availability_mission'])
    cost = Column('fld_cost',
                  Float,
                  nullable=False,
                  default=__defaults__['cost'])
    cost_failure = Column('fld_cost_failure',
                          Float,
                          nullable=False,
                          default=__defaults__['cost_failure'])
    cost_hour = Column('fld_cost_hour',
                       Float,
                       nullable=False,
                       default=__defaults__['cost_hour'])
    hazard_rate_active = Column('fld_hazard_rate_active',
                                Float,
                                nullable=False,
                                default=__defaults__['hazard_rate_active'])
    hazard_rate_dormant = Column('fld_hazard_rate_dormant',
                                 Float,
                                 nullable=False,
                                 default=__defaults__['hazard_rate_dormant'])
    hazard_rate_logistics = Column(
        'fld_hazard_rate_logistics',
        Float,
        nullable=False,
        default=__defaults__['hazard_rate_logistics'])
    hazard_rate_mission = Column('fld_hazard_rate_mission',
                                 Float,
                                 nullable=False,
                                 default=__defaults__['hazard_rate_mission'])
    hazard_rate_software = Column('fld_hazard_rate_software',
                                  Float,
                                  nullable=False,
                                  default=__defaults__['hazard_rate_software'])
    mmt = Column('fld_mmt', Float, nullable=False, default=__defaults__['mmt'])
    mcmt = Column('fld_mcmt',
                  Float,
                  nullable=False,
                  default=__defaults__['mcmt'])
    mpmt = Column('fld_mpmt',
                  Float,
                  nullable=False,
                  default=__defaults__['mpmt'])
    mtbf_logistics = Column('fld_mtbf_logistics',
                            Float,
                            nullable=False,
                            default=__defaults__['mtbf_logistics'])
    mtbf_mission = Column('fld_mtbf_mission',
                          Float,
                          nullable=False,
                          default=__defaults__['mtbf_mission'])
    mttr = Column('fld_mttr',
                  Float,
                  nullable=False,
                  default=__defaults__['mttr'])
    name = Column('fld_name',
                  String(128),
                  nullable=False,
                  default=__defaults__['name'])
    reliability_logistics = Column(
        'fld_reliability_logistics',
        Float,
        nullable=False,
        default=__defaults__['reliability_logistics'])
    reliability_mission = Column('fld_reliability_mission',
                                 Float,
                                 nullable=False,
                                 default=__defaults__['reliability_mission'])
    remarks = Column('fld_remarks',
                     String,
                     nullable=False,
                     default=__defaults__['remarks'])
    total_part_count = Column('fld_total_part_count',
                              Integer,
                              nullable=False,
                              default=__defaults__['total_part_count'])
    revision_code = Column('fld_revision_code',
                           String(8),
                           nullable=False,
                           default=__defaults__['revision_code'])
    program_time = Column('fld_program_time',
                          Float,
                          nullable=False,
                          default=__defaults__['program_time'])
    program_time_sd = Column('fld_program_time_sd',
                             Float,
                             nullable=False,
                             default=__defaults__['program_time_sd'])
    program_cost = Column('fld_program_cost',
                          Float,
                          nullable=False,
                          default=__defaults__['program_cost'])
    program_cost_sd = Column('fld_program_cost_sd',
                             Float,
                             nullable=False,
                             default=__defaults__['program_cost_sd'])

    # Define the relationships to other tables in the RAMSTK Program database.
    environment: relationship = relationship(
        'RAMSTKEnvironment',
        back_populates='revision',
        cascade='delete',
    )
    mission: relationship = relationship(
        'RAMSTKMission',
        back_populates='revision',
        cascade='delete',
    )
    phase: relationship = relationship(
        'RAMSTKMissionPhase',
        back_populates='revision',
        cascade='delete',
    )
    failures: relationship = relationship(
        'RAMSTKFailureDefinition',
        back_populates='revision',
    )
    function: relationship = relationship(
        'RAMSTKFunction',
        back_populates='revision',
    )
    requirement: relationship = relationship(
        'RAMSTKRequirement',
        back_populates='revision',
    )
    stakeholder: relationship = relationship(
        'RAMSTKStakeholder',
        back_populates='revision',
    )
    hardware: relationship = relationship(
        'RAMSTKHardware',
        back_populates='revision',
    )
    # software: relationship = relationship('RAMSTKSoftware',
    # back_populates='revision',)
    validation: relationship = relationship(
        'RAMSTKValidation',
        back_populates='revision',
    )
    # incident: relationship = relationship('RAMSTKIncident',
    # back_populates='revision',)
    # test: relationship = relationship('RAMSTKTest',
    # back_populates='revision',)
    # survival: relationship = relationship('RAMSTKSurvival',
    # back_populates='revision',)
    hazard: relationship = relationship(
        'RAMSTKHazardAnalysis',
        back_populates='revision',
    )
    program_status: relationship = relationship(
        'RAMSTKProgramStatus',
        back_populates='revision',
    )

    def get_attributes(self):
        """Retrieve current values of the RAMSTKRevision data model attributes.

        :return: {revision_id, availability, mission_availability, cost,
                  cost_per_failure, cost_per_hour, active_hazard_rate,
                  dormant_hazard_rate, mission_hazard_rate, hazard_rate,
                  software_hazard_rate, mmt, mcmt, mpmt, mission_mtbf, mtbf,
                  mttr, name, mission_reliability, reliability, remarks,
                  n_parts, code, program_time, program_time_se, program_cost,
                  program_cost_se} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'availability_logistics': self.availability_logistics,
            'availability_mission': self.availability_mission,
            'cost': self.cost,
            'cost_failure': self.cost_failure,
            'cost_hour': self.cost_hour,
            'hazard_rate_active': self.hazard_rate_active,
            'hazard_rate_dormant': self.hazard_rate_dormant,
            'hazard_rate_logistics': self.hazard_rate_logistics,
            'hazard_rate_mission': self.hazard_rate_mission,
            'hazard_rate_software': self.hazard_rate_software,
            'mmt': self.mmt,
            'mcmt': self.mcmt,
            'mpmt': self.mpmt,
            'mtbf_logistics': self.mtbf_logistics,
            'mtbf_mission': self.mtbf_mission,
            'mttr': self.mttr,
            'name': self.name,
            'reliability_logistics': self.reliability_logistics,
            'reliability_mission': self.reliability_mission,
            'remarks': self.remarks,
            'total_part_count': self.total_part_count,
            'revision_code': self.revision_code,
            'program_time': self.program_time,
            'program_time_sd': self.program_time_sd,
            'program_cost': self.program_cost,
            'program_cost_sd': self.program_cost_sd,
        }

        return _attributes
