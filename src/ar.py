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
from config.config import get_sde_path_for
from models.rule import RuleGroup
from rules import (
    area_of_review, art_pen, authorization, authorization_action, contact, correction, enforcement, facility, inspection, mit, operating_status, violation, well
)


def get_rules(sde, rule=None):
    facility_rules = RuleGroup(sde, facility.TABLE, facility.RULES)
    well_rules = RuleGroup(sde, well.TABLE, well.RULES)
    aor_rules = RuleGroup(sde, area_of_review.TABLE, area_of_review.RULES)
    art_pen_rules = RuleGroup(sde, art_pen.TABLE, art_pen.RULES)
    authorization_rules = RuleGroup(sde, authorization.TABLE, authorization.RULES)
    auth_action_rules = RuleGroup(sde, authorization_action.TABLE, authorization_action.RULES)
    contact_rules = RuleGroup(sde, contact.TABLE, contact.RULES)
    correction_rules = RuleGroup(sde, correction.TABLE, correction.RULES)
    enforcement_rules = RuleGroup(sde, enforcement.TABLE, enforcement.RULES)
    inspection_rules = RuleGroup(sde, inspection.TABLE, inspection.RULES)
    mit_rules = RuleGroup(sde, mit.TABLE, mit.RULES)
    operating_status_rules = RuleGroup(sde, operating_status.TABLE, operating_status.RULES)
    violation_rules = RuleGroup(sde, violation.TABLE, violation.RULES)

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
        print('Unable to reach the database or acquire the necessary schema lock to add rules')
        exit(0)

    if args['update']:
        for rule in get_rules(sde, args['--rule']):
            rule.execute()
    elif args['delete']:
        for rule in get_rules(sde, args['--rule']):
            rule.delete()

    arcpy.management.ClearWorkspaceCache(sde)
