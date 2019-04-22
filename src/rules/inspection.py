#!/usr/bin/env python
# * coding: utf8 *
'''
inspection.py
A module that has the UICInspection rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

TABLE = 'UICInspection'

GUID = Constant('Inspection Guid', 'GUID', 'Inspection.Guid', 'GUID()')

TYPE = Constraint('Inspection Type', 'Inspection.Type', common.constrain_to_domain('InspectionType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

ASSISTANCE = Constraint('Inspection Assistance', 'Inspection.Assistance', common.constrain_to_domain('InspectionAssistance'))
ASSISTANCE.triggers = [config.triggers.insert, config.triggers.update]

DEFICIENCY = Constraint('Inspection Deficiency', 'Inspection.Deficiency', common.constrain_to_domain('InspectionDeficiency'))
DEFICIENCY.triggers = [config.triggers.insert, config.triggers.update]
