#!/usr/bin/env python
# * coding: utf8 *
'''
operating_status.py
A module that has the UICWellOperatingStatus rules
'''

from . import common
from config import config
from services.loader import load_rule_for
from models.ruletypes import Constant, Constraint

TABLE = 'UICWellOperatingStatus'
FOLDER = 'operatingStatus'

guid_constant = Constant('Well operating status Guid', 'GUID', 'WellOperatingStatus.Guid', 'GUID()')

type_domain_constraint = Constraint(
    'Operating Status Type', 'OperatingStatus.Type', common.constrain_to_domain('OperatingStatusType', 'UICOperatingStatusTypeDomain')
)
type_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

date_constraint = Constraint('Operating Status Date', 'OperatingStatus.Date', load_rule_for(FOLDER, 'dateConstraint'))
date_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    date_constraint,
]
