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
from rules import (
    area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit, operating_status, violation, well
)

facility_rules = CalculateWithArcadeRule(
    config.sde, facility.TABLE, [
        facility.GUID,
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
        well.SUBCLASS,
        well.HIGHPRIORITY,
        well.INJECTION_AQUIFER_EXEMPT,
        well.NO_MIGRATION_PET_STATUS,
    ]
)

aor_rules = CalculateWithArcadeRule(
    config.sde,
    area_of_review.TABLE,
    [
        area_of_review.GUID,
    ],
)

art_pen_rules = CalculateWithArcadeRule(
    config.sde,
    art_pen.TABLE,
    [
        art_pen.GUID,
    ],
)

authorization_rules = CalculateWithArcadeRule(
    config.sde,
    authorization.TABLE,
    [
        authorization.GUID,
        authorization.ID,
    ],
)

auth_action_rules = CalculateWithArcadeRule(
    config.sde,
    authorization_action.TABLE,
    [
        authorization_action.GUID,
    ],
)

contact_rules = CalculateWithArcadeRule(
    config.sde,
    contact.TABLE,
    [
        contact.GUID,
    ],
)

correction_rules = CalculateWithArcadeRule(
    config.sde,
    correction.TABLE,
    [
        correction.GUID,
    ],
)

enforcement_rules = CalculateWithArcadeRule(
    config.sde,
    enforcement.TABLE,
    [
        enforcement.GUID,
    ],
)

inspection_rules = CalculateWithArcadeRule(
    config.sde,
    inspection.TABLE,
    [
        inspection.GUID,
    ],
)

mit_rules = CalculateWithArcadeRule(
    config.sde,
    mit.TABLE,
    [
        mit.GUID,
    ],
)

operating_status_rules = CalculateWithArcadeRule(
    config.sde,
    operating_status.TABLE,
    [
        operating_status.GUID,
    ],
)

violation_rules = CalculateWithArcadeRule(
    config.sde,
    violation.TABLE,
    [
        violation.GUID,
    ],
)

rules = [
    facility_rules,
    well_rules,
    aor_rules,
    art_pen_rules,
    auth_action_rules,
    authorization_rules,
    contact_rules,
    correction_rules,
    enforcement_rules,
    inspection_rules,
    mit_rules,
    operating_status_rules,
    violation_rules,
]

if not arcpy.TestSchemaLock(os.path.join(config.sde, facility.TABLE)):
    print('Unable to acquire the necessary schema lock to add rules')
    exit(0)

for rule in rules:
    rule.execute()

arcpy.management.ClearWorkspaceCache(config.sde)
