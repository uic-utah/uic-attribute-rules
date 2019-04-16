#!/usr/bin/env python
# * coding: utf8 *
'''
facility.py
A module that creates attribute rules for the UICFacility table
'''

from config import config
from models.ruletypes import Calculation, Constant, Constraint

TABLE = 'UICFacility'

extract_fips = '''var field = 'FIPS';
var set = FeatureSetByName($datastore, 'Counties', [field], true);

function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return { 'errorMessage': 'No intersection found' };
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

var result = getAttributeFromLargestArea($feature, set, field);
result = text(result, '00')

return iif(isnan(number('490' + result)), null, number('490' + result));'''

extract_city = '''var field = 'NAME';
var set = FeatureSetByName($datastore, 'Municipalities', [field], true);

function getAttributeFromLargestArea(feat, set, field) {
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

return getAttributeFromLargestArea($feature, set, field);
'''

extract_zip = '''var field = 'ZIP5';
var set = FeatureSetByName($datastore, 'ZipCodes', [field], true);

function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat);
    var counts = count(items);

    if (counts == 0) {
        return { 'errorMessage': 'No intersection found' };
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

return getAttributeFromLargestArea($feature, set, field);
'''

constrain_domain = '''if (!haskey($feature, 'countyfips')) {
    return true;
}

var code = number($feature.countyfips)
if (isnan(code)) {
    return {
        'errorMessage': 'The fips code is empty'
    };
}

if (code % 2 == 0) {
    return {
        'errorMessage': 'The fips code is should be odd: ' + code
    };
}

if (code >= 49001 && code <= 49057) {
    return true;
}

return {
    'errorMessage': 'The code does not fall within the valid ranges: ' + code
};
'''

create_id = '''var keys = ['countyfips', 'guid'];

for (var key in keys) {
    if (!haskey($feature, keys[key])) {
        return null;
    }
}

return 'UTU' + right($feature.countyfips, 2) + 'F' + upper(mid($feature.guid, 29, 8))'''

GUID = Constant('Facility Guid', 'GUID', 'Facility.Guid', 'Guid()')
FIPS = Calculation('County Fips', 'CountyFIPS', 'Facility.FIPS', extract_fips)
ID = Calculation('Facility Id', 'FacilityID', 'Facility.Id', create_id)
CITY = Calculation('Facility City', 'FacilityCity', 'Facility.City', extract_city)
ZIP = Calculation('Facility Zip', 'FacilityZIP', 'Facility.ZipCode', extract_zip)
FIPS_DOMAIN = Constraint('County Fips', 'Facility.FIPS', constrain_domain)
FIPS_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]
