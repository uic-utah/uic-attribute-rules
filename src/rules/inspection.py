#!/usr/bin/env python
# * coding: utf8 *
'''
inspection.py
A module that has the UICInspection rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

constrain_to_one_parent = '''if (!haskey($feature, 'facility_fk') || !haskey($feature, 'well_fk')) {
    return true;
}

return iif (isempty($feature.facility_fk) && isempty($feature.well_fk) || (!isempty($feature.facility_fk) && !isempty($feature.well_fk)), {
    'errorMessage': 'an inspection record must have either, but not both, a Facility_FK or a Well_FK'
}, true);'''

constrain_to_facility = '''if (!haskey($feature, 'inspectiontype') || !haskey($feature, 'facility_fk') || isempty($feature.inspectiontype)) {
    return true;
}

if (lower(domaincode($feature, 'inspectiontype', $feature.inspectiontype)) != 'nw') {
    return true;
}

return iif (isempty($feature.facility_fk), {
    'errorMessage': 'If InspectionType coded value is NW, then there must be a Facility_FK but no Well_FK'
}, true);'''

TABLE = 'UICInspection'

GUID = Constant('Inspection Guid', 'GUID', 'Inspection.Guid', 'GUID()')

TYPE_DOMAIN = Constraint('Inspection Type', 'Inspection.Type', common.constrain_to_domain('InspectionType'))
TYPE_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]

ASSISTANCE_DOMAIN = Constraint('Inspection Assistance', 'Inspection.Assistance', common.constrain_to_domain('InspectionAssistance'))
ASSISTANCE_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]

DEFICIENCY_DOMAIN = Constraint('Inspection Deficiency', 'Inspection.Deficiency', common.constrain_to_domain('InspectionDeficiency'))
DEFICIENCY_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]

FOREIGN_KEY = Constraint('One parent relation', 'FacilityFk.WellFk', constrain_to_one_parent)
FOREIGN_KEY.triggers = [config.triggers.insert, config.triggers.update]

FACILITY_ONLY = Constraint('NW for facility only', 'FacilityOnly.InspectionType', constrain_to_facility)
FACILITY_ONLY.triggers = [config.triggers.insert, config.triggers.update]
