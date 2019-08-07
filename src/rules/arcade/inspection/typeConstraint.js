if (!haskey($feature, 'inspectiontype') || !haskey($feature, 'facility_fk') || isempty($feature.inspectiontype)) {
    return true;
}

var code = lower(domaincode($feature, 'inspectiontype', $feature.inspectiontype));
if (code != 'nw' && code != 'fi') {
    return true;
}

return iif(isempty($feature.facility_fk), {
    'errorMessage': 'If InspectionType coded value is NW, then there must be a Facility_FK but no Well_FK.'
}, true);
