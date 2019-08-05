#!/usr/bin/env python
# * coding: utf8 *
'''
operating_status.py
A module that has the UICWellOperatingStatus rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

constrain_date = '''if (!haskey($feature, 'OperatingStatusDate')) {
    return true;
}

if (date('1901-01-01') > $feature.operatingstatusdate || $feature.operatingstatusdate > date()) {
    return {
        'errorMessage': 'Operating status date needs to be between todays date and 1/1/1901'
    };
}

return true;'''

TABLE = 'UICWellOperatingStatus'

GUID = Constant('Well operating status Guid', 'GUID', 'WellOperatingStatus.Guid', 'GUID()')

TYPE = Constraint('Operating Status Type', 'OperatingStatus.Type', common.constrain_to_domain('OperatingStatusType', 'UICOperatingStatusTypeDomain'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

DATE = Constraint('Operating Status Date', 'OperatingStatus.Date', constrain_date)
DATE.triggers = [config.triggers.insert, config.triggers.update]
