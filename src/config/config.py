#!/usr/bin/env python
# * coding: utf8 *
'''
config.py
A module that stores common items for attribute rules
'''
from types import SimpleNamespace

triggers = SimpleNamespace(**{
    'update': 'UPDATE',
    'insert': 'INSERT',
    'delete': 'DELETE',
})

rule_types = SimpleNamespace(**{
    'calculation': 'CALCULATION',
    'constraint': 'CONSTRAINT',
})

editable = SimpleNamespace(**{
    'yes': 'EDITABLE',
    'no': 'NONEDITABLE',
})
