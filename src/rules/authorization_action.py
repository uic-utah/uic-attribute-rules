#!/usr/bin/env python
# * coding: utf8 *
'''
authorization_action.py
A module that has the UICAuthorizationAction rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

TABLE = 'UICAuthorizationAction'

GUID = Constant('Authorization Action Guid', 'GUID', 'AuthorizationAction.Guid', 'GUID()')

TYPE = Constraint('Authorization Action Type', 'AuthorizationAction.AuthorizationActionType', common.constrain_to_domain('AuthorizationActionType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]
