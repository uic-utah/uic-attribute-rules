#!/usr/bin/env python
# * coding: utf8 *
'''
ar

Usage:
    ar update [--rule=<rule>]
    ar delete
    ar --version
    ar (-h | --help)

Options:
    --rule=<rule>   The allowable rules.
                        area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit,
                        operating_status, violation, well
    -h --help       Shows this screen
    -v --version    Shows the version
'''

import os

from docopt import docopt

import arcpy
from config import config
from models.rule import ArcadeRule
from rules import (
    area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit, operating_status, violation, well
)

facility_rules = ArcadeRule(
    config.sde, facility.TABLE, [
        facility.GUID,
        facility.FIPS_DOMAIN,
        facility.FIPS,
        facility.ID,
        facility.CITY,
        facility.ZIP,
        facility.ZIP_DOMAIN,
    ]
)

well_rules = ArcadeRule(
    config.sde, well.TABLE, [
        well.GUID,
        well.ID,
        well.FACILITY,
        well.CLASS,
        well.SUBCLASS,
        well.HIGHPRIORITY,
        well.INJECTION_AQUIFER_EXEMPT,
        well.NO_MIGRATION_PET_STATUS,
        well.FACILITY_TYPE,
        well.REMEDIATION_TYPE,
        well.SWPZ,
    ]
)

aor_rules = ArcadeRule(
    config.sde,
    area_of_review.TABLE,
    [
        area_of_review.GUID,
    ],
)

art_pen_rules = ArcadeRule(
    config.sde,
    art_pen.TABLE,
    [
        art_pen.GUID,
        art_pen.WELL_TYPE,
        art_pen.CA_DOMAIN,
    ],
)

authorization_rules = ArcadeRule(
    config.sde,
    authorization.TABLE,
    [
        authorization.GUID,
        authorization.ID,
        authorization.TYPE,
        authorization.SECTOR_TYPE,
    ],
)

auth_action_rules = ArcadeRule(
    config.sde,
    authorization_action.TABLE,
    [
        authorization_action.GUID,
        authorization_action.TYPE,
        authorization_action.ACTION_DATE,
    ],
)

contact_rules = ArcadeRule(
    config.sde,
    contact.TABLE,
    [
        contact.GUID,
        contact.TYPE,
        contact.STATE,
        # contact.CONTACT_TYPE,
    ],
)

correction_rules = ArcadeRule(
    config.sde,
    correction.TABLE,
    [
        correction.GUID,
        correction.TYPE,
        correction.COMMENT,
    ],
)

enforcement_rules = ArcadeRule(
    config.sde,
    enforcement.TABLE,
    [
        enforcement.GUID,
        enforcement.TYPE,
        enforcement.COMMENT,
    ],
)

inspection_rules = ArcadeRule(
    config.sde,
    inspection.TABLE,
    [
        inspection.GUID,
        inspection.TYPE_DOMAIN,
        inspection.ASSISTANCE_DOMAIN,
        inspection.DEFICIENCY_DOMAIN,
        inspection.FOREIGN_KEY,
        inspection.FACILITY_ONLY,
        inspection.INSPECTION_DATE,
        inspection.CORRECTION,
    ],
)

mit_rules = ArcadeRule(
    config.sde,
    mit.TABLE,
    [
        mit.GUID,
        mit.TYPE,
        mit.ACTION,
    ],
)

operating_status_rules = ArcadeRule(
    config.sde,
    operating_status.TABLE,
    [
        operating_status.GUID,
        operating_status.TYPE,
        operating_status.DATE,
    ],
)

violation_rules = ArcadeRule(
    config.sde,
    violation.TABLE,
    [
        violation.GUID,
        violation.TYPE,
        violation.CONTAMINATION,
        violation.CONTAMINATION_CALC,
        violation.ENDANGER,
        violation.NONCOMPLIANCE,
        violation.COMMENT,
        violation.VIOLATIONS,
    ],
)


def get_rules(rule=None):
    if rule is None:
        return [
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

    rules = {
        'area_of_review': aor_rules,
        'art_pen': art_pen_rules,
        'authorization': authorization_rules,
        'authorization_action': auth_action_rules,
        'contact': contact_rules,
        'correction': correction_rules,
        'enforcement': enforcement_rules,
        'facility': facility_rules,
        'inspection': inspection_rules,
        'mit': mit_rules,
        'operating_status': operating_status_rules,
        'violation': violation_rules,
        'well': well_rules
    }

    return [rules[rule]]


if __name__ == '__main__':
    '''Main entry point for program. Parse arguments and pass to engine module
    '''
    args = docopt(__doc__, version='1.0.0')

    if not arcpy.TestSchemaLock(os.path.join(config.sde, facility.TABLE)):
        print('Unable to acquire the necessary schema lock to add rules')
        exit(0)

    if args['update']:
        for rule in get_rules(args['--rule']):
            rule.execute()
    elif args['delete']:
        for rule in get_rules(args['--rule']):
            rule.delete()

    arcpy.management.ClearWorkspaceCache(config.sde)
