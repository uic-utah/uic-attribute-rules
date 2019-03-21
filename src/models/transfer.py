#!/usr/bin/env python
# * coding: utf8 *
'''
tranfer.py
A module that holds the data tranfer models
'''


class Guid(object):

    def __init__(self, name, field, rule_name):
        self.name = name
        self.field = field
        self.rule_name = rule_name
        self.description = 'Calculation Rule. {}'.format(rule_name)


class Constant(object):

    def __init__(self, name, field, rule_name, value):
        self.name = name
        self.field = field
        self.rule_name = rule_name
        self.description = 'Calculation Rule. {}'.format(rule_name)
        self.arcade = 'return "{}"'.format(value)
