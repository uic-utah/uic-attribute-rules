#!/usr/bin/env python
# * coding: utf8 *
'''
config.py
A module that stores common items for attribute rules
'''
import os
from types import SimpleNamespace

triggers = SimpleNamespace(**{
    'update': 'UPDATE',
    'insert': 'INSERT',
    'delete': 'DELETE'
})

rule_type = SimpleNamespace(**{
    'calculation': 'CALCULATION',
    'constraint': 'CONSTRAINT'
})

editable = SimpleNamespace(**{
    'yes': 'EDITABLE',
    'no': 'NONEDITABLE'
})

sde = os.path.join(os.path.dirname(__file__), '..', '..', 'pro-project', 'localhost.sde')
