if (!haskey($feature, 'wellclass') || isempty($feature.wellclass)) {
    return true;
}

return iif(isempty(domainname($feature, 'wellclass', $feature.wellclass)), {
    'errorMessage': 'WellClass may not be <null>; select the appropriate value from the UICWellClassDomain (dropdown menu). Input: ' + $feature.wellclass
}, true)
