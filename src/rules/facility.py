#!/usr/bin/env python
# * coding: utf8 *
'''
facility.py
A module that creates attribute rules for the UICFacility table
'''

import os

from models.rule import Rule


class CalculateGuidRule(Rule):

    def __init__(self, sde, table, metas):
        self.name = table
        self.table_path = os.path.join(sde, table)
        self.meta_rules = metas

        self.tag = 'GUID'

        self.error_number = 7500
        self.error_message = 'This GUID is auto generated and cannot be modified.'

        self.arcade = 'return Guid()'


class CalculateConstantRule(Rule):

    def __init__(self, sde, table, metas):
        self.name = table
        self.table_path = os.path.join(sde, table)
        self.meta_rules = metas

        self.tag = 'Constant'

        self.error_number = 7501
        self.error_message = 'This value is auto generated and cannot be modified.'

        self.arcade = 'return "UT"'
