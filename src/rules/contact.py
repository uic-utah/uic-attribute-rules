#!/usr/bin/env python
# * coding: utf8 *
'''
contact.py
A module that has the UICContact rules
'''

from . import common
from config import config
from models.ruletypes import Constant, Constraint

#: can't featureset by name a m*m relationship table
constrain_contact_type = '''if (!haskey($feature, 'guid') || isempty($feature.guid)) {
    return true;
}

var fields = ['facilityguid', 'contactguid'];
var xref = FeatureSetByName($datastore, 'UICFacilityToContact', fields, false);
var contactSet = FeatureSetByName($datastore, 'UICContact', ['guid', 'contacttype'], false);

var pk = $feature.guid;

// TODO: One day there will be a relationship traversal operation
var relations = filter(xref, 'contactguid=@pk');

if (isempty(relations)) {
    return {
        'errorMessage': 'There are no facilities related to this contact'
    };
}

var querystring = 'guid in (';

for (var relation in relations) {
    querystring += "'" + relation.contactguid + "',";
}

querystring = left(querystring, count(querystring) - 1) + ')';

var contacts = filter(contactSet, querystring);

for (var contact in contacts) {
    if (indexof([1, 3], contact.contacttype) > -1) {
        return true;
    }
}

return {
    'errorMessage': 'There is no owner or operator contact type for this facility'
};
'''

TABLE = 'UICContact'

GUID = Constant('Contact Guid', 'GUID', 'Contact.Guid', 'GUID()')

TYPE = Constraint('Contact Type', 'Contact.Type', common.constrain_to_domain('ContactType'))
TYPE.triggers = [config.triggers.insert, config.triggers.update]

STATE = Constraint('Mail State', 'Contact.MailState', common.constrain_to_domain('ContactMailState'))
STATE.triggers = [config.triggers.insert, config.triggers.update]

CONTACT_TYPE = Constraint('Owner Operator', 'Contact.OwnerType', constrain_contact_type)
CONTACT_TYPE.triggers = [config.triggers.insert, config.triggers.update]
