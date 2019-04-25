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

var code = lower(domaincode($feature, 'inspectiontype', $feature.inspectiontype));
if (code != 'nw' && code != 'fi') {
    return true;
}

return iif (isempty($feature.facility_fk), {
    'errorMessage': 'If InspectionType coded value is NW, then there must be a Facility_FK but no Well_FK'
}, true);'''

constrain_inspection_date = '''if (!haskey($feature, 'inspectiondate') || !haskey($feature, 'well_fk') || isempty($feature.inspectiondate)) {
    return true;
}

if (isempty($feature.well_fk)) {
    return true;
}

var well = $feature.well_fk;
var statusset = featuresetbyname($datastore, 'UICWellOperatingStatus', ['OperatingStatusDate'], false);

var statuses = filter(statusset, 'well_fk=@well');

if (isempty(status)) {
    return true;
}

var earliestDate = date();

for (var status in statuses) {
    if (status.operatingstatusdate < earliestDate) {
        earliestDate = status.operatingstatusdate;
    }
}

return iif ($feature.inspectiondate < earliestDate, {
    'errorMessage': 'If the Inspection record is associated with a Well, the InspectionDate must be equal' +
                    'to or later than the earliest OperatingStatusDate associated with the Well.'
}, true);'''

constrain_correction = '''if (!haskey($feature, 'inspectiondeficiency') || isempty($feature.inspectiondeficiency)) {
    return true;
}

var code = domaincode($feature, 'inspectiondeficiency', $feature.inspectiondeficiency);

if (indexof(['NO', 'OS'], code) > -1) {
    return true;
}

var correctionset = featuresetbyname($datasource, 'uiccorrection', ['inspection_fk'], false);

var pk = $feature.guid;
var corrections = filter(correctionset, 'inspection_fk=@pk');

return iif (isempty(corrections), {
    'errorMessage': "If InspectionDeficiency is anything other than 'No Deficiency' or 'Deficiency Not Observed'" +
                    'there must be a Correction record associated with the Inspection record.'
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

INSPECTION_DATE = Constraint('Well operating status date', 'Inspection.InspectionDate', constrain_inspection_date)
INSPECTION_DATE.triggers = [config.triggers.insert, config.triggers.update]

CORRECTION = Constraint('No Deficiency', 'Inspection.InspectionDeficiency', constrain_correction)
CORRECTION.triggers = [config.triggers.insert, config.triggers.update]
