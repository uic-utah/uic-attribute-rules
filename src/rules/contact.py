#!/usr/bin/env python
# * coding: utf8 *
'''
contact.py
A module that has the UICContact rules
'''

from config import config
from models.ruletypes import Constant, Constraint
from services.loader import load_rule_for

from . import common

TABLE = 'UICContact'
FOLDER = 'contact'

guid_constant = Constant('Contact Guid', 'GUID', 'GUID()')

name_constraint_update = Constraint('Contact Name', 'Contact.ContactName.update', common.constrain_to_required('ContactName'))
name_constraint_update.triggers = [config.triggers.update]

organization_constraint_update = Constraint('Contact Organization', 'Contact.ContactOrganization.update', common.constrain_to_required('ContactOrganization'))
organization_constraint_update.triggers = [config.triggers.update]

address_constraint_update = Constraint('Contact mailing address', 'Contact.ContactMailAddress.update', common.constrain_to_required('ContactMailAddress'))
address_constraint_update.triggers = [config.triggers.update]

city_constraint_update = Constraint('Contact mailing city', 'Contact.ContactMailCity.update', common.constrain_to_required('ContactMailCity'))
city_constraint_update.triggers = [config.triggers.update]

state_constraint_update = Constraint('Contact mailing state', 'Contact.ContactMailState.update', common.constrain_to_required('ContactMailState'))
state_constraint_update.triggers = [config.triggers.update]

type_constraint = Constraint('Contact Type', 'Contact.Type', common.constrain_to_domain('ContactType', allow_null=True, domain='UICContactTypeDomain'))

type_constraint_update = Constraint(
    'Contact Type', 'Contact.Type.update', common.constrain_to_domain('ContactType', allow_null=False, domain='UICContactTypeDomain')
)
type_constraint_update.triggers = [config.triggers.update]

state_constraint = Constraint('Mail State', 'Contact.MailState', common.constrain_to_domain('ContactMailState', allow_null=True, domain='UICStateDomain'))

state_constraint_update = Constraint(
    'Mail State', 'Contact.MailState.update', common.constrain_to_domain('ContactMailState', allow_null=False, domain='UICStateDomain')
)
state_constraint_update.triggers = [config.triggers.update]

contact_type_constraint = Constraint('Owner Operator', 'Contact.OwnerType', load_rule_for(FOLDER, 'contactType'))
contact_type_constraint.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    type_constraint,
    state_constraint,
    #: this doesn't work with m*m
    # contact_type_constraint,
    type_constraint_update,
    state_constraint_update,
    name_constraint_update,
    organization_constraint_update,
    address_constraint_update,
    city_constraint_update,
    state_constraint_update,
    state_constraint,
]
