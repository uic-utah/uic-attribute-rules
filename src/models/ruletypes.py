#!/usr/bin/env python
# * coding: utf8 *
'''
ruletypes.py
A module that holds the types of rules
'''

from config import config


class BaseType(object):

    def __init__(self):
        self.type = config.rule_types.calculation
        self.editable = config.editable.no
        self.triggers = config.triggers.insert

        self.description = None
        self.tag = None
        self.error_number = -1
        self.error_message = None
        self.arcade = None
        self.error_number = 7500


class Constant(BaseType):

    def __init__(self, name, field, rule_name, value):
        super(Constant, self).__init__()

        self.name = name
        self.field = field
        self.rule_name = 'Constant.' + rule_name
        self.description = 'Calculation Rule. {}'.format(rule_name)

        self.arcade = 'return {};'.format(value)

        self.tag = 'Constant'

        self.error_number += 1
        self.error_message = 'This value is auto generated and cannot be modified.'


class Calculation(BaseType):

    def __init__(self, name, field, rule_name, arcade):
        super(Calculation, self).__init__()

        self.name = name
        self.field = field
        self.rule_name = 'Calculation.' + rule_name
        self.description = 'Calculation Rule. {}'.format(rule_name)

        self.arcade = arcade

        self.tag = 'Calculation'

        self.error_number += 2
        self.error_message = 'This value is auto generated and cannot be modified.'


class Constraint(BaseType):

        super(Constraint, self).__init__()

    def __init__(self, name, field, rule_name, arcade):
        self.name = name
        self.field = field
        self.rule_name = 'Constraint.' + rule_name
        self.description = 'Constraint Rule. {}'.format(rule_name)

        self.arcade = arcade

        self.type = config.rule_types.constraint

        self.tag = 'Constraint'

        self.error_number += 3
        self.error_message = 'The data entered does not fall within the allowable values.'
