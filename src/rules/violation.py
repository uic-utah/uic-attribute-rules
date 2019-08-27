#!/usr/bin/env python
# * coding: utf8 *
'''
violation.py
A module that has the UICViolation rules
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = 'UICViolation'
FOLDER = 'violation'

guid_constant = Constant('Violation Guid', 'GUID', 'GUID()')

type_domain_constraint = Constraint('Violation Type', 'Violation.Type', common.constrain_to_domain('ViolationType', domain='UICViolationTypeDomain'))
type_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

contamination_domain_constraint = Constraint(
    'Contamination', 'Violation.Contamination', common.constrain_to_domain('USDWContamination', domain='UICYesNoUnknownDomain')
)
contamination_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

contamination_calculation = Calculation(
    'Significant Non Compliance', 'SignificantNonCompliance', 'Violation.SignificantNonCompliance',
    load_rule_for(FOLDER, 'significantNonComplianceCalculation')
)
contamination_calculation.editable = config.editable.no
contamination_calculation.triggers = [config.triggers.insert, config.triggers.update]

endanger_domain_constraint = Constraint('Endanger', 'Violation.Endanger', common.constrain_to_domain('Endanger', domain='UICYesNoUnknownDomain'))
endanger_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

noncompliance_domain_constraint = Constraint(
    'SignificantNonCompliance', 'Violation.SignificantNonCompliance', common.constrain_to_domain('SignificantNonCompliance', domain='UICYesNoUnknownDomain')
)
noncompliance_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

comment_constraint = Constraint('Comments', 'Violation.Comments', load_rule_for(FOLDER, 'commentConstraint'))
comment_constraint.triggers = [config.triggers.insert, config.triggers.update]

violation_constraint = Constraint('Violation Type For Facility vs Well', 'Violation.FacilityWellTypes', load_rule_for(FOLDER, 'facilityWellTypesConstraint'))
violation_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    contamination_domain_constraint,
    contamination_calculation,
    endanger_domain_constraint,
    noncompliance_domain_constraint,
    comment_constraint,
    violation_constraint,
]
