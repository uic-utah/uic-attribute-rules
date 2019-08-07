// ident4ca is yes artpencatype cannot be empty
if (!haskey($feature, 'artpen_catype') || !haskey($feature, 'ident4ca')) {
    return true;
}

var no = 2;

if (isempty($feature.ident4ca) || $feature.ident4ca == no) {
    return true;
}

return iif(isempty($feature.artpen_catype), {
    'errorMessage': 'ArtPen_CAType cannot be empty when Ident4CA is yes.'
}, true);
