if (!haskey($feature, 'guid') || isempty($feature.guid)) {
    return true;
}

var facilitySet = FeatureSetByName($datastore, 'UICFacility', ['guid'], false);
var contactSet = FeatureSetByName($datastore, 'UICContact', ['Facility_FK', 'ContactType'], false);

var pk = $feature.facility_fk;

// TODO: One day there will be a relationship traversal operation
var facilities = filter(facilitySet, 'guid=@pk');

if (isempty(facilities)) {
    return {
        'errorMessage': 'There are no facilities related to this contact.'
    };
}

var fk = $feature.facility_fk;
var contacts = filter(contactSet, 'Facility_FK=@fk');

for (var contact in contacts) {
    if (indexof([1, 3], contact.contacttype) > -1) {
        return true;
    }
}

return {
    'errorMessage': 'There is no owner or operator contact type for this facility.'
};
