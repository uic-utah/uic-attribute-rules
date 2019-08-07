if (!haskey($feature, 'wellswpz') || isempty($feature.wellswpz)) {
    return true;
}

return iif(isempty(domainname($feature, 'wellswpz', $feature.wellswpz)), {
    'errorMessage': 'WellSWPZ may not be <null>; select the appropriate value from the UICGWProtectionDomain (dropdown menu). Input: ' + $feature.wellswpz
}, true);
