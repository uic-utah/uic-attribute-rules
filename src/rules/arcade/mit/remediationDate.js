if (!haskey($feature, 'mitremactdate') || !haskey($feature, 'mitremediationaction')) {
    return true;
}

if (isempty($feature.mitremediationaction) || lower(domainname($feature, 'mitremediationaction', $feature.mitremediationaction)) == 'waiting') {
    return true;
}

return iif(isempty($feature.mitremactdate), {
    'errorMessage': 'MITRemActDate may not be empty if MITRemediationAction has a value other than `waiting`.'
}, true);
