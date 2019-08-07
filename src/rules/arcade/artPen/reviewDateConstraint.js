// review date cannot be empty when ident4ca is not null
if (!haskey($feature, 'artpen_reviewdate') || !haskey($feature, 'ident4ca')) {
    return true;
}

if (isempty($feature.ident4ca)) {
    return true;
}

return iif(isempty($feature.artpen_reviewdate), {
    'errorMessage': 'Review date is required when Ident4CA has a value.'
}, true);
