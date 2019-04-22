#!/usr/bin/env python
# * coding: utf8 *
'''
contact.py
A module that has the UICContact rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

TABLE = 'UICContact'

GUID = Constant('Contact Guid', 'GUID', 'Contact.Guid', 'GUID()')

TYPE = Constraint('Contact Type', 'Contact.Type', common.constrain_to_domain('ContactType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

STATE = Constraint('Mail State', 'Contact.MailState', common.constrain_to_domain('ContactMailState'))
STATE.triggers = [config.triggers.insert, config.triggers.update]
