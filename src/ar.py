#!/usr/bin/env python
# * coding: utf8 *
'''
ar.py
A module that runs attribute rules
'''

import arcpy
from config import config
from models.transfer import Constant, Guid
from rules.facility import CalculateConstantRule, CalculateGuidRule

tables = {'facility': 'UICFacility'}
rules = [
    CalculateGuidRule(config.sde, tables['facility'], [Guid('Facility Guid', 'GUID', 'Calculate_Guid')]),
    CalculateConstantRule(config.sde, tables['facility'], [Constant('Facility State', 'FacilityState', 'Calculate_State', 'UT')])
]

for rule in rules:
    rule.execute()

arcpy.management.ClearWorkspaceCache(config.sde)
