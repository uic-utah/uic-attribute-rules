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
        facility.FACILITY_GUID,
        facility.FACILITY_STATE,
        facility.FACILITY_FIPS_DOMAIN,
        facility.FACILITY_FIPS,
        facility.FACILITY_ID,
        facility.FACILITY_CITY,
        facility.FACILITY_ZIP,
    config.sde, facility.TABLE, [
    ]
)

well_rules = CalculateWithArcadeRule(
    config.sde, well.TABLE, [
    config.sde,
    [
        well.WELL_GUID,
        well.WELL_ID,
        well.WELL_FACILITY,
        well.WELL_CLASS,
        # well.,
        well.WELL_HIGHPRIORITY,
        well.WELL_INJECTION_AQUIFER_EXEMPT,
    ]
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
