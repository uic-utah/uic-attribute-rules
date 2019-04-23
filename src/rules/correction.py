#!/usr/bin/env python
# * coding: utf8 *
'''
correction.py
A module that has the UICCorrection rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

TABLE = 'UICCorrection'

constrain_other_comment = '''if (!haskey($feature, 'correctiveaction') || !haskey($feature, 'comments')) {
    return true;
}

if (isempty($feature.correctiveaction) || lower(domaincode($feature, 'correctiveaction')) != 'ot') {
    return true;
}

return iif (isempty($feature.comments), {
    'errorMessage': 'When Corrective action is OT, a comment is required'
}, true);'''

GUID = Constant('Correction Guid', 'GUID', 'Correction.Guid', 'GUID()')

TYPE = Constraint('Corrective Action', 'Correction.CorrectiveAction', common.constrain_to_domain('CorrectiveAction'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

COMMENT = Constraint('Comment', 'Correction.Comment', constrain_other_comment)
COMMENT.triggers = [config.triggers.insert, config.triggers.update]
