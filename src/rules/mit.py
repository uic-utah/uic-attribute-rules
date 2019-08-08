#!/usr/bin/env python
# * coding: utf8 *
'''
mit.py
A module that has the UICMIT rules
'''

from config import config
from models.ruletypes import Constant, Constraint

from . import common

TABLE = 'UICMIT'

guid_constant = Constant('MIT Guid', 'GUID', 'MIT.Guid', 'GUID()')

type_constraint = Constraint('MIT Type', 'MIT.Type', common.constrain_to_domain('MITType', domain='UICMITTypeDomain'))
type_constraint.triggers = [config.triggers.insert, config.triggers.update]

date_constraint_update = Constraint('MIT ', 'UICMIT.MITDate.update', common.constrain_to_required('MITDate'))
date_constraint_update.triggers = [config.triggers.update]

result_constraint_update = Constraint('MIT ', 'UICMIT.MITResult.update', common.constrain_to_required('MITResult'))
result_constraint_update.triggers = [config.triggers.update]

RULES = [
    guid_constant,
    type_constraint,
    date_constraint_update,
    result_constraint_update,
]
