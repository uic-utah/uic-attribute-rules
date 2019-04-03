#!/usr/bin/env python
# * coding: utf8 *
'''
well.py
A module that holds the rules for uicwells
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint

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

WELL_GUID = Constant('Well Guid', 'GUID', 'Well.Guid', 'Guid()')
WELL_ID = Calculation('Well Id', 'WellId', 'Well.Id', create_id)
WELL_ID.triggers = [config.triggers.update]
WELL_FACILITY = Calculation('Facility Fk', 'Facility_Fk', 'Well.Facility_FK', extract_facility)
WELL_AUTHORIZATION = None
WELL_CLASS = None
WELL_SUBCLASS = None
WELL_ELEVATION = None
WELL_HIGHPRIORITY = None
WELL_YESNO = None
