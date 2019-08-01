#!/usr/bin/env python
# * coding: utf8 *
'''
enforcement.py
A module that has the UICEnforcement rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

constrain_other_comment = '''if (!haskey($feature, 'EnforcementType') || !haskey($feature, 'comments')) {
    return true;
}

if (isempty($feature.EnforcementType) || lower(domaincode($feature, 'EnforcementType', $feature.enforcementtype)) != 'otr') {
    return true;
}

return iif (isempty($feature.comments), {
    'errorMessage': 'When EnforcementType is OTR, enter a description of the other type of enforcement action taken in the Comment field. This is required.'
}, true);'''

TABLE = 'UICEnforcement'

GUID = Constant('Enforcement Guid', 'GUID', 'Enforcement.Guid', 'GUID()')

TYPE = Constraint('Enforcement Type', 'Enforcement.EnforcementType', common.constrain_to_domain('EnforcementType', 'UICEnforcementTypeDomain'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

COMMENT = Constraint('Comment', 'Enforcement.Comment', constrain_other_comment)
COMMENT.triggers = [config.triggers.insert, config.triggers.update]
