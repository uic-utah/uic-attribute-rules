if (!haskey($feature, 'guid') || isempty($feature.guid)) {
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
        'errorMessage': 'There are no facilities related to this contact.'
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
    'errorMessage': 'There is no owner or operator contact type for this facility.'
};