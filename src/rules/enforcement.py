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

if (isempty($feature.EnforcementType) || lower(domainname($feature, 'EnforcementType')) != 'otr') {
    return true;
}

return iif (isempty($feature.comments), {
    'errorMessage': 'When Enforcement Type is OTR, a comment is required'
}, true);'''

TABLE = 'UICEnforcement'

GUID = Constant('Enforcement Guid', 'GUID', 'Enforcement.Guid', 'GUID()')

TYPE = Constraint('Enforcement Type', 'Enforcement.EnforcementType', common.constrain_to_domain('EnforcementType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

COMMENT = Constraint('Comment', 'Enforcement.Comment', constrain_other_comment)
COMMENT.triggers = [config.triggers.insert, config.triggers.update]
