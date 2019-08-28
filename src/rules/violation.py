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

type_domain_constraint = Constraint(
    'Violation Type', 'ViolationType', common.constrain_to_domain('ViolationType', allow_null=True, domain='UICViolationTypeDomain')
)

type_domain_constraint_update = Constraint(
    'Violation Type', 'ViolationType.update', common.constrain_to_domain('ViolationType', allow_null=False, domain='UICViolationTypeDomain')
)
type_domain_constraint_update.triggers = [config.triggers.update]

contamination_domain_constraint = Constraint(
    'Contamination', 'USDWContamination', common.constrain_to_domain('USDWContamination', allow_null=True, domain='UICYesNoUnknownDomain')
)

contamination_domain_constraint_update = Constraint(
    'Contamination', 'USDWContamination.update', common.constrain_to_domain('USDWContamination', allow_null=False, domain='UICYesNoUnknownDomain')
)
contamination_domain_constraint_update.triggers = [config.triggers.insert, config.triggers.update]

endanger_domain_constraint = Constraint('Endanger', 'Endanger', common.constrain_to_domain('Endanger', allow_null=True, domain='UICYesNoUnknownDomain'))

endanger_domain_constraint_update = Constraint(
    'Endanger', 'Endanger.update', common.constrain_to_domain('Endanger', allow_null=False, domain='UICYesNoUnknownDomain')
)
endanger_domain_constraint_update.triggers = [config.triggers.update]

contamination_calculation = Calculation('Significant Non Compliance', 'SignificantNonCompliance', load_rule_for(FOLDER, 'significantNonComplianceCalculation'))
contamination_calculation.editable = config.editable.no
contamination_calculation.triggers = [config.triggers.insert, config.triggers.update]

noncompliance_domain_constraint = Constraint(
    'SignificantNonCompliance', 'SignificantNonCompliance',
    common.constrain_to_domain('SignificantNonCompliance', allow_null=True, domain='UICYesNoUnknownDomain')
)

noncompliance_domain_constraint_update = Constraint(
    'SignificantNonCompliance', 'SignificantNonCompliance.update',
    common.constrain_to_domain('SignificantNonCompliance', allow_null=False, domain='UICYesNoUnknownDomain')
)
noncompliance_domain_constraint_update.triggers = [config.triggers.insert, config.triggers.update]

comment_constraint = Constraint('Comments required for other', 'Comments', load_rule_for(FOLDER, 'commentConstraint'))
comment_constraint.triggers = [config.triggers.insert, config.triggers.update]

violation_constraint = Constraint('Violation Type For Facility vs Well', 'FacilityWellTypes', load_rule_for(FOLDER, 'facilityWellTypesConstraint'))
violation_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    type_domain_constraint_update,
    contamination_domain_constraint,
    contamination_domain_constraint_update,
    endanger_domain_constraint,
    endanger_domain_constraint_update,
    noncompliance_domain_constraint,
    noncompliance_domain_constraint_update,
    contamination_calculation,
    comment_constraint,
    violation_constraint,
]
