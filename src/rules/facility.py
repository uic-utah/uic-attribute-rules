#!/usr/bin/env python
# * coding: utf8 *
'''
facility.py
A module that creates attribute rules for the UICFacility table
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint

extract_fips = '''var set = FeatureSetByName($datastore, 'Counties')
function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat)
    var counts = count(items);

    if (counts == 0) {
        return { 'errorMessage': 'No intersection found' };
    }

    if (counts == 1) {
        var result = first(items)

        return result[field]
    }

    var largest = -1
    var result

    for (var item in items) {
        var size = area(intersection(item, feat))

        if (size > largest) {
            largest = size
            result = item[field]
        }
    }

    return result
}

var fips = getAttributeFromLargestArea($feature, set, 'FIPS');

return iif(isnan(number('490' + fips)), null, number('490' + fips));
'''

extract_city = '''var set = FeatureSetByName($datastore, 'Municipalities')
function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat)
    var counts = count(items);

    if (counts == 0) {
        return null;
    }

    if (counts == 1) {
        var result = first(items)

        return result[field]
    }

    var largest = -1
    var result

    for (var item in items) {
        var size = area(intersection(item, feat))

        if (size > largest) {
            largest = size
            result = item[field]
        }
    }

    return result
}

return getAttributeFromLargestArea($feature, set, 'NAME');
'''

extract_zip = '''var set = FeatureSetByName($datastore, 'ZipCodes')
function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat)
    var counts = count(items);

    if (counts == 0) {
        return { 'errorMessage': 'No intersection found' };
    }

    if (counts == 1) {
        var result = first(items)

        return result[field]
    }

    var largest = -1
    var result

    for (var item in items) {
        var size = area(intersection(item, feat))

        if (size > largest) {
            largest = size
            result = item[field]
        }
    }

    return result
}

return getAttributeFromLargestArea($feature, set, 'ZIP5');
'''

constrain_domain = '''var code = number($feature.countyfips)
if (isnan(code)) {
    return false
}

if (code % 2 == 0) {
    return false
}

return code >= 49001 && code <= 49057;
'''

create_id = '''return 'UTU' + right($feature.countyfips, 2) + upper(mid($feature.guid, 29, 8))'''

FACILITY_GUID = Constant('Facility Guid', 'GUID', 'Facility.Guid', 'Guid()')
FACILITY_STATE = Constant('Facility State', 'FacilityState', 'Facility.State', '"UT"')
FACILITY_FIPS = Calculation('County Fips', 'CountyFIPS', 'Facility.FIPS', extract_fips)
FACILITY_ID = Calculation('Facility Id', 'FacilityID', 'Facility.Id', create_id)
FACILITY_CITY = Calculation('Facility City', 'FacilityCity', 'Facility.City', extract_city)
FACILITY_ZIP = Calculation('Facility Zip', 'FacilityZIP', 'Facility.ZipCode', extract_zip)
FACILITY_FIPS_DOMAIN = Constraint('County Fips', 'CountyFIPS', 'Facility.FIPS', constrain_domain)
