if (!haskey($feature, 'ArtPen_WellName ')) {
    return true;
}

return iif(!isempty($feature.ArtPen_WellName), {
    'errorMessage': 'ArtPen well name must not be empty. Input: ' + $feature.wellname
}, true);
