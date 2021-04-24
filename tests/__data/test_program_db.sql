CREATE TABLE ramstk_revision (
    fld_revision_id INTEGER NOT NULL,
    fld_availability_logistics FLOAT NOT NULL,
    fld_availability_mission FLOAT NOT NULL,
    fld_cost FLOAT NOT NULL,
    fld_cost_failure FLOAT NOT NULL,
    fld_cost_hour FLOAT NOT NULL,
    fld_hazard_rate_active FLOAT NOT NULL,
    fld_hazard_rate_dormant FLOAT NOT NULL,
    fld_hazard_rate_logistics FLOAT NOT NULL,
    fld_hazard_rate_mission FLOAT NOT NULL,
    fld_hazard_rate_software FLOAT NOT NULL,
    fld_mmt FLOAT NOT NULL,
    fld_mcmt FLOAT NOT NULL,
    fld_mpmt FLOAT NOT NULL,
    fld_mtbf_logistics FLOAT NOT NULL,
    fld_mtbf_mission FLOAT NOT NULL,
    fld_mttr FLOAT NOT NULL,
    fld_name VARCHAR(128) NOT NULL,
    fld_reliability_logistics FLOAT NOT NULL,
    fld_reliability_mission FLOAT NOT NULL,
    fld_remarks VARCHAR NOT NULL,
    fld_total_part_count INTEGER NOT NULL,
    fld_revision_code VARCHAR(8) NOT NULL,
    fld_program_time FLOAT NOT NULL,
    fld_program_time_sd FLOAT NOT NULL,
    fld_program_cost FLOAT NOT NULL,
    fld_program_cost_sd FLOAT NOT NULL,
    PRIMARY KEY (fld_revision_id)
);
INSERT INTO "ramstk_revision" VALUES(1,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Test Revision',1.0,1.0,X'',1,'',0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_revision" VALUES(2,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'Test Revision 2',1.0,1.0,X'',1,'',0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_program_info (
    fld_revision_id INTEGER NOT NULL,
    fld_function_active INTEGER,
    fld_requirement_active INTEGER,
    fld_hardware_active INTEGER,
    fld_software_active INTEGER,
    fld_rcm_active INTEGER,
    fld_testing_active INTEGER,
    fld_incident_active INTEGER,
    fld_survival_active INTEGER,
    fld_vandv_active INTEGER,
    fld_hazard_active INTEGER,
    fld_stakeholder_active INTEGER,
    fld_allocation_active INTEGER,
    fld_similar_item_active INTEGER,
    fld_fmea_active INTEGER,
    fld_pof_active INTEGER,
    fld_rbd_active INTEGER,
    fld_fta_active INTEGER,
    fld_created_on DATE DEFAULT CURRENT_DATE,
    fld_created_by VARCHAR(512),
    fld_last_saved_on DATE DEFAULT CURRENT_DATE,
    fld_last_saved_by VARCHAR(512),
    PRIMARY KEY (fld_revision_id)
);
INSERT INTO "ramstk_program_info" VALUES(1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,CURRENT_DATE,'',CURRENT_DATE,'');
CREATE TABLE ramstk_program_status (
    fld_revision_id INTEGER NOT NULL,
    fld_status_id INTEGER NOT NULL,
    fld_cost_remaining FLOAT,
    fld_date_status DATE,
    fld_time_remaining FLOAT,
    PRIMARY KEY (fld_status_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id),
    UNIQUE (fld_date_status)
);
INSERT INTO "ramstk_program_status" VALUES(1,1,0.0,'2019-07-21',0.0);
CREATE TABLE ramstk_mission (
    fld_revision_id INTEGER,
    fld_mission_id INTEGER NOT NULL,
    fld_description VARCHAR,
    fld_mission_time FLOAT,
    fld_time_units VARCHAR(256),
    PRIMARY KEY (fld_mission_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mission" VALUES(1,1,'Test Mission 1',0.0,'hours');
INSERT INTO "ramstk_mission" VALUES(1,2,'Test Mission 2',0.0,'hours');
INSERT INTO "ramstk_mission" VALUES(1,3,'Test Mission 3',0.0,'hours');
CREATE TABLE ramstk_mission_phase (
    fld_revision_id INTEGER,
    fld_mission_id INTEGER,
    fld_phase_id INTEGER NOT NULL,
    fld_description VARCHAR,
    fld_name VARCHAR(256),
    fld_phase_start FLOAT,
    fld_phase_end FLOAT,
    PRIMARY KEY (fld_phase_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_mission_id) REFERENCES ramstk_mission (fld_mission_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mission_phase" VALUES(1,1,1,'Test Mission Phase 1','',0.0,0.0);
INSERT INTO "ramstk_mission_phase" VALUES(1,2,2,'Test Mission Phase 2','',0.0,0.0);
INSERT INTO "ramstk_mission_phase" VALUES(1,3,3,'Test Mission Phase 3','',0.0,0.0);
CREATE TABLE ramstk_environment (
    fld_revision_id INTEGER,
    fld_phase_id INTEGER,
    fld_environment_id INTEGER NOT NULL,
    fld_name VARCHAR(256),
    fld_units VARCHAR(128),
    fld_minimum FLOAT,
    fld_maximum FLOAT,
    fld_mean FLOAT,
    fld_variance FLOAT,
    fld_ramp_rate FLOAT,
    fld_low_dwell_time FLOAT,
    fld_high_dwell_time FLOAT,
    PRIMARY KEY (fld_environment_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_phase_id) REFERENCES ramstk_mission_phase (fld_phase_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_environment" VALUES(1,1,1,'Condition Name','Units',0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_environment" VALUES(1,2,2,'Condition Name 2','Units',0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_environment" VALUES(1,3,3,'Condition Name 3','Units',0.0,0.0,0.0,0.0,0.0,0.0,0.0);

CREATE TABLE ramstk_failure_definition (
    fld_revision_id INTEGER,
    fld_definition_id INTEGER NOT NULL,
    fld_definition VARCHAR(1024),
    PRIMARY KEY (fld_definition_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_failure_definition" VALUES(1,1,'Failure Definition');
INSERT INTO "ramstk_failure_definition" VALUES(1,2,'Failure Definition');

CREATE TABLE ramstk_hardware (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_alt_part_number VARCHAR(256),
    fld_attachments VARCHAR(512),
    fld_cage_code VARCHAR(256),
    fld_category_id INTEGER,
    fld_comp_ref_des VARCHAR(256),
    fld_cost FLOAT,
    fld_cost_failure FLOAT,
    fld_cost_hour FLOAT,
    fld_cost_type_id INTEGER,
    fld_description VARCHAR(512),
    fld_duty_cycle FLOAT,
    fld_figure_number VARCHAR(256),
    fld_lcn VARCHAR(256),
    fld_level INTEGER,
    fld_manufacturer_id INTEGER,
    fld_mission_time FLOAT,
    fld_name VARCHAR(256),
    fld_nsn VARCHAR(256),
    fld_page_number VARCHAR(256),
    fld_parent_id INTEGER,
    fld_part INTEGER,
    fld_part_number VARCHAR(256),
    fld_quantity INTEGER,
    fld_ref_des VARCHAR(256),
    fld_remarks VARCHAR,
    fld_repairable INTEGER,
    fld_specification_number VARCHAR(256),
    fld_subcategory_id INTEGER,
    fld_tagged_part INTEGER,
    fld_total_cost FLOAT,
    fld_total_part_count INTEGER,
    fld_total_power_dissipation FLOAT,
    fld_year_of_manufacture INTEGER,
    PRIMARY KEY (fld_hardware_id),
    CONSTRAINT ramstk_hardware_ukey UNIQUE (fld_revision_id, fld_hardware_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_hardware" VALUES(1,1,'','','',0,'S1',5.28,0.0,1.85263157894736840859e-05,2,'Test System',100.0,'','',0,0,10.0,'','','',0,0,'',1,'S1','',0,'',0,0,5.28,10,0.0,2019);
INSERT INTO "ramstk_hardware" VALUES(1,2,'','','',0,'S1:SS1',0.0,0.0,0.0,0,'Test Sub-System 1',100.0,'','',0,0,100.0,'','','',1,0,'',1,'SS1','',0,'',0,0,0.0,0,0.0,2019);
INSERT INTO "ramstk_hardware" VALUES(1,3,'','','',0,'S1:SS2',1282.95,0.0,0.0,0,'Test Sub-System 2',100.0,'','',0,0,100.0,'','','',1,0,'',1,'SS2','',0,'',0,0,0.0,55,4.67,2019);
INSERT INTO "ramstk_hardware" VALUES(1,4,'','','',0,'S1:SS3',0.0,0.0,0.0,0,'Test Sub-System 3',100.0,'','',0,0,100.0,'','','',1,0,'',1,'SS3','',0,'',0,0,0.0,0,0.0,2019);
INSERT INTO "ramstk_hardware" VALUES(1,5,'','','',0,'S1:SS4',438.19,0.0,0.0,0,'Test Sub-System 4',100.0,'','',0,0,100.0,'','','',1,0,'',1,'SS4','',0,'',0,0,0.0,89,45.89,2019);
INSERT INTO "ramstk_hardware" VALUES(1,6,'','','',0,'S1:SS1:A1',832.98,0.0,0.0,0,'Test Assembly 1',100.0,'','',0,0,100.0,'Test Assembly 6','','',2,0,'',1,'A1','',0,'',0,0,0.0,132,12.3,2019);
INSERT INTO "ramstk_hardware" VALUES(1,7,'','','',0,'S1:SS1:A2',1432.86,0.0,0.0,0,'Test Assembly 2',100.0,'','',0,0,100.0,'Test Assembly 7','','',2,0,'',1,'A2','',0,'',0,0,0.0,26,0.967,2019);
INSERT INTO "ramstk_hardware" VALUES(1,8,'','','',4,'S1:SS1:A2:C1',0.0,0.0,0.0,0,'Test Capacitor 1',100.0,'','',0,0,100.0,'Test Capacitor','','',7,1,'',1,'C1','',0,'',1,0,0.0,0,0.0,2019);

CREATE TABLE ramstk_mode (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_critical_item INTEGER,
    fld_description VARCHAR(512),
    fld_design_provisions VARCHAR,
    fld_detection_method VARCHAR(512),
    fld_effect_end VARCHAR(512),
    fld_effect_local VARCHAR(512),
    fld_effect_next VARCHAR(512),
    fld_effect_probability FLOAT,
    fld_hazard_rate_source VARCHAR(512),
    fld_isolation_method VARCHAR(512),
    fld_mission VARCHAR(64),
    fld_mission_phase VARCHAR(64),
    fld_mode_criticality FLOAT,
    fld_mode_hazard_rate FLOAT,
    fld_mode_op_time FLOAT,
    fld_mode_probability VARCHAR(64),
    fld_mode_ratio FLOAT,
    fld_operator_actions VARCHAR,
    fld_other_indications VARCHAR(512),
    fld_remarks VARCHAR,
    fld_rpn_severity INTEGER,
    fld_rpn_severity_new INTEGER,
    fld_severity_class VARCHAR(64),
    fld_single_point INTEGER,
    fld_type_id INTEGER,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id) REFERENCES ramstk_hardware (fld_revision_id, fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mode" VALUES(1,1,4,0,'System Test Failure Mode #1','','','','','',1.0,'','','Default Mission','',0.0,0.0,10.0,'',0.5,'','','',1,1,'IV',0,0);
INSERT INTO "ramstk_mode" VALUES(1,1,5,0,'System Test Failure Mode #2','','','','','',0.75,'','','Default Mission','',0.0,0.0,5.0,'',0.2,'','','',1,1,'I',0,0);
INSERT INTO "ramstk_mode" VALUES(1,1,6,0,'System Test Failure Mode #3','','','','','',0.9,'','','Default Mission','',0.0,0.0,10.0,'',0.3,'','','',1,1,'I',0,0);
CREATE TABLE ramstk_mechanism (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    fld_pof_include INTEGER,
    fld_rpn INTEGER,
    fld_rpn_detection INTEGER,
    fld_rpn_detection_new INTEGER,
    fld_rpn_new INTEGER,
    fld_rpn_occurrence INTEGER,
    fld_rpn_occurrence_new INTEGER,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id) REFERENCES ramstk_mode (fld_revision_id, fld_hardware_id, fld_mode_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mechanism" VALUES(1,1,4,1,'Test Failure Mechanism #1 for Mode ID 4',1,0,8,7,0,2,2);
INSERT INTO "ramstk_mechanism" VALUES(1,1,5,1,'Test Failure Mechanism #1 for Mode ID 5',1,0,2,5,0,4,4);
INSERT INTO "ramstk_mechanism" VALUES(1,1,6,1,'Test Failure Mechanism #1 for Mode ID 6',1,0,5,2,0,7,5);
CREATE TABLE ramstk_cause (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_cause_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    fld_rpn INTEGER,
    fld_rpn_detection INTEGER,
    fld_rpn_detection_new INTEGER,
    fld_rpn_new INTEGER,
    fld_rpn_occurrence INTEGER,
    fld_rpn_occurrence_new INTEGER,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id) REFERENCES ramstk_mechanism (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_cause" VALUES(1,1,4,1,1,'Test Failure Cause #1 for Mechanism ID 1',0,2,1,0,8,5);
INSERT INTO "ramstk_cause" VALUES(1,1,5,1,1,'Test Failure Cause #2 for Mechanism ID 2',0,4,3,0,4,3);
INSERT INTO "ramstk_cause" VALUES(1,1,6,1,1,'Test Failure Cause #1 for Mechanism ID 3',0,3,3,0,6,4);
CREATE TABLE ramstk_action (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_cause_id INTEGER NOT NULL,
    fld_action_id INTEGER NOT NULL,
    fld_action_recommended VARCHAR,
    fld_action_category VARCHAR(512),
    fld_action_owner VARCHAR(512),
    fld_action_due_date DATE,
    fld_action_status VARCHAR(512),
    fld_action_taken VARCHAR,
    fld_action_approved INTEGER,
    fld_action_approve_date DATE,
    fld_action_closed INTEGER,
    fld_action_close_date DATE,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id, fld_action_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id) REFERENCES ramstk_cause (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_action" VALUES(1,1,4,1,1,1,'Test FMEA Recommended Action #1 for Cause ID 1.','','','2019-08-20','',X'',0,'2019-08-20',0,'2019-08-20');
INSERT INTO "ramstk_action" VALUES(1,1,5,1,1,1,'Test FMEA Recommended Action #1 for Cause ID 2.','','','2019-08-20','',X'',0,'2019-08-20',0,'2019-08-20');
INSERT INTO "ramstk_action" VALUES(1,1,6,1,1,1,'Test FMEA Recommended Action #1 for Cause ID 3','','','2019-08-20','',X'',0,'2019-08-20',0,'2019-08-20');
CREATE TABLE ramstk_control (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_cause_id INTEGER NOT NULL,
    fld_control_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    fld_type_id VARCHAR(512),
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id, fld_control_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id) REFERENCES ramstk_cause (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_cause_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_control" VALUES(1,1,4,1,1,1,'Test FMEA Control #1 for Mode ID 4','');
INSERT INTO "ramstk_control" VALUES(1,1,5,1,1,1,'Test FMEA Control #1 for Mode ID 5','');
INSERT INTO "ramstk_control" VALUES(1,1,6,1,1,1,'Test FMEA Control #1 for Mode ID 6','');
CREATE TABLE ramstk_op_load (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_load_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    fld_damage_model VARCHAR(512),
    fld_priority_id INTEGER,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id) REFERENCES ramstk_mechanism (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_op_load" VALUES(1,1,4,1,1,'Test Operating Load #1','',0);
INSERT INTO "ramstk_op_load" VALUES(1,1,5,1,1,'Test Operating Load #2','',0);
INSERT INTO "ramstk_op_load" VALUES(1,1,6,1,1,'Test Operating Load #3','',0);
CREATE TABLE ramstk_op_stress (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_load_id INTEGER NOT NULL,
    fld_stress_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    fld_load_history VARCHAR(512),
    fld_measurable_parameter VARCHAR(512),
    fld_remarks VARCHAR,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id, fld_stress_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id) REFERENCES ramstk_op_load (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_op_stress" VALUES(1,1,4,1,1,1,'Test Operating Stress #1','Histogram','','');
INSERT INTO "ramstk_op_stress" VALUES(1,1,5,1,1,1,'Test Operating Stress #2','Histogram','','');
INSERT INTO "ramstk_op_stress" VALUES(1,1,6,1,1,1,'Test Operating Stress #3','Histogram','','');
CREATE TABLE ramstk_test_method (
    fld_revision_id INTEGER NOT NULL,
    fld_hardware_id INTEGER NOT NULL,
    fld_mode_id INTEGER NOT NULL,
    fld_mechanism_id INTEGER NOT NULL,
    fld_load_id INTEGER NOT NULL,
    fld_test_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    fld_boundary_conditions VARCHAR(512),
    fld_remarks VARCHAR,
    PRIMARY KEY (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id, fld_test_id),
    FOREIGN KEY(fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id) REFERENCES ramstk_op_load (fld_revision_id, fld_hardware_id, fld_mode_id, fld_mechanism_id, fld_load_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_test_method" VALUES(1,1,4,1,1,1,'Test Test Method #1','','');
INSERT INTO "ramstk_test_method" VALUES(1,1,5,1,1,1,'Test Test Method #2','','');
INSERT INTO "ramstk_test_method" VALUES(1,1,6,1,1,1,'Test Test Method #3','','');
CREATE TABLE ramstk_load_history (
    fld_load_history_id INTEGER NOT NULL,
    fld_description VARCHAR(512),
    PRIMARY KEY (fld_load_history_id)
);
CREATE TABLE ramstk_allocation (
    fld_revision_id INTEGER,
    fld_hardware_id INTEGER,
    fld_availability_alloc FLOAT,
    fld_duty_cycle FLOAT,
    fld_env_factor INTEGER,
    fld_goal_measure_id INTEGER,
    fld_hazard_rate_alloc FLOAT,
    fld_hazard_rate_goal FLOAT,
    fld_included INTEGER,
    fld_int_factor INTEGER,
    fld_allocation_method_id INTEGER,
    fld_mission_time FLOAT,
    fld_mtbf_alloc FLOAT,
    fld_mtbf_goal FLOAT,
    fld_n_sub_systems INTEGER,
    fld_n_sub_elements INTEGER,
    fld_parent_id INTEGER,
    fld_percent_weight_factor FLOAT,
    fld_reliability_alloc FLOAT,
    fld_reliability_goal FLOAT,
    fld_op_time_factor INTEGER,
    fld_soa_factor INTEGER,
    fld_weight_factor INTEGER,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_allocation" VALUES(1,1,0.0,100.0,1,1,0.0,0.0,1,1,1,10.0,0.0,0.0,1,1,0,0.0,1.0,1.0,1,1,1);
INSERT INTO "ramstk_allocation" VALUES(1,2,0.0,100.0,1,1,0.0,0.000617,1,1,4,100.0,0.0,0.0,1,1,1,0.0,1.0,0.995,1,1,1);
INSERT INTO "ramstk_allocation" VALUES(1,3,0.0,100.0,1,1,0.0,0.0,1,1,1,100.0,0.0,0.0,1,1,1,0.0,1.0,1.0,1,1,1);
INSERT INTO "ramstk_allocation" VALUES(1,4,0.0,100.0,1,1,0.0,0.0,1,1,1,100.0,0.0,0.0,1,1,1,0.0,1.0,1.0,1,1,1);
INSERT INTO "ramstk_allocation" VALUES(1,5,0.0,100.0,1,1,0.0,0.0,1,1,1,100.0,0.0,0.0,1,1,1,0.0,1.0,1.0,1,1,1);
INSERT INTO "ramstk_allocation" VALUES(1,6,0.0,80.0,6,1,0.000157531914893617,0.0,1,3,1,100.0,6.3479200432198813358e+03,12000.0,1,2,2,0.0,9.84370241029675296928e-01,0.9995,9,2,0.8);
INSERT INTO "ramstk_allocation" VALUES(1,7,0.0,90.0,3,1,4.59468085106382972786e-04,0.0,1,5,1,100.0,2.17642972910395928929e+03,0.0,1,4,2,0.0,0.955092763646177,1.0,9,7,0.95);
INSERT INTO "ramstk_allocation" VALUES(1,8,0.0,100.0,1,1,0.0,0.0,1,1,1,100.0,0.0,0.0,1,1,1,0.0,1.0,1.0,1,1,1);
CREATE TABLE ramstk_design_electric (
    fld_hardware_id INTEGER,
    fld_application_id INTEGER,
    fld_area FLOAT,
    fld_capacitance FLOAT,
    fld_configuration_id INTEGER,
    fld_construction_id INTEGER,
    fld_contact_form_id INTEGER,
    fld_contact_gauge INTEGER,
    fld_contact_rating_id INTEGER,
    fld_current_operating FLOAT,
    fld_current_rated FLOAT,
    fld_current_ratio FLOAT,
    fld_environment_active_id INTEGER,
    fld_environment_dormant_id INTEGER,
    fld_family_id INTEGER,
    fld_feature_size FLOAT,
    fld_frequency_operating FLOAT,
    fld_insert_id INTEGER,
    fld_insulation_id INTEGER,
    fld_manufacturing_id INTEGER,
    fld_matching_id INTEGER,
    fld_n_active_pins INTEGER,
    fld_n_circuit_planes INTEGER,
    fld_n_cycles INTEGER,
    fld_n_elements INTEGER,
    fld_n_hand_soldered INTEGER,
    fld_n_wave_soldered INTEGER,
    fld_operating_life FLOAT,
    fld_overstress INTEGER,
    fld_package_id INTEGER,
    fld_power_operating FLOAT,
    fld_power_rated FLOAT,
    fld_power_ratio FLOAT,
    fld_reason VARCHAR,
    fld_resistance FLOAT,
    fld_specification_id INTEGER,
    fld_technology_id INTEGER,
    fld_temperature_active FLOAT,
    fld_temperature_case FLOAT,
    fld_temperature_dormant FLOAT,
    fld_temperature_hot_spot FLOAT,
    fld_temperature_junction FLOAT,
    fld_temperature_knee FLOAT,
    fld_temperature_rated_max FLOAT,
    fld_temperature_rated_min FLOAT,
    fld_temperature_rise FLOAT,
    fld_theta_jc FLOAT,
    fld_type_id INTEGER,
    fld_voltage_ac_operating FLOAT,
    fld_voltage_dc_operating FLOAT,
    fld_voltage_esd FLOAT,
    fld_voltage_rated FLOAT,
    fld_voltage_ratio FLOAT,
    fld_weight FLOAT,
    fld_years_in_production INTEGER,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_design_electric" VALUES(1,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(2,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(3,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(4,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(5,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(6,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(7,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
INSERT INTO "ramstk_design_electric" VALUES(8,0,0.0,0.0,0,0,0,0,0,0.0,0.0,0.0,0,0,0,0.0,0.0,0,0,0,0,0,1,0,0,0,0,0.0,0,0,0.0,0.0,0.0,'',0.0,0,0,35.0,0.0,25.0,0.0,0.0,25.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,1);
CREATE TABLE ramstk_design_mechanic (
    fld_hardware_id INTEGER,
    fld_altitude_operating FLOAT,
    fld_application_id INTEGER,
    fld_balance_id INTEGER,
    fld_clearance FLOAT,
    fld_casing_id INTEGER,
    fld_contact_pressure FLOAT,
    fld_deflection FLOAT,
    fld_diameter_coil FLOAT,
    fld_diameter_inner FLOAT,
    fld_diameter_outer FLOAT,
    fld_diameter_wire FLOAT,
    fld_filter_size FLOAT,
    fld_flow_design FLOAT,
    fld_flow_operating FLOAT,
    fld_frequency_operating FLOAT,
    fld_friction FLOAT,
    fld_impact_id INTEGER,
    fld_leakage_allowable FLOAT,
    fld_length FLOAT,
    fld_length_compressed FLOAT,
    fld_length_relaxed FLOAT,
    fld_load_design FLOAT,
    fld_load_id INTEGER,
    fld_load_operating FLOAT,
    fld_lubrication_id INTEGER,
    fld_manufacturing_id INTEGER,
    fld_material_id INTEGER,
    fld_meyer_hardness FLOAT,
    fld_misalignment_angle FLOAT,
    fld_n_ten INTEGER,
    fld_n_cycles INTEGER,
    fld_n_elements INTEGER,
    fld_offset FLOAT,
    fld_particle_size FLOAT,
    fld_pressure_contact FLOAT,
    fld_pressure_delta FLOAT,
    fld_pressure_downstream FLOAT,
    fld_pressure_rated FLOAT,
    fld_pressure_upstream FLOAT,
    fld_rpm_design FLOAT,
    fld_rpm_operating FLOAT,
    fld_service_id INTEGER,
    fld_spring_index FLOAT,
    fld_surface_finish FLOAT,
    fld_technology_id INTEGER,
    fld_thickness FLOAT,
    fld_torque_id INTEGER,
    fld_type_id INTEGER,
    fld_viscosity_design FLOAT,
    fld_viscosity_dynamic FLOAT,
    fld_water_per_cent FLOAT,
    fld_width_minimum FLOAT,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_design_mechanic" VALUES(1,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(2,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(3,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(4,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(5,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(6,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(7,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_design_mechanic" VALUES(8,0.0,0,0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0,0.0,0,0,0,0.0,0.0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0.0,0.0,0,0.0,0,0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_mil_hdbk_f (
    fld_hardware_id INTEGER,
    fld_a_one FLOAT,
    fld_a_two FLOAT,
    fld_b_one FLOAT,
    fld_b_two FLOAT,
    fld_c_one FLOAT,
    fld_c_two FLOAT,
    fld_lambda_bd FLOAT,
    fld_lambda_bp FLOAT,
    fld_lambda_cyc FLOAT,
    fld_lambda_eos FLOAT,
    fld_pi_a FLOAT,
    fld_pi_c FLOAT,
    fld_pi_cd FLOAT,
    fld_pi_cf FLOAT,
    fld_pi_cr FLOAT,
    fld_pi_cv FLOAT,
    fld_pi_cyc FLOAT,
    fld_pi_e FLOAT,
    fld_pi_f FLOAT,
    fld_pi_i FLOAT,
    fld_pi_k FLOAT,
    fld_pi_l FLOAT,
    fld_pi_m FLOAT,
    fld_pi_mfg FLOAT,
    fld_pi_n FLOAT,
    fld_pi_nr FLOAT,
    fld_pi_p FLOAT,
    fld_pi_pt FLOAT,
    fld_pi_q FLOAT,
    fld_pi_r FLOAT,
    fld_pi_s FLOAT,
    fld_pi_t FLOAT,
    fld_pi_taps FLOAT,
    fld_pi_u FLOAT,
    fld_pi_v FLOAT,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(4,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(6,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(7,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_mil_hdbk_f" VALUES(8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_nswc (
    fld_hardware_id INTEGER,
    fld_c_ac FLOAT,
    fld_c_alt FLOAT,
    fld_c_b FLOAT,
    fld_c_bl FLOAT,
    fld_c_bt FLOAT,
    fld_c_bv FLOAT,
    fld_c_c FLOAT,
    fld_c_cf FLOAT,
    fld_c_cp FLOAT,
    fld_c_cs FLOAT,
    fld_c_cv FLOAT,
    fld_c_cw FLOAT,
    fld_c_d FLOAT,
    fld_c_dc FLOAT,
    fld_c_dl FLOAT,
    fld_c_dp FLOAT,
    fld_c_ds FLOAT,
    fld_c_dt FLOAT,
    fld_c_dw FLOAT,
    fld_c_dy FLOAT,
    fld_c_e FLOAT,
    fld_c_f FLOAT,
    fld_c_g FLOAT,
    fld_c_ga FLOAT,
    fld_c_gl FLOAT,
    fld_c_gp FLOAT,
    fld_c_gs FLOAT,
    fld_c_gt FLOAT,
    fld_c_gv FLOAT,
    fld_c_h FLOAT,
    fld_c_i FLOAT,
    fld_c_k FLOAT,
    fld_c_l FLOAT,
    fld_c_lc FLOAT,
    fld_c_m FLOAT,
    fld_c_mu FLOAT,
    fld_c_n FLOAT,
    fld_c_np FLOAT,
    fld_c_nw FLOAT,
    fld_c_p FLOAT,
    fld_c_pd FLOAT,
    fld_c_pf FLOAT,
    fld_c_pv FLOAT,
    fld_c_q FLOAT,
    fld_c_r FLOAT,
    fld_c_rd FLOAT,
    fld_c_s FLOAT,
    fld_c_sc FLOAT,
    fld_c_sf FLOAT,
    fld_c_st FLOAT,
    fld_c_sv FLOAT,
    fld_c_sw FLOAT,
    fld_c_sz FLOAT,
    fld_c_t FLOAT,
    fld_c_v FLOAT,
    fld_c_w FLOAT,
    fld_c_y FLOAT,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_nswc" VALUES(1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(4,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(6,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(7,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_nswc" VALUES(8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0);
CREATE TABLE ramstk_reliability (
    fld_hardware_id INTEGER,
    fld_add_adj_factor FLOAT,
    fld_availability_logistics FLOAT,
    fld_availability_mission FLOAT,
    fld_avail_log_variance FLOAT,
    fld_avail_mis_variance FLOAT,
    fld_failure_distribution_id INTEGER,
    fld_hazard_rate_active FLOAT,
    fld_hazard_rate_dormant FLOAT,
    fld_hazard_rate_logistics FLOAT,
    fld_hazard_rate_method_id INTEGER,
    fld_hazard_rate_mission FLOAT,
    fld_hazard_rate_model VARCHAR(512),
    fld_hazard_rate_percent FLOAT,
    fld_hazard_rate_software FLOAT,
    fld_hazard_rate_specified FLOAT,
    fld_hazard_rate_type_id INTEGER,
    fld_hr_active_variance FLOAT,
    fld_hr_dormant_variance FLOAT,
    fld_hr_log_variance FLOAT,
    fld_hr_mis_variance FLOAT,
    fld_hr_spec_variance FLOAT,
    fld_lambda_b FLOAT,
    fld_location_parameter FLOAT,
    fld_mtbf_logistics FLOAT,
    fld_mtbf_mission FLOAT,
    fld_mtbf_specified FLOAT,
    fld_mtbf_log_variance FLOAT,
    fld_mtbf_mis_variance FLOAT,
    fld_mtbf_spec_variance FLOAT,
    fld_mult_adj_factor FLOAT,
    fld_quality_id INTEGER,
    fld_reliability_goal FLOAT,
    fld_reliability_goal_measure_id INTEGER,
    fld_reliability_logistics FLOAT,
    fld_reliability_mission FLOAT,
    fld_reliability_log_variance FLOAT,
    fld_reliability_mis_variance FLOAT,
    fld_scale_parameter FLOAT,
    fld_shape_parameter FLOAT,
    fld_survival_analysis_id INTEGER,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_reliability" VALUES(1,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0,0.0,'',0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(2,0.0,1.0,1.0,0.0,0.0,0,0.00617,0.0,0.0,0,0.0,'',0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(3,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0,0.0,'',0.0,0.045,0.0,3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,38292.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(4,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0,0.0,'',0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(5,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0035,0.0,0,0.0,'',0.0,0.0,0.15,2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(6,0.0,1.0,1.0,0.0,0.0,0,2.89e-06,0.0,0.0,0,0.0,'',0.0,2.3,0.045,2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.9995,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(7,0.0,1.0,1.0,0.0,0.0,0,1.132e-07,0.0,0.0,0,0.0,'',0.0,0.0,0.0,3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,89560.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
INSERT INTO "ramstk_reliability" VALUES(8,0.0,1.0,1.0,0.0,0.0,0,0.0,0.0,0.0,0,0.0,'',0.0,0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0,0.0,0,1.0,1.0,0.0,0.0,0.0,0.0,0);
CREATE TABLE ramstk_similar_item (
    fld_revision_id INTEGER,
    fld_hardware_id INTEGER,
    fld_change_description_1 VARCHAR,
    fld_change_description_2 VARCHAR,
    fld_change_description_3 VARCHAR,
    fld_change_description_4 VARCHAR,
    fld_change_description_5 VARCHAR,
    fld_change_description_6 VARCHAR,
    fld_change_description_7 VARCHAR,
    fld_change_description_8 VARCHAR,
    fld_change_description_9 VARCHAR,
    fld_change_description_10 VARCHAR,
    fld_change_factor_1 FLOAT,
    fld_change_factor_2 FLOAT,
    fld_change_factor_3 FLOAT,
    fld_change_factor_4 FLOAT,
    fld_change_factor_5 FLOAT,
    fld_change_factor_6 FLOAT,
    fld_change_factor_7 FLOAT,
    fld_change_factor_8 FLOAT,
    fld_change_factor_9 FLOAT,
    fld_change_factor_10 FLOAT,
    fld_environment_from_id INTEGER,
    fld_environment_to_id INTEGER,
    fld_function_1 VARCHAR(128),
    fld_function_2 VARCHAR(128),
    fld_function_3 VARCHAR(128),
    fld_function_4 VARCHAR(128),
    fld_function_5 VARCHAR(128),
    fld_similar_item_method_id INTEGER,
    fld_parent_id INTEGER,
    fld_quality_from_id INTEGER,
    fld_quality_to_id INTEGER,
    fld_result_1 FLOAT,
    fld_result_2 FLOAT,
    fld_result_3 FLOAT,
    fld_result_4 FLOAT,
    fld_result_5 FLOAT,
    fld_temperature_from FLOAT,
    fld_temperature_to FLOAT,
    fld_user_blob_1 VARCHAR,
    fld_user_blob_2 VARCHAR,
    fld_user_blob_3 VARCHAR,
    fld_user_blob_4 VARCHAR,
    fld_user_blob_5 VARCHAR,
    fld_user_float_1 FLOAT,
    fld_user_float_2 FLOAT,
    fld_user_float_3 FLOAT,
    fld_user_float_4 FLOAT,
    fld_user_float_5 FLOAT,
    fld_user_int_1 INTEGER,
    fld_user_int_2 INTEGER,
    fld_user_int_3 INTEGER,
    fld_user_int_4 INTEGER,
    fld_user_int_5 INTEGER,
    PRIMARY KEY (fld_hardware_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_hardware_id) REFERENCES ramstk_hardware (fld_hardware_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_similar_item" VALUES(1,1,'','','','','','','','','','',1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0,0,'0','0','0','0','0',1,0,0,0,0.0,0.0,0.0,0.0,0.0,30.0,30.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
INSERT INTO "ramstk_similar_item" VALUES(1,2,'54657374206368616E6765206465736372697074696F6E20666F7220666163746F722023312E','','','','','','','','','',0.85,1.2,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,2,3,'pi1*pi2*hr','0','0','0','0',2,1,1,2,0.0,0.0,0.0,0.0,0.0,55.0,65.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
INSERT INTO "ramstk_similar_item" VALUES(1,3,'','','','','','','','','','',1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0,0,'0','0','0','0','0',1,1,0,0,0.0,0.0,0.0,0.0,0.0,30.0,30.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
INSERT INTO "ramstk_similar_item" VALUES(1,4,'','','','','','','','','','',1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0,0,'0','0','0','0','0',1,1,0,0,0.0,0.0,0.0,0.0,0.0,30.0,30.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
INSERT INTO "ramstk_similar_item" VALUES(1,5,'','','','','','','','','','',1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0,0,'0','0','0','0','0',1,1,0,0,0.0,0.0,0.0,0.0,0.0,30.0,30.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
INSERT INTO "ramstk_similar_item" VALUES(1,6,'54686973206973206368616E67652064656372697074696F6E203120666F7220617373656D626C792036','54686973206973206368616E67652064656372697074696F6E203220666F7220617373656D626C792036','54686973206973206368616E67652064656372697074696F6E203320666F7220617373656D626C792036','','','','','','','',1.0,1.0,1.0,1.0,0.95,1.0,1.0,1.0,1.0,1.0,0,0,'0','0','0','0','0',1,2,0,0,0.0,0.0,0.0,0.0,0.0,30.0,30.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);
INSERT INTO "ramstk_similar_item" VALUES(1,7,'54686973206973206368616E67652064656372697074696F6E203120666F7220617373656D626C792037','54686973206973206368616E67652064656372697074696F6E203220666F7220617373656D626C792037','54686973206973206368616E67652064656372697074696F6E203320666F7220617373656D626C792037','','','','','','','',1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0,0,'0','0','0','0','0',1,2,0,0,0.0,0.0,0.0,0.0,0.0,30.0,30.0,'','','','','',0.0,0.0,0.0,0.0,0.0,0,0,0,0,0);

CREATE TABLE ramstk_function (
    fld_revision_id INTEGER,
    fld_function_id INTEGER NOT NULL,
    fld_availability_logistics FLOAT,
    fld_availability_mission FLOAT,
    fld_cost FLOAT,
    fld_function_code VARCHAR(16),
    fld_hazard_rate_logistics FLOAT,
    fld_hazard_rate_mission FLOAT,
    fld_level INTEGER,
    fld_mmt FLOAT,
    fld_mcmt FLOAT,
    fld_mpmt FLOAT,
    fld_mtbf_logistics FLOAT,
    fld_mtbf_mission FLOAT,
    fld_mttr FLOAT,
    fld_name VARCHAR(256),
    fld_parent_id INTEGER,
    fld_remarks VARCHAR,
    fld_safety_critical INTEGER,
    fld_total_mode_count INTEGER,
    fld_total_part_count INTEGER,
    fld_type_id INTEGER,
    PRIMARY KEY (fld_function_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_function" VALUES(1,1,1.0,1.0,0.0,'FUNC-0001',0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,'Function Name',0,'',0,0,0,0);
INSERT INTO "ramstk_function" VALUES(1,2,1.0,1.0,0.0,'FUNC-0002',0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,'Function Name',0,'',0,0,0,0);
INSERT INTO "ramstk_function" VALUES(1,3,1.0,1.0,0.0,'FUNC-0003',0.0,0.0,0,0.0,0.0,0.0,0.0,0.0,0.0,'Function Name',0,'',0,0,0,0);
CREATE TABLE ramstk_hazard_analysis (
    fld_revision_id INTEGER,
    fld_function_id INTEGER,
    fld_hazard_id INTEGER NOT NULL,
    fld_potential_hazard VARCHAR(256),
    fld_potential_cause VARCHAR(512),
    fld_assembly_effect VARCHAR(512),
    fld_assembly_severity VARCHAR(256),
    fld_assembly_probability VARCHAR(256),
    fld_assembly_hri INTEGER,
    fld_assembly_mitigation VARCHAR,
    fld_assembly_severity_f VARCHAR(256),
    fld_assembly_probability_f VARCHAR(256),
    fld_assembly_hri_f INTEGER,
    fld_function_1 VARCHAR(128),
    fld_function_2 VARCHAR(128),
    fld_function_3 VARCHAR(128),
    fld_function_4 VARCHAR(128),
    fld_function_5 VARCHAR(128),
    fld_remarks VARCHAR,
    fld_result_1 FLOAT,
    fld_result_2 FLOAT,
    fld_result_3 FLOAT,
    fld_result_4 FLOAT,
    fld_result_5 FLOAT,
    fld_system_effect VARCHAR(512),
    fld_system_severity VARCHAR(256),
    fld_system_probability VARCHAR(256),
    fld_system_hri INTEGER,
    fld_system_mitigation VARCHAR,
    fld_system_severity_f VARCHAR(256),
    fld_system_probability_f VARCHAR(256),
    fld_system_hri_f INTEGER,
    fld_user_blob_1 VARCHAR,
    fld_user_blob_2 VARCHAR,
    fld_user_blob_3 VARCHAR,
    fld_user_float_1 FLOAT,
    fld_user_float_2 FLOAT,
    fld_user_float_3 FLOAT,
    fld_user_int_1 INTEGER,
    fld_user_int_2 INTEGER,
    fld_user_int_3 INTEGER,
    PRIMARY KEY (fld_hazard_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE,
    FOREIGN KEY(fld_function_id) REFERENCES ramstk_function (fld_function_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_hazard_analysis" VALUES(1,1,1,'','','','Medium','Level A - Frequent',20,'','Medium','Level A - Frequent',4,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','Medium','Level A - Frequent',20,'','Medium','Level A - Frequent',20,'','','',0.0,0.0,0.0,0,0,0);
INSERT INTO "ramstk_hazard_analysis" VALUES(1,2,2,'','','','Major','Level A - Frequent',20,'','Major','Level A - Frequent',20,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','Major','Level A - Frequent',20,'','Major','Level A - Frequent',20,'','','',0.0,0.0,0.0,0,0,0);
INSERT INTO "ramstk_hazard_analysis" VALUES(1,3,3,'','','','Major','Level A - Frequent',20,'','Major','Level A - Frequent',20,'','','','','','',0.0,0.0,0.0,0.0,0.0,'','Major','Level A - Frequent',20,'','Major','Level A - Frequent',20,'','','',0.0,0.0,0.0,0,0,0);

CREATE TABLE ramstk_incident (
    fld_revision_id INTEGER NOT NULL,
    fld_incident_id INTEGER NOT NULL,
    fld_accepted INTEGER,
    fld_approved INTEGER,
    fld_approved_by INTEGER,
    fld_analysis VARCHAR,
    fld_category_id INTEGER,
    fld_chargeable INTEGER,
    fld_chargeable_1 INTEGER,
    fld_chargeable_2 INTEGER,
    fld_chargeable_3 INTEGER,
    fld_chargeable_4 INTEGER,
    fld_chargeable_5 INTEGER,
    fld_chargeable_6 INTEGER,
    fld_chargeable_7 INTEGER,
    fld_chargeable_8 INTEGER,
    fld_chargeable_9 INTEGER,
    fld_chargeable_10 INTEGER,
    fld_complete INTEGER,
    fld_complete_by INTEGER,
    fld_cost FLOAT,
    fld_criticality_id INTEGER,
    fld_date_approved DATE,
    fld_date_complete DATE,
    fld_date_requested DATE,
    fld_date_reviewed DATE,
    fld_description_long VARCHAR,
    fld_description_short VARCHAR(512),
    fld_detection_method_id INTEGER,
    fld_execution_time FLOAT,
    fld_hardware_id INTEGER,
    fld_incident_age INTEGER,
    fld_life_cycle_id INTEGER,
    fld_relevant INTEGER,
    fld_relevant_1 INTEGER,
    fld_relevant_2 INTEGER,
    fld_relevant_3 INTEGER,
    fld_relevant_4 INTEGER,
    fld_relevant_5 INTEGER,
    fld_relevant_6 INTEGER,
    fld_relevant_7 INTEGER,
    fld_relevant_8 INTEGER,
    fld_relevant_9 INTEGER,
    fld_relevant_10 INTEGER,
    fld_relevant_11 INTEGER,
    fld_relevant_12 INTEGER,
    fld_relevant_13 INTEGER,
    fld_relevant_14 INTEGER,
    fld_relevant_15 INTEGER,
    fld_relevant_16 INTEGER,
    fld_relevant_17 INTEGER,
    fld_relevant_18 INTEGER,
    fld_relevant_19 INTEGER,
    fld_relevant_20 INTEGER,
    fld_remarks VARCHAR,
    fld_request_by INTEGER,
    fld_reviewed INTEGER,
    fld_reviewed_by INTEGER,
    fld_software_id INTEGER,
    fld_status INTEGER,
    fld_test_case VARCHAR(512),
    fld_test_found VARCHAR(512),
    fld_type_id INTEGER,
    fld_unit VARCHAR(256),
    PRIMARY KEY (fld_incident_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_incident_action (
    fld_incident_id INTEGER NOT NULL,
    fld_action_id INTEGER NOT NULL,
    fld_action_owner INTEGER,
    fld_action_prescribed VARCHAR,
    fld_action_taken VARCHAR,
    fld_approved INTEGER,
    fld_approved_by INTEGER,
    fld_approved_date DATE,
    fld_closed INTEGER,
    fld_closed_by INTEGER,
    fld_closed_date DATE,
    fld_due_date DATE,
    fld_status_id INTEGER,
    PRIMARY KEY (fld_action_id),
    FOREIGN KEY(fld_incident_id) REFERENCES ramstk_incident (fld_incident_id)
);
CREATE TABLE ramstk_incident_detail (
    fld_incident_id INTEGER NOT NULL,
    fld_hardware_id INTEGER,
    fld_age_at_incident FLOAT,
    fld_cnd_nff INTEGER,
    fld_failure INTEGER,
    fld_initial_installation INTEGER,
    fld_interval_censored INTEGER,
    fld_mode_type_id INTEGER,
    fld_occ_fault INTEGER,
    fld_suspension INTEGER,
    fld_ttf FLOAT,
    fld_use_cal_time INTEGER,
    fld_use_op_time INTEGER,
    PRIMARY KEY (fld_incident_id),
    FOREIGN KEY(fld_incident_id) REFERENCES ramstk_incident (fld_incident_id)
);
CREATE TABLE ramstk_matrix (
    fld_revision_id INTEGER,
    fld_matrix_id INTEGER NOT NULL,
    fld_column_id INTEGER,
    fld_column_item_id INTEGER NOT NULL,
    fld_matrix_type VARCHAR(128),
    fld_parent_id INTEGER,
    fld_row_id INTEGER,
    fld_row_item_id INTEGER NOT NULL,
    fld_value INTEGER,
    PRIMARY KEY (fld_revision_id, fld_matrix_id, fld_column_item_id, fld_row_item_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_matrix" VALUES(1,1,1,1,'fnctn_hrdwr',0,1,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,1,1,'fnctn_hrdwr',0,1,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,1,1,'fnctn_hrdwr',0,1,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,2,2,'fnctn_hrdwr',0,2,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,2,2,'fnctn_hrdwr',0,2,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,2,2,'fnctn_hrdwr',0,2,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,3,3,'fnctn_hrdwr',0,3,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,3,3,'fnctn_hrdwr',0,3,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,3,3,'fnctn_hrdwr',0,3,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,4,4,'fnctn_hrdwr',0,4,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,4,4,'fnctn_hrdwr',0,4,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,4,4,'fnctn_hrdwr',0,4,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,5,5,'fnctn_hrdwr',0,5,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,5,5,'fnctn_hrdwr',0,5,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,5,5,'fnctn_hrdwr',0,5,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,6,6,'fnctn_hrdwr',0,6,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,6,6,'fnctn_hrdwr',0,6,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,6,6,'fnctn_hrdwr',0,6,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,7,7,'fnctn_hrdwr',0,7,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,7,7,'fnctn_hrdwr',0,7,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,7,7,'fnctn_hrdwr',0,7,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,8,8,'fnctn_hrdwr',0,8,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,8,8,'fnctn_hrdwr',0,8,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,1,8,8,'fnctn_hrdwr',0,8,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,3,'hrdwr_rqrmnt',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,2,'hrdwr_rqrmnt',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,0,4,'hrdwr_rqrmnt',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,3,'hrdwr_vldtn',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,2,'hrdwr_vldtn',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,4,'hrdwr_vldtn',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,5,'hrdwr_vldtn',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,4,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,5,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,6,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,7,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,8,0);
INSERT INTO "ramstk_matrix" VALUES(1,6,0,6,'hrdwr_vldtn',0,0,9,0);
INSERT INTO "ramstk_matrix" VALUES(1,2,1,1,'rqrmnt_hrdwr',0,1,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,2,2,'rqrmnt_hrdwr',0,1,1,1);
INSERT INTO "ramstk_matrix" VALUES(1,3,3,3,'rqrmnt_hrdwr',0,1,1,2);
INSERT INTO "ramstk_matrix" VALUES(1,3,4,4,'rqrmnt_hrdwr',0,1,1,2);
INSERT INTO "ramstk_matrix" VALUES(1,3,5,5,'rqrmnt_hrdwr',0,1,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,6,6,'rqrmnt_hrdwr',0,1,1,1);
INSERT INTO "ramstk_matrix" VALUES(1,3,7,7,'rqrmnt_hrdwr',0,1,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,8,8,'rqrmnt_hrdwr',0,1,1,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,1,1,'rqrmnt_hrdwr',0,2,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,2,2,'rqrmnt_hrdwr',0,2,2,1);
INSERT INTO "ramstk_matrix" VALUES(1,3,3,3,'rqrmnt_hrdwr',0,2,2,2);
INSERT INTO "ramstk_matrix" VALUES(1,3,4,4,'rqrmnt_hrdwr',0,2,2,2);
INSERT INTO "ramstk_matrix" VALUES(1,3,5,5,'rqrmnt_hrdwr',0,2,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,6,6,'rqrmnt_hrdwr',0,2,2,1);
INSERT INTO "ramstk_matrix" VALUES(1,3,7,7,'rqrmnt_hrdwr',0,2,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,8,8,'rqrmnt_hrdwr',0,2,2,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,1,1,'rqrmnt_hrdwr',0,3,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,2,2,'rqrmnt_hrdwr',0,3,3,1);
INSERT INTO "ramstk_matrix" VALUES(1,3,3,3,'rqrmnt_hrdwr',0,3,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,3,4,4,'rqrmnt_hrdwr',0,3,3,2);
INSERT INTO "ramstk_matrix" VALUES(1,3,5,5,'rqrmnt_hrdwr',0,3,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,6,6,'rqrmnt_hrdwr',0,3,3,1);
INSERT INTO "ramstk_matrix" VALUES(1,3,7,7,'rqrmnt_hrdwr',0,3,3,0);
INSERT INTO "ramstk_matrix" VALUES(1,3,8,8,'rqrmnt_hrdwr',0,3,3,0);

CREATE TABLE ramstk_requirement (
    fld_revision_id INTEGER,
    fld_requirement_id INTEGER NOT NULL,
    fld_derived INTEGER,
    fld_description VARCHAR,
    fld_figure_number VARCHAR(256),
    fld_owner INTEGER,
    fld_page_number VARCHAR(256),
    fld_parent_id INTEGER,
    fld_priority INTEGER,
    fld_requirement_code VARCHAR(256),
    fld_specification VARCHAR(256),
    fld_requirement_type INTEGER,
    fld_validated INTEGER,
    fld_validated_date DATE,
    fld_clarity_0 INTEGER,
    fld_clarity_1 INTEGER,
    fld_clarity_2 INTEGER,
    fld_clarity_3 INTEGER,
    fld_clarity_4 INTEGER,
    fld_clarity_5 INTEGER,
    fld_clarity_6 INTEGER,
    fld_clarity_7 INTEGER,
    fld_clarity_8 INTEGER,
    fld_complete_0 INTEGER,
    fld_complete_1 INTEGER,
    fld_complete_2 INTEGER,
    fld_complete_3 INTEGER,
    fld_complete_4 INTEGER,
    fld_complete_5 INTEGER,
    fld_complete_6 INTEGER,
    fld_complete_7 INTEGER,
    fld_complete_8 INTEGER,
    fld_complete_9 INTEGER,
    fld_consistent_0 INTEGER,
    fld_consistent_1 INTEGER,
    fld_consistent_2 INTEGER,
    fld_consistent_3 INTEGER,
    fld_consistent_4 INTEGER,
    fld_consistent_5 INTEGER,
    fld_consistent_6 INTEGER,
    fld_consistent_7 INTEGER,
    fld_consistent_8 INTEGER,
    fld_verifiable_0 INTEGER,
    fld_verifiable_1 INTEGER,
    fld_verifiable_2 INTEGER,
    fld_verifiable_3 INTEGER,
    fld_verifiable_4 INTEGER,
    fld_verifiable_5 INTEGER,
    PRIMARY KEY (fld_requirement_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_requirement" VALUES(1,1,0,'','',0,'',0,0,'REL-0001','',0,0,'2019-07-21',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "ramstk_requirement" VALUES(1,2,0,'','',0,'',0,0,'FUN-0002','',0,0,'2019-07-21',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
INSERT INTO "ramstk_requirement" VALUES(1,3,0,'','',0,'',0,0,'PRF-0003','',0,0,'2019-07-21',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

CREATE TABLE ramstk_software (
    fld_revision_id INTEGER NOT NULL,
    fld_software_id INTEGER NOT NULL,
    fld_a FLOAT,
    fld_aloc INTEGER,
    fld_am FLOAT,
    fld_application_id INTEGER,
    fld_ax INTEGER,
    fld_budget_test FLOAT,
    fld_budget_dev FLOAT,
    fld_bx INTEGER,
    fld_category_id INTEGER,
    fld_cb INTEGER,
    fld_cx INTEGER,
    fld_d FLOAT,
    fld_dc FLOAT,
    fld_dd INTEGER,
    fld_description VARCHAR(512),
    fld_development_id INTEGER,
    fld_dev_assess_type_id INTEGER,
    fld_df FLOAT,
    fld_do FLOAT,
    fld_dr FLOAT,
    fld_dr_eot INTEGER,
    fld_dr_test INTEGER,
    fld_e FLOAT,
    fld_ec FLOAT,
    fld_et FLOAT,
    fld_ev FLOAT,
    fld_ew FLOAT,
    fld_f FLOAT,
    fld_ft1 FLOAT,
    fld_ft2 FLOAT,
    fld_hloc INTEGER,
    fld_hours_dev FLOAT,
    fld_hours_test FLOAT,
    fld_level INTEGER,
    fld_loc INTEGER,
    fld_n_branches INTEGER,
    fld_n_branches_test INTEGER,
    fld_n_inputs INTEGER,
    fld_n_inputs_test INTEGER,
    fld_n_interfaces INTEGER,
    fld_n_interfaces_test INTEGER,
    fld_ncb INTEGER,
    fld_nm INTEGER,
    fld_nm_test INTEGER,
    fld_os FLOAT,
    fld_parent_id INTEGER,
    fld_phase_id INTEGER,
    fld_ren_avg FLOAT,
    fld_ren_eot FLOAT,
    fld_rpfom FLOAT,
    fld_s1 FLOAT,
    fld_s2 FLOAT,
    fld_sa FLOAT,
    fld_schedule_dev FLOAT,
    fld_schedule_test FLOAT,
    fld_sl FLOAT,
    fld_sm FLOAT,
    fld_sq FLOAT,
    fld_sr FLOAT,
    fld_st FLOAT,
    fld_sx FLOAT,
    fld_t FLOAT,
    fld_tc FLOAT,
    fld_tcl INTEGER,
    fld_te FLOAT,
    fld_test_approach INTEGER,
    fld_test_effort INTEGER,
    fld_test_path INTEGER,
    fld_test_time FLOAT,
    fld_test_time_eot FLOAT,
    fld_tm FLOAT,
    fld_um INTEGER,
    fld_wm INTEGER,
    fld_xm INTEGER,
    PRIMARY KEY (fld_software_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_software_development (
    fld_software_id INTEGER NOT NULL,
    fld_question_id INTEGER NOT NULL,
    fld_answer INTEGER,
    PRIMARY KEY (fld_question_id),
    FOREIGN KEY(fld_software_id) REFERENCES ramstk_software (fld_software_id)
);
CREATE TABLE ramstk_software_review (
    fld_software_id INTEGER NOT NULL,
    fld_question_id INTEGER NOT NULL,
    fld_answer INTEGER,
    fld_value INTEGER,
    fld_type VARCHAR(256),
    PRIMARY KEY (fld_question_id),
    FOREIGN KEY(fld_software_id) REFERENCES ramstk_software (fld_software_id)
);
CREATE TABLE ramstk_software_test (
    fld_software_id INTEGER NOT NULL,
    fld_technique_id INTEGER NOT NULL,
    fld_recommended INTEGER,
    fld_used INTEGER,
    PRIMARY KEY (fld_technique_id),
    FOREIGN KEY(fld_software_id) REFERENCES ramstk_software (fld_software_id)
);
CREATE TABLE ramstk_stakeholder (
    fld_revision_id INTEGER,
    fld_stakeholder_id INTEGER NOT NULL,
    fld_customer_rank INTEGER,
    fld_description TEXT,
    fld_group VARCHAR(128),
    fld_improvement FLOAT,
    fld_overall_weight FLOAT,
    fld_planned_rank INTEGER,
    fld_priority INTEGER,
    fld_requirement_id INTEGER,
    fld_stakeholder VARCHAR(128),
    fld_user_float_1 FLOAT,
    fld_user_float_2 FLOAT,
    fld_user_float_3 FLOAT,
    fld_user_float_4 FLOAT,
    fld_user_float_5 FLOAT,
    PRIMARY KEY (fld_stakeholder_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_stakeholder" VALUES(1,1,1,'Test Stakeholder Input','',0.0,0.0,1,1,0,'',1.0,1.0,1.0,1.0,1.0);
INSERT INTO "ramstk_stakeholder" VALUES(1,2,1,'Test Stakeholder Input 2','',0.0,0.0,1,1,0,'',1.0,1.0,1.0,1.0,1.0);
CREATE TABLE ramstk_survival (
    fld_revision_id INTEGER NOT NULL,
    fld_survival_id INTEGER NOT NULL,
    fld_hardware_id INTEGER,
    fld_description VARCHAR(512),
    fld_source_id INTEGER,
    fld_distribution_id INTEGER,
    fld_confidence FLOAT,
    fld_confidence_type_id INTEGER,
    fld_confidence_method_id INTEGER,
    fld_fit_method_id INTEGER,
    fld_rel_time FLOAT,
    fld_n_rel_points INTEGER,
    fld_n_suspensions INTEGER,
    fld_n_failures INTEGER,
    fld_scale_ll FLOAT,
    fld_scale FLOAT,
    fld_scale_ul FLOAT,
    fld_shape_ll FLOAT,
    fld_shape FLOAT,
    fld_shape_ul FLOAT,
    fld_location_ll FLOAT,
    fld_location FLOAT,
    fld_location_ul FLOAT,
    fld_variance_1 FLOAT,
    fld_variance_2 FLOAT,
    fld_variance_3 FLOAT,
    fld_covariance_1 FLOAT,
    fld_covariance_2 FLOAT,
    fld_covariance_3 FLOAT,
    fld_mhb FLOAT,
    fld_lp FLOAT,
    fld_lr FLOAT,
    fld_aic FLOAT,
    fld_bic FLOAT,
    fld_mle FLOAT,
    fld_start_time FLOAT,
    fld_start_date DATE,
    fld_end_date DATE,
    fld_nevada_chart INTEGER,
    PRIMARY KEY (fld_survival_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_survival_data (
    fld_survival_id INTEGER NOT NULL,
    fld_record_id INTEGER NOT NULL,
    fld_name VARCHAR(512),
    fld_source_id INTEGER,
    fld_failure_date DATE,
    fld_left_interval FLOAT,
    fld_right_interval FLOAT,
    fld_status_id INTEGER,
    fld_quantity INTEGER,
    fld_tbf FLOAT,
    fld_mode_type_id INTEGER,
    fld_nevada_chart INTEGER,
    fld_ship_date DATE,
    fld_number_shipped INTEGER,
    fld_return_date DATE,
    fld_number_returned INTEGER,
    fld_user_float_1 FLOAT,
    fld_user_float_2 FLOAT,
    fld_user_float_3 FLOAT,
    fld_user_integer_1 INTEGER,
    fld_user_integer_2 INTEGER,
    fld_user_integer_3 INTEGER,
    fld_user_string_1 VARCHAR(512),
    fld_user_string_2 VARCHAR(512),
    fld_user_string_3 VARCHAR(512),
    PRIMARY KEY (fld_record_id),
    FOREIGN KEY(fld_survival_id) REFERENCES ramstk_survival (fld_survival_id)
);
CREATE TABLE ramstk_unit (
    fld_unit_id INTEGER NOT NULL,
    fld_code VARCHAR(256),
    fld_description VARCHAR(512),
    fld_type VARCHAR(256),
    PRIMARY KEY (fld_unit_id)
);
CREATE TABLE ramstk_validation (
    fld_revision_id INTEGER,
    fld_validation_id INTEGER NOT NULL,
    fld_acceptable_maximum FLOAT,
    fld_acceptable_mean FLOAT,
    fld_acceptable_minimum FLOAT,
    fld_acceptable_variance FLOAT,
    fld_confidence FLOAT,
    fld_cost_average FLOAT,
    fld_cost_ll FLOAT,
    fld_cost_maximum FLOAT,
    fld_cost_mean FLOAT,
    fld_cost_minimum FLOAT,
    fld_cost_ul FLOAT,
    fld_cost_variance FLOAT,
    fld_date_end DATE,
    fld_date_start DATE,
    fld_description VARCHAR,
    fld_measurement_unit VARCHAR(256),
    fld_name VARCHAR(256),
    fld_status FLOAT,
    fld_type VARCHAR(256),
    fld_task_specification VARCHAR(512),
    fld_time_average FLOAT,
    fld_time_ll FLOAT,
    fld_time_maximum FLOAT,
    fld_time_mean FLOAT,
    fld_time_minimum FLOAT,
    fld_time_ul FLOAT,
    fld_time_variance FLOAT,
    PRIMARY KEY (fld_validation_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id) ON DELETE CASCADE
);
INSERT INTO "ramstk_validation" VALUES(1,1,0.0,0.0,0.0,0.0,95.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'2019-08-20','2019-07-21','Test Validation','','',0.0,'','',0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_validation" VALUES(1,2,0.0,0.0,0.0,0.0,95.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'2019-08-20','2019-07-21','Test Validation','','',0.0,'','',0.0,0.0,0.0,0.0,0.0,0.0,0.0);
INSERT INTO "ramstk_validation" VALUES(1,3,0.0,0.0,0.0,0.0,95.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'2019-08-20','2019-07-21','Test Validation','','',0.0,'','',0.0,0.0,0.0,0.0,0.0,0.0,0.0);

CREATE TABLE ramstk_test (
    fld_revision_id INTEGER NOT NULL,
    fld_test_id INTEGER NOT NULL,
    fld_assess_model_id INTEGER,
    fld_attachment VARCHAR(512),
    fld_avg_fef FLOAT,
    fld_avg_growth FLOAT,
    fld_avg_ms FLOAT,
    fld_chi_square FLOAT,
    fld_confidence FLOAT,
    fld_consumer_risk FLOAT,
    fld_cramer_vonmises FLOAT,
    fld_cum_failures INTEGER,
    fld_cum_mean FLOAT,
    fld_cum_mean_ll FLOAT,
    fld_cum_mean_se FLOAT,
    fld_cum_mean_ul FLOAT,
    fld_cum_time FLOAT,
    fld_description VARCHAR,
    fld_grouped INTEGER,
    fld_group_interval FLOAT,
    fld_inst_mean FLOAT,
    fld_inst_mean_ll FLOAT,
    fld_inst_mean_se FLOAT,
    fld_inst_mean_ul FLOAT,
    fld_mg FLOAT,
    fld_mgp FLOAT,
    fld_n_phases INTEGER,
    fld_name VARCHAR(512),
    fld_plan_model_id INTEGER,
    fld_prob FLOAT,
    fld_producer_risk FLOAT,
    fld_scale FLOAT,
    fld_scale_ll FLOAT,
    fld_scale_se FLOAT,
    fld_scale_ul FLOAT,
    fld_shape FLOAT,
    fld_shape_ll FLOAT,
    fld_shape_se FLOAT,
    fld_shape_ul FLOAT,
    fld_tr FLOAT,
    fld_ttt FLOAT,
    fld_ttff FLOAT,
    fld_type_id INTEGER,
    PRIMARY KEY (fld_test_id),
    FOREIGN KEY(fld_revision_id) REFERENCES ramstk_revision (fld_revision_id)
);
CREATE TABLE ramstk_growth_test (
    fld_test_id INTEGER NOT NULL,
    fld_phase_id INTEGER NOT NULL,
    fld_i_mi FLOAT,
    fld_i_mf FLOAT,
    fld_i_ma FLOAT,
    fld_i_num_fails INTEGER,
    fld_p_growth_rate FLOAT,
    fld_p_ms FLOAT,
    fld_p_fef_avg FLOAT,
    fld_p_prob FLOAT,
    fld_p_mi FLOAT,
    fld_p_mf FLOAT,
    fld_p_ma FLOAT,
    fld_test_time FLOAT,
    fld_p_num_fails INTEGER,
    fld_p_start_date DATE,
    fld_p_end_date DATE,
    fld_p_weeks FLOAT,
    fld_test_units INTEGER,
    fld_p_tpu FLOAT,
    fld_p_tpupw FLOAT,
    fld_o_growth_rate FLOAT,
    fld_o_ms FLOAT,
    fld_o_fef_avg FLOAT,
    fld_o_mi FLOAT,
    fld_o_mf FLOAT,
    fld_o_ma FLOAT,
    fld_o_test_time FLOAT,
    fld_o_num_fails INTEGER,
    fld_o_ttff FLOAT,
    PRIMARY KEY (fld_phase_id),
    FOREIGN KEY(fld_test_id) REFERENCES ramstk_test (fld_test_id)
);
