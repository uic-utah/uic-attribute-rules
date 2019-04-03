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

tables = {'facility': 'UICFacility', 'well': 'UICWell'}

facility_rules = CalculateWithArcadeRule(
    config.sde, tables['facility'], [
        facility.FACILITY_GUID,
        facility.FACILITY_STATE,
        facility.FACILITY_FIPS_DOMAIN,
        facility.FACILITY_FIPS,
        facility.FACILITY_ID,
        facility.FACILITY_CITY,
        facility.FACILITY_ZIP,
    ]
)

well_rules = CalculateWithArcadeRule(config.sde, tables['well'], [
    well.WELL_GUID,
    well.WELL_ID,
    well.WELL_FACILITY,
])

rules = [
    # facility_rules,
    well_rules,
]

if not arcpy.TestSchemaLock(os.path.join(config.sde, tables['facility'])):
    print('Unable to acquire the necessary schema lock to add rules')
    exit(0)

for rule in rules:
    rule.execute()

arcpy.management.ClearWorkspaceCache(config.sde)
