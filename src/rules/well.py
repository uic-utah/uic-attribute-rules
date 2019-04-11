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

return iif(isempty($feature.wellclass), null, generateId($feature.wellclass));
'''

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

return getAttributeFromLargestArea($feature, set, field);
'''

constrain_wellclass = '''if (isempty($feature.wellclass)) {
    return true;
}

iif (indexof([1,3,4,5,6], $feature.wellclass) > -1, true, {
    'errorMessage': 'Acceptable well classes are 1, 3, 4, 5, or 6. Input: ' + $feature.wellclass
})'''

constrain_yes_no_unknown = '''if (isempty({0})) {{
    return true;
}}
iif (indexof(['Y', 'N', 'U'], {0}) > -1, true, {{
    'errorMessage': 'Acceptable values are Y, N, U. Input: ' + {0}
}})'''

extract_elevation = '''var set = FeatureSetByName($datastore, 'DEM', ['Feet'], true);

var items = intersects(set, $feature);

var counts = count(items);

return counts;
'''

GUID = Constant('Well Guid', 'GUID', 'Well.Guid', 'Guid()')
ID = Calculation('Well Id', 'WellId', 'Well.Id', create_id)
ID.triggers = [config.triggers.update]
FACILITY = Calculation('Facility Fk', 'Facility_Fk', 'Well.Facility_FK', extract_facility)
AUTHORIZATION = None

CLASS = Constraint('Well Class', 'Well.Class', constrain_wellclass)
CLASS.triggers = [config.triggers.insert, config.triggers.update]

SUBCLASS = None
# TODO: rasters are not supported
# ELEVATION = Calculation('Well Elevation', 'SurfaceElevation', 'Well.SurfaceElevation', extract_elevation)

HIGHPRIORITY = Constraint('High Priority', 'Well.HighPriority', constrain_yes_no_unknown.format('$feature.highpriority'))
HIGHPRIORITY.triggers = [config.triggers.update]

INJECTION_AQUIFER_EXEMPT = Constraint(
    'Injection Aquifer Exempt', 'Well.InjectionAquiferExempt', constrain_yes_no_unknown.format('$feature.InjectionAquiferExempt')
)
INJECTION_AQUIFER_EXEMPT.triggers = [config.triggers.update]
