if (!haskey($feature, 'ArtPen_WellName')) {
    return true;
}

return iif(isempty($feature.artpen_wellname), {
    'errorMessage': 'ArtPen well name must not be empty. Input: ' + $feature.artpen_wellname
}, true);
