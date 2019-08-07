if (!haskey($feature, 'startdate')) {
    return true;
}

return iif(isempty($feature.startdate), {
    'errorMessage': 'Authorization start date must not be empty. Input: ' + $feature.startdate
}, true);
