#!/usr/bin/env python
# * coding: utf8 *
'''
art_pen.py
A module that has the UICArtPen rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

TABLE = 'UICArtPen'

constrain_ca_type = '''if (!haskey($feature, 'artpen_catype') || !haskey($feature, 'ident4ca')) {
    return true;
}

if (isempty($feature.ident4ca)) {
    return true;
}

return iif (isempty($feature.artpen_catype), {
    'errorMessage': 'ArtPen_CAType cannot be empty when Ident4CA has a value'
}, true);'''

constrain_ca_type = '''if (!haskey($feature, 'artpen_cadate') || !haskey($feature, 'ident4ca')) {
    return true;
}

if (isempty($feature.ident4ca)) {
    return true;
}

return iif (isempty($feature.artpen_cadate), {
    'errorMessage': 'ArtPen_CADate cannot be empty when Ident4CA has a value'
}, true);'''

GUID = Constant('Art Pen Guid', 'GUID', 'ArtPen.Guid', 'GUID()')

WELL_TYPE = Constraint('Well Type', 'ArtPen.WellType', common.constrain_to_domain('artpen_wellname'))
WELL_TYPE.triggers = [config.triggers.insert, config.triggers.update]

CA_DOMAIN = Constraint('CA', 'ArtPen.Ident4CA', common.constrain_to_domain('ident4ca'))
CA_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]

CA_TYPE_DOMAIN = Constraint('CA Type', 'ArtPen.ArtPen_CAType', constrain_ca_type)
CA_TYPE_DOMAIN.triggers = [config.triggers.insert, config.triggers.update]

CA_DATE = Constraint('CA Date', 'ArtPen.ArtPen_CADate', constrain_ca_type)
CA_DATE.triggers = [config.triggers.insert, config.triggers.update]
