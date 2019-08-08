// if well class is empty, no worries
if (!haskey($feature, 'wellsubclass') || isempty($feature.wellsubclass)) {
    return true;
}

// if well class is not 1001, no worries
if ($feature.wellsubclass != 1001) {
    return true;
}

return iif(isempty($feature.nomigrationpetstatus) || domaincode($feature, 'nomigrationpetstatus', $feature.nomigrationpetstatus) == 'NA', {
    'errorMessage': 'Class I Hazardous wells require a NoMigrationPetStatus.'
}, true);
