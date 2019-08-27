#!/usr/bin/env python
# * coding: utf8 *
'''
well.py
A module that holds the rules for uicwells
'''

from . import common
from config import config
from services.loader import load_rule_for
from models.ruletypes import Calculation, Constant, Constraint

TABLE = 'UICWell'
FOLDER = 'well'

guid_constant = Constant('Well Guid', 'GUID', 'Guid()')

id_calculation = Calculation('Well Id', 'WellId', 'Well.Id', load_rule_for(FOLDER, 'idCalculation'))
id_calculation.triggers = [config.triggers.insert, config.triggers.update]
id_calculation.editabe = config.editable.no

facility_calculation = Calculation('Facility Fk', 'Facility_Fk', 'Well.Facility_FK', load_rule_for(FOLDER, 'facilityCalculation'))

class_constraint = Constraint('Well Class', 'Well.Class', load_rule_for(FOLDER, 'classConstraint'))
class_constraint.triggers = [config.triggers.insert, config.triggers.update]

subclass_constraint = Constraint('Well Subclass', 'Well.Subclass', load_rule_for(FOLDER, 'subClassConstraint'))
subclass_constraint.triggers = [config.triggers.insert, config.triggers.update]

highpriority_constraint = Constraint('High Priority', 'Well.HighPriority', load_rule_for(FOLDER, 'highPriorityConstraint'))
highpriority_constraint.triggers = [config.triggers.insert, config.triggers.update]

injection_aquifer_constraint = Constraint(
    'Injection Aquifer Exempt', 'Well.InjectionAquiferExempt',
    common.constrain_to_domain('InjectionAquiferExempt', allow_null=False, domain='UICYesNoUnknownDomain')
)
injection_aquifer_constraint.triggers = [config.triggers.insert, config.triggers.update]

no_migration_pet_status_constraint = Constraint('No Migration Pet Status', 'Well.NoMigrationPetStatus', load_rule_for(FOLDER, 'noMigrationPetStatusConstraint'))
no_migration_pet_status_constraint.triggers = [config.triggers.insert, config.triggers.update]

facility_type_constraint = Constraint('Class I Facility Type', 'Well.ClassIFacilityType', load_rule_for(FOLDER, 'facilityTypeConstraint'))
facility_type_constraint.triggers = [config.triggers.insert, config.triggers.update]

remediation_type_constraint = Constraint('Remediation Project Type', 'Well.RemediationProjectType', load_rule_for(FOLDER, 'remediationConstraint_insert'))

remediation_type_constraint_update = Constraint(
    'Remediation Project Type', 'Well.RemediationProjectType.update', load_rule_for(FOLDER, 'remediationConstraint_update')
)
remediation_type_constraint_update.triggers = [config.triggers.update]

swpz_constraint = Constraint('Well SWPZ', 'Well.WellSWPZ', load_rule_for(FOLDER, 'swpzConstraint_insert'))

swpz_constraint_update = Constraint('Well SWPZ', 'Well.WellSWPZ.update', load_rule_for(FOLDER, 'swpzConstraint_update'))
swpz_constraint_update.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    id_calculation,
    facility_calculation,
    class_constraint,
    subclass_constraint,
    highpriority_constraint,
    injection_aquifer_constraint,
    no_migration_pet_status_constraint,
    facility_type_constraint,
    remediation_type_constraint,
    remediation_type_constraint_update,
    swpz_constraint,
    swpz_constraint_update,
]
