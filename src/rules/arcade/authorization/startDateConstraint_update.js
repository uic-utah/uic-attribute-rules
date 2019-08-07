if (!haskey($feature, 'startdate ')) {
    return true;
}

return iif(!isempty($feature.ArtPen_WellName), {
    'errorMessage': 'Authorization start date must not be empty. Input: ' + $feature.startdate
}, true);
