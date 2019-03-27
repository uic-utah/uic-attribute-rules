#!/usr/bin/env python
# * coding: utf8 *
'''
rule.py
A module that acts as the base class for all rules
'''

import os

from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module

import arcpy


class Rule(object):

    def __init__(self):
        self.name = None
        self.meta_rules = []
        self.table_path = None

    def execute(self):
        print('creating rules for {}'.format(self.name))
        for rule in self.meta_rules:
            print('  creating {} rule'.format(rule.rule_name))

            try:
                arcpy.management.DeleteAttributeRule(self.table_path, rule.rule_name)
            except Exception:
                pass

            try:
                arcpy.management.AddAttributeRule(
                    in_table=self.table_path,
                    name=rule.rule_name,
                    type=rule.type,
                    script_expression=rule.arcade,
                    is_editable=rule.editable,
                    triggering_events=rule.triggers,
                    error_number=rule.error_number,
                    error_message=rule.error_message,
                    description=rule.description,
                    subtype='',
                    field=rule.field,
                    exclude_from_client_evaluation='',
                    batch=False,
                    severity='',
                    tags=rule.tag
                )
                print('  done')
            except ExecuteError as e:
                message, = e.args

                if message.startswith('ERROR 002541'):
                    print('    rule already exists, skipping...')
                else:
                    raise e


class CalculateWithArcadeRule(Rule):

    def __init__(self, sde, table, metas):
        super(CalculateWithArcadeRule, self).__init__()

        self.name = table
        self.table_path = os.path.join(sde, table)
        self.meta_rules = metas
