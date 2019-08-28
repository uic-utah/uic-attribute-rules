if (!haskey($feature, 'USDWContamination') || isempty($feature.USDWContamination)) {
    return $feature.SignificantNonCompliance;
}

if (lower(domaincode($feature, 'USDWContamination')) != 'y') {
    return $feature.SignificantNonCompliance;
}

return 'Y';
