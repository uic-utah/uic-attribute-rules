#!/usr/bin/env python
# * coding: utf8 *
'''
ruletypes.py
A module that holds the types of rules
'''


class Constant(object):

    def __init__(self, name, field, rule_name, value):
        self.name = name
        self.field = field
        self.rule_name = 'Constant.' + rule_name
        self.description = 'Calculation Rule. {}'.format(rule_name)
        self.arcade = 'return {};'.format(value)


class Calculation(object):

    def __init__(self, name, field, rule_name, arcade):
        self.name = name
        self.field = field
        self.rule_name = 'Calculation.' + rule_name
        self.description = 'Calculation Rule. {}'.format(rule_name)
        self.arcade = arcade


class Constraint(object):

    def __init__(self, name, field, rule_name, arcade):
        self.name = name
        self.field = field
        self.rule_name = 'Constraint.' + rule_name
        self.description = 'Constraint Rule. {}'.format(rule_name)
        self.arcade = arcade
