#!/usr/bin/env python
# * coding: utf8 *
'''
mit.py
A module that has the UICMIT rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

TABLE = 'UICMIT'

GUID = Constant('MIT Guid', 'GUID', 'MIT.Guid', 'GUID()')

TYPE = Constraint('MIT Type', 'MIT.Type', common.constrain_to_domain('MITType', 'UICMITTypeDomain'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

ACTION = Constraint('MIT Remediation Action', 'MIT.Remediation Action', common.constrain_to_domain('MITRemediationAction', 'UICMITRemediationActionDomain'))
ACTION.triggers = [config.triggers.insert, config.triggers.update]
