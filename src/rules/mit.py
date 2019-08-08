#!/usr/bin/env python
# * coding: utf8 *
'''
mit.py
A module that has the UICMIT rules
'''

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = 'UICMIT'
FOLDER = 'mit'

guid_constant = Constant('MIT Guid', 'GUID', 'MIT.Guid', 'GUID()')

type_domain_constraint = Constraint('MIT type', 'MIT.Type', common.constrain_to_domain('MITType', allow_null=False, domain='UICMITTypeDomain'))
type_domain_constraint.triggers = [config.triggers.update]

date_constraint_update = Constraint('MIT date', 'UICMIT.MITDate.update', common.constrain_to_required('MITDate'))
date_constraint_update.triggers = [config.triggers.update]

result_constraint_update = Constraint('MIT result', 'UICMIT.MITResult.update', common.constrain_to_required('MITResult'))
result_constraint_update.triggers = [config.triggers.update]

type_constraint = Constraint('MIT Date and Type', 'UICMIT.MITDate', load_rule_for(FOLDER, 'typeConstraint'))
type_constraint.triggers = [config.triggers.insert, config.triggers.update]

result_constraint = Constraint('MIT Result and Type', 'UICMIT.MITResult', load_rule_for(FOLDER, 'resultConstraint'))
result_constraint.triggers = [config.triggers.insert, config.triggers.update]

remediation_constraint = Constraint('MIT Remediation Action and Result', 'UICMIT.RemediationAction', load_rule_for(FOLDER, 'remedationConstraint'))
remediation_constraint.triggers = [config.triggers.insert, config.triggers.update]

remeditation_date_constraint = Constraint('Remediation Action Date and Remedation Action', 'UICMIT.RemActDate', load_rule_for(FOLDER, 'remediationDate'))
remeditation_date_constraint.triggers = [config.triggers.insert, config.triggers.update]

comment_constraint = Constraint('Comment for Other Action', 'MIT.Comment', load_rule_for(FOLDER, 'commentConstraint'))
comment_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_domain_constraint,
    date_constraint_update,
    result_constraint_update,
    type_constraint,
    result_constraint,
    remediation_constraint,
    remeditation_date_constraint,
    comment_constraint,
]
