#!/usr/bin/env python
# * coding: utf8 *
'''
violation.py
A module that has the UICViolation rules
'''

from . import common
from config import config
from models.ruletypes import Calculation, Constant, Constraint

constrain_other_comment = '''if (!haskey($feature, 'ViolationType') || !haskey($feature, 'comments')) {
    return true;
}

if (isempty($feature.ViolationType) || lower(domaincode($feature, 'ViolationType', $feature.violationtype)) != 'ot') {
    return true;
}

return iif (isempty($feature.comments), {
    'errorMessage': 'When Violation Type is OT, a comment is required'
}, true);'''

set_yes_if_yes = '''if (!haskey($feature, 'USDWContamination') || isempty($feature.USDWContamination)) {
    return;
}

if (lower(domainname($feature, 'USDWContamination')) != 'yes') {
    return;
}

return 'Y'; '''

constrain_facility_and_well_types = '''if (!haskey($feature, 'ViolationType') || !haskey($feature, 'Well_FK') || !haskey($feature, 'Facility_FK')) {
    return true;
}

var facilityViolations = ['OM', 'MR', 'FO', 'FA', 'FI', 'FR', 'OT'];
var wellViolations = ['UI', 'OM', 'PA', 'MR', 'IP', 'FO', 'FA', 'FR', 'MI', 'MO', 'OT'];

if (!isempty($feature.well_fk)) {
    return iif (indexof(wellViolations, $feature.violationtype) == -1, {
        'errorMessage': 'Acceptable well violation types: ' + wellViolations
    }, true);
}

if (!isempty($feature.facility_fk)) {
    return iif (indexof(facilityViolations, $feature.violationtype) == -1, {
        'errorMessage': 'Acceptable facility violation types: ' + facilityViolations
    }, true);
}'''

TABLE = 'UICViolation'

GUID = Constant('Violation Guid', 'GUID', 'Violation.Guid', 'GUID()')

TYPE = Constraint('Violation Type', 'Violation.Type', common.constrain_to_domain('ViolationType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

CONTAMINATION = Constraint('Contamination', 'Violation.Contamination', common.constrain_to_domain('USDWContamination'))
CONTAMINATION.triggers = [config.triggers.insert, config.triggers.update]

CONTAMINATION_CALC = Calculation('Significant Non Compliance', 'SignificantNonCompliance', 'Violation.SignificantNonCompliance', set_yes_if_yes)
CONTAMINATION_CALC.triggers = [config.triggers.insert, config.triggers.update]

ENDANGER = Constraint('Endanger', 'Violation.Endanger', common.constrain_to_domain('Endanger'))
ENDANGER.triggers = [config.triggers.insert, config.triggers.update]

NONCOMPLIANCE = Constraint('SignificantNonCompliance', 'Violation.SignificantNonCompliance', common.constrain_to_domain('SignificantNonCompliance'))
NONCOMPLIANCE.triggers = [config.triggers.insert, config.triggers.update]

COMMENT = Constraint('Comments', 'Violation.Comments', constrain_other_comment)
COMMENT.triggers = [config.triggers.insert, config.triggers.update]

VIOLATIONS = Constraint('Violation Type For Facility vs Well', 'Violation.FacilityWellTypes', constrain_facility_and_well_types)
VIOLATIONS.triggers = [config.triggers.insert, config.triggers.update]
