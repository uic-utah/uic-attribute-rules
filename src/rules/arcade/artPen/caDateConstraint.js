// catype is anything but waiting or empty artpencadate needs a value
if (!haskey($feature, 'artpen_cadate') || !haskey($feature, 'artpen_catype')) {
    return true;
}

var catype = domainname($feature, 'artpen_catype', $feature.artpen_catype);

return iif(isempty(catype) || catype == 'waiting', {
    'errorMessage': 'ArtPen_CADate cannot be empty when ArtPen_CAType is not <null> or waiting.'
}, true);
