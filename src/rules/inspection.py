#!/usr/bin/env python
# * coding: utf8 *
'''
inspection.py
A module that has the UICInspection rules
'''

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = 'UICInspection'
FOLDER = 'inspection'

guid_constant = Constant('Inspection Guid', 'GUID', 'GUID()')

type_domain_constraint = Constraint('Inspection Type', 'InspectionType', common.constrain_to_domain('InspectionType', domain='UICInspectionTypeDomain'))
type_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

assistance_domain_constraint = Constraint(
    'Inspection Assistance', 'InspectionAssistance', common.constrain_to_domain('InspectionAssistance', domain='UICComplianceAssistanceDomain')
)
assistance_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

deficiency_domain_constraint = Constraint(
    'Inspection Deficiency', 'InspectionDeficiency', common.constrain_to_domain('InspectionDeficiency', domain='UICDeficiencyDomain')
)
deficiency_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

foreign_key_constraint = Constraint('One parent relation', 'Single Parent', load_rule_for(FOLDER, 'oneFKConstraint'))
foreign_key_constraint.triggers = [config.triggers.insert, config.triggers.update]

facility_only_constraint = Constraint('NW for facility only', 'InspectionType', load_rule_for(FOLDER, 'typeConstraint'))
facility_only_constraint.triggers = [config.triggers.insert, config.triggers.update]

inspection_date_constraint = Constraint('Well operating status date', 'InspectionDate', load_rule_for(FOLDER, 'dateConstraint'))
inspection_date_constraint.triggers = [config.triggers.insert, config.triggers.update]

deficiency_constraint = Constraint('No Deficiency', 'InspectionDeficiency', load_rule_for(FOLDER, 'deficiencyConstraint'))
deficiency_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    assistance_domain_constraint,
    deficiency_domain_constraint,
    foreign_key_constraint,
    facility_only_constraint,
    inspection_date_constraint,
    deficiency_constraint,
]
