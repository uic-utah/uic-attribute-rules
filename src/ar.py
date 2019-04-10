#!/usr/bin/env python
# * coding: utf8 *
'''
ar.py
A module that runs attribute rules
'''

import os

import arcpy
from config import config
from models.rule import CalculateWithArcadeRule
from rules import facility, well


facility_rules = CalculateWithArcadeRule(
    config.sde, facility.TABLE, [
        facility.GUID,
        facility.STATE,
        facility.FIPS_DOMAIN,
        facility.FIPS,
        facility.ID,
        facility.CITY,
        facility.ZIP,
    ]
)

well_rules = CalculateWithArcadeRule(
    config.sde, well.TABLE, [
        well.GUID,
        well.ID,
        well.FACILITY,
        well.CLASS,
        well.HIGHPRIORITY,
        well.INJECTION_AQUIFER_EXEMPT,
    ]
    config.sde,
    [
)

rules = [
    # facility_rules,
    well_rules,
]

if not arcpy.TestSchemaLock(os.path.join(config.sde, facility.TABLE)):
    print('Unable to acquire the necessary schema lock to add rules')
    exit(0)

for rule in rules:
    rule.execute()

arcpy.management.ClearWorkspaceCache(config.sde)
