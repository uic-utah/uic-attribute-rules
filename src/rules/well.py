#!/usr/bin/env python
# * coding: utf8 *
'''
well.py
A module that holds the rules for uicwells
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint

TABLE = 'UICWell'

create_id = '''function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return null;
    }

    if (counts == 1) {
        var result = first(items);

        return result[field];
    }

    var largest = -1;
    var result;

    for (var item in items) {
        var size = area(intersection(item, feat));

        if (size > largest) {
            largest = size;
            result = item[field];
        }
    }

    return result;
}

function generateId(class) {
    var field = 'FIPS';
    var set = FeatureSetByName($datastore, 'Counties', [field], true);

    // there is a bug so the $feature can't be used.
    // TODO: replace with $feature when bug is resolved
    var geom = point({"x" : 423117, "y" : 4393267.15, "spatialReference" : {"wkid" : 26912}});
    var fips = getAttributeFromLargestArea(geom, set, field);

    return 'UTU' + fips + class + upper(mid($feature.guid, 29, 8));
}

var keys = ['wellclass', 'guid'];

for (var key in keys) {
    if (!haskey($feature, keys[key])) {
        return null;
    }
}

return iif(isempty($feature.wellclass), null, generateId($feature.wellclass));'''

extract_facility = '''function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return null;
    }

    if (counts == 1) {
        var result = first(items);

        return result[field];
    }

    var largest = -1;
    var result;

    for (var item in items) {
        var size = area(intersection(item, feat));

        if (size > largest) {
            largest = size;
            result = item[field];
        }
    }

    return result;
}

var field = 'Guid';
var set = FeatureSetByName($datastore, 'UICFacility', [field], true);

if (!haskey($feature, field)) {
    return null;
}

return getAttributeFromLargestArea($feature, set, field);'''

constrain_wellclass = '''if (!haskey($feature, 'wellclass') || isempty($feature.wellclass)) {
    return true;
}

return iif (isempty(domainname($feature, 'wellclass', $feature.wellclass)), {
    'errorMessage': 'Acceptable well classes are 1, 3, 4, 5, or 6. Input: ' + $feature.wellclass
}, true)'''

constrain_subclass = '''if (!haskey($feature, 'wellsubclass') || !haskey($feature, 'wellclass')) {
    return true;
}

if (isempty($feature.wellclass)) {
    return true;
}

if (isempty($feature.wellsubclass)) {
    return {
        'errorMessage': 'Well subclass is required'
    }
}

return iif (left($feature.wellsubclass, 1) == text($feature.wellclass), true, {
    'errorMessage': 'Well sub class (' + text($feature.wellsubclass) + ') is not associated with the well class (' + text($feature.wellclass) + ')'
})'''

constrain_yes_no_unknown = '''if (!haskey($feature, '{0}') || isempty($feature.{0})) {{
    return true;
}}

return iif (isempty(domainname($feature, '{0}', $feature.{0})), {{
    'errorMessage': 'Acceptable values are Y, N, U. Input: ' + $feature.{0}
}}, true)'''

extract_elevation = '''var set = FeatureSetByName($datastore, 'DEM', ['Feet'], true);

var items = intersects(set, $feature);

var counts = count(items);

return counts;'''

#: if well class = 1, NMPS needs a value
constrain_class_one_wells = '''var keys = ['wellsubclass'];
// if well class is empty, no worries
for (var index in keys) {
    if (!haskey($feature, keys[index]) || isempty($feature[keys[index]])) {
        return true;
    }
}

// if well class is not 1001 or 1003, no worries
if (indexof([1001, 1003], $feature.wellsubclass) == -1) {
    return true;
}

return iif (isempty($feature.nomigrationpetstatus), {
    'errorMessage': 'Class I wells require a NoMigrationPetStatus'
}, true);'''

constrain_highpriority = '''if (!haskey($feature, 'highpriority') || !haskey($feature, 'wellclass')) {
    return true;
}

if ($feature.wellclass == 5) {
    return iif (isempty(domainname($feature, 'highpriority', $feature.highpriority)), {
            'errorMessage': 'Class V wells require a high priority value'
        }, true);
}

if (isempty($feature.highpriority)) {
    return true;
}

return iif (isempty(domainname($feature, 'highpriority', $feature.highpriority)), {
    'errorMessage': 'Acceptable values for high priority are C, N, U. Input: ' + $feature.highpriority
}, true);'''

constrain_facility_type = '''if (!haskey($feature, 'classifacilitytype') || !haskey($feature, 'wellclass')) {
    return true;
}

if ($feature.wellclass == 1) {
    return iif (isempty(domainname($feature, 'classifacilitytype', $feature.classifacilitytype)), {
            'errorMessage': 'Class I wells require a facility type value'
        }, true);
}

if (isempty($feature.classifacilitytype)) {
    return true;
}

return iif (isempty(domainname($feature, 'classifacilitytype', $feature.classifacilitytype)), {
    'errorMessage': 'Acceptable values for facility type are C, N, U. Input: ' + $feature.classifacilitytype
}, true);'''

constrain_remediation = '''if (!haskey($feature, 'remediationprojecttype') || isempty($feature.remediationprojecttype)) {
    return true;
}

if (($feature.remediationprojecttype > 0 && $feature.remediationprojecttype < 9) || $feature.remediationprojecttype == 999){
    return true;
}

return {
    'errorMessage': 'Acceptable values for remediation project type are 1-8 and 999. Input: ' + $feature.remediationprojecttype
}'''

constrain_swpz = '''if (!haskey($feature, 'wellswpz') || isempty($feature.wellswpz)) {
    return true;
}

return iif (isempty(domainname($feature, 'wellswpz', $feature.wellswpz)), {
    'errorMessage': 'Acceptable values for SWPZ types are Y, S, N, U. Input: ' + $feature.wellswpz
}, true);'''

GUID = Constant('Well Guid', 'GUID', 'Well.Guid', 'Guid()')
ID = Calculation('Well Id', 'WellId', 'Well.Id', create_id)
ID.triggers = [config.triggers.insert, config.triggers.update]
FACILITY = Calculation('Facility Fk', 'Facility_Fk', 'Well.Facility_FK', extract_facility)
AUTHORIZATION = None

CLASS = Constraint('Well Class', 'Well.Class', constrain_wellclass)
CLASS.triggers = [config.triggers.insert, config.triggers.update]

SUBCLASS = Constraint('Well Subclass', 'Well.Subclass', constrain_subclass)
SUBCLASS.triggers = [config.triggers.insert, config.triggers.update]

# TODO: rasters are not supported
# ELEVATION = Calculation('Well Elevation', 'SurfaceElevation', 'Well.SurfaceElevation', extract_elevation)

HIGHPRIORITY = Constraint('High Priority', 'Well.HighPriority', constrain_highpriority)
HIGHPRIORITY.triggers = [config.triggers.insert, config.triggers.update]

INJECTION_AQUIFER_EXEMPT = Constraint('Injection Aquifer Exempt', 'Well.InjectionAquiferExempt', constrain_yes_no_unknown.format('InjectionAquiferExempt'))
INJECTION_AQUIFER_EXEMPT.triggers = [config.triggers.update]

NO_MIGRATION_PET_STATUS = Constraint('No Migration Pet Status', 'Well.NoMigrationPetStatus', constrain_class_one_wells)
NO_MIGRATION_PET_STATUS.triggers = [config.triggers.insert, config.triggers.update]

FACILITY_TYPE = Constraint('Class I Facility Type', 'Well.ClassIFacilityType', constrain_facility_type)
FACILITY_TYPE.triggers = [config.triggers.insert, config.triggers.update]

REMEDIATION_TYPE = Constraint('Remediation Project Type', 'Well.RemediationProjectType', constrain_remediation)
REMEDIATION_TYPE.triggers = [config.triggers.insert, config.triggers.update]

SWPZ = Constraint('Well SWPZ', 'Well.WellSQPZ', constrain_swpz)
SWPZ.triggers = [config.triggers.insert, config.triggers.update]
