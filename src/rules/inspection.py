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

TABLE = 'UICInspection'

GUID = Constant('Inspection Guid', 'GUID', 'Inspection.Guid', 'GUID()')

TYPE = Constraint('Inspection Type', 'Inspection.Type', common.constrain_to_domain('InspectionType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

ASSISTANCE = Constraint('Inspection Assistance', 'Inspection.Assistance', common.constrain_to_domain('InspectionAssistance'))
ASSISTANCE.triggers = [config.triggers.insert, config.triggers.update]

DEFICIENCY = Constraint('Inspection Deficiency', 'Inspection.Deficiency', common.constrain_to_domain('InspectionDeficiency'))
DEFICIENCY.triggers = [config.triggers.insert, config.triggers.update]

FOREIGN_KEY = Constraint('One parent relation', 'FacilityFk.WellFk', constrain_to_one_parent)
FOREIGN_KEY.triggers = [config.triggers.insert, config.triggers.update]
