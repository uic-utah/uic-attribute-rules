#!/usr/bin/env python
# * coding: utf8 *
'''
rule.py
A module that acts as the base class for all rules
'''

from arcgisscripting import ExecuteError

import arcpy
from config import config


class Rule(object):

    def __init__(self):
        self.name = None
        self.meta_rules = []
        self.table_path = None
        self.description = None
        self.tag = None
        self.error_number = -1
        self.error_message = None
        self.arcade = None
        self.editable = config.editable.no
        self.triggers = config.triggers.insert

    def execute(self):
        print('creating rules for {}'.format(self.name))
        for rule in self.meta_rules:
            print('  creating {} rule'.format(rule.rule_name))

            if not hasattr(rule, 'arcade'):
                rule.arcade = self.arcade

            try:
                arcpy.management.DeleteAttributeRule(self.table_path, rule.rule_name)
            except Exception:
                pass

            try:
                arcpy.management.AddAttributeRule(
                    in_table=self.table_path,
                    name=rule.rule_name,
                    type=config.rule_type.calculation,
                    script_expression=rule.arcade,
                    is_editable=self.editable,
                    triggering_events=self.triggers,
                    error_number=self.error_number,
                    error_message=self.error_message,
                    description=rule.description,
                    subtype='',
                    field=rule.field,
                    exclude_from_client_evaluation='',
                    batch=False,
                    severity='',
                    tags=self.tag
                )
                print('  done')
            except ExecuteError as e:
                message, = e.args

                if message.startswith('ERROR 002541'):
                    print('    rule already exists, skipping...')
                else:
                    raise e
