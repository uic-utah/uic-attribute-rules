#!/usr/bin/env python
# * coding: utf8 *
'''
ar.py
A module that runs attribute rules
'''

import os

import arcpy
from config import config
from models.transfer import Calculation, Constant, Guid
from rules.facility import CalculateConstantRule, CalculateGuidRule, CalculateWithArcadeRule

tables = {'facility': 'UICFacility'}

create_id = "'UTU' + right($feature.CountyFIPS, 2) + upper(mid($feature.GUID, 29, 8))"
extract_fips = '''var set = FeatureSetByName($datastore, 'Counties')
function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat)
    console(items)

    if (items == false) {
        return { 'errorMessage': 'No intersection found' }
    }

    if (count(items) == 1) {
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

getAttributeFromLargestArea($feature, set, 'FIPS')
'''
extract_city = '''
var set = FeatureSetByName($datastore, 'Municipalities')
function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat)
    console(items)

    if (items == false) {
        return { 'errorMessage': 'No intersection found' }
    }

    if (count(items) == 1) {
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

getAttributeFromLargestArea($feature, set, 'NAME')
'''

extract_zip = '''
var set = FeatureSetByName($datastore, 'ZipCodes')
function getAttributeFromLargestArea(feat, set, field) {
    var items = intersects(set, feat)
    console(items)

    if (items == false) {
        return { 'errorMessage': 'No intersection found' }
    }

    if (count(items) == 1) {
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
getAttributeFromLargestArea($feature, set, 'ZIP5')
'''

create_id = '''return 'UTU' + $feature.countyfips + upper(mid($feature.guid, 29, 8))'''

guid_rule = CalculateGuidRule(config.sde, tables['facility'], [Guid('Facility Guid', 'GUID', 'Guid')])

state_rule = CalculateConstantRule(config.sde, tables['facility'], [Constant('Facility State', 'FacilityState', 'State', 'UT')])

fips_rule = CalculateWithArcadeRule(
    config.sde, tables['facility'], [
        Calculation('County Fips', 'CountyFIPS', 'FIPS', extract_fips),
        Calculation('Facility Id', 'FacilityID', 'Id', create_id),
        Calculation('Facility City', 'FacilityCity', 'City', extract_city),
        Calculation('Facility Zip', 'FacilityZIP', 'ZipCode', extract_zip),
    ]
)

id_rule = CalculateWithArcadeRule(config.sde, tables['facility'], [])

rules = [guid_rule, state_rule, fips_rule, id_rule]

if not arcpy.TestSchemaLock(os.path.join(config.sde, tables['facility'])):
    print('Unable to acquire the necessary schema lock to add rules')
    exit(0)

for rule in rules:
    rule.execute()

arcpy.management.ClearWorkspaceCache(config.sde)
