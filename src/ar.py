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
from rules import facility

tables = {'facility': 'UICFacility'}

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

id_rule = CalculateWithArcadeRule(config.sde, tables['facility'], [])

rules = [facility_rules]

if not arcpy.TestSchemaLock(os.path.join(config.sde, tables['facility'])):
    print('Unable to acquire the necessary schema lock to add rules')
    exit(0)

for rule in rules:
    rule.execute()

arcpy.management.ClearWorkspaceCache(config.sde)
