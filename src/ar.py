#!/usr/bin/env python
# * coding: utf8 *
'''
ar

Usage:
    ar update [--rule=<rule> --env=<env>]
    ar delete [--env=<env>]
    ar --version
    ar (-h | --help)

Options:
    --rule=<rule>   The allowable rules.
                        area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit,
                        operating_status, violation, well
    --env=<env>     local, dev, prod
    -h --help       Shows this screen
    -v --version    Shows the version
'''

import os

from docopt import docopt

import arcpy
from models.rule import RuleGroup
from rules import (
    area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit, operating_status, violation, well
)


def get_sde_path_for(env=None):
    sde = os.path.join(os.path.dirname(__file__), '..', 'pro-project')

    if env is None:
        return os.path.join(sde, 'localhost.sde')

    if env == 'local':
        return os.path.join(sde, 'localhost.sde')

    if env == 'dev':
        return os.path.join(sde, 'stage.sde')

    if env == 'prod':
        return os.path.join(sde, 'prod.sde')

    raise Exception('{} env not found'.format(env))


def get_rules(sde, rule=None):
    facility_rules = ArcadeRule(
        sde, facility.TABLE, [
            facility.GUID,
            facility.FIPS_DOMAIN,
            facility.FIPS,
            facility.ID,
            facility.CITY,
            facility.ZIP,
            facility.ZIP_DOMAIN,
        ]
    )


    aor_rules = ArcadeRule(
        sde,
        area_of_review.TABLE,
        [
            area_of_review.GUID,
        ],
    )

    art_pen_rules = ArcadeRule(
        sde,
        art_pen.TABLE,
        [
            art_pen.GUID,
            art_pen.WELL_TYPE,
            art_pen.CA_DATE,
        ],
    )

    authorization_rules = ArcadeRule(
        sde,
        authorization.TABLE,
        [
            authorization.GUID,
            authorization.ID,
            authorization.TYPE_DOMAIN,
            authorization.TYPE,
            authorization.SECTOR_TYPE,
        ],
    )

    well_rules = RuleGroup(sde, well.TABLE, well.RULES)
    auth_action_rules = RuleGroup(sde, authorization_action.TABLE, authorization_action.RULES)
    contact_rules = ArcadeRule(
    well_rules = RuleGroup(sde, well.TABLE, well.RULES)
        sde,
        contact.TABLE,
        [
            contact.GUID,
            contact.TYPE,
            contact.STATE,
            # contact.CONTACT_TYPE,
        ],
    )

    correction_rules = ArcadeRule(
        sde,
        correction.TABLE,
        [
            correction.GUID,
            correction.TYPE,
            correction.COMMENT,
        ],
    )

    enforcement_rules = ArcadeRule(
        sde,
        enforcement.TABLE,
        [
            enforcement.GUID,
            enforcement.TYPE,
            enforcement.COMMENT,
        ],
    )

    inspection_rules = ArcadeRule(
        sde,
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
        sde,
        mit.TABLE,
        [
            mit.GUID,
            mit.TYPE,
        ],
    )

    operating_status_rules = ArcadeRule(
        sde,
        operating_status.TABLE,
        [
            operating_status.GUID,
            operating_status.TYPE,
            operating_status.DATE,
        ],
    )

    violation_rules = ArcadeRule(
        sde, violation.TABLE, [
            violation.GUID,
            violation.TYPE,
            violation.CONTAMINATION,
            violation.CONTAMINATION_CALC,
            violation.ENDANGER,
            violation.NONCOMPLIANCE,
            violation.COMMENT,
            violation.VIOLATIONS,
        ]
    )

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

    sde = get_sde_path_for(args['--env'])
    print('acting on {}'.format(sde))

    if not arcpy.TestSchemaLock(os.path.join(sde, facility.TABLE)):
        print('Unable to acquire the necessary schema lock to add rules')
        exit(0)

    if args['update']:
        for rule in get_rules(sde, args['--rule']):
            rule.execute()
    elif args['delete']:
        for rule in get_rules(sde, args['--rule']):
            rule.delete()

    arcpy.management.ClearWorkspaceCache(sde)
